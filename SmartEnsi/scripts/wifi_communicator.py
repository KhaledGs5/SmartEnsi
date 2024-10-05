import time
import socket
import threading
from queue import Queue


class InMessage:

    def __init__(self, data: str, require_ack: bool, client_addr: str) -> None:
        self.data = data
        self.require_acknowledgment = require_ack
        self.client_addr = client_addr


class OutMessage:

    def __init__(self, data: str, require_ack: bool = False) -> None:
        self.data = data


class WiFiCommunicator:

    ACKNOWLEDGMENT_FLAG = 'A'
    CPU_RELEASE_SLEEP = 0.000_001

    def __init__(self, max_buffer_sz: int, port: int = 11111, in_queue_sz: int = 0, out_queue_sz: int = 0) -> None:

        assert max_buffer_sz > 0, f"Buffer size must be > 0 [{max_buffer_sz = }]"
        assert in_queue_sz >= 0, f"Queue size can't be negative [{in_queue_sz = }]"
        assert out_queue_sz >= 0, f"Queue size can't be negative [{out_queue_sz = }]"
        
        # Signal to the communicator to "Rest In Peace"
        self._rip = False
        self._have_client = False


        self._max_buffer_size = max_buffer_sz
        self._incoming_messages_queue = Queue(maxsize=in_queue_sz)
        self._outgoing_messages_queue = Queue(maxsize=out_queue_sz)

        # Client info
        self._client = None
        self._client_address = None

        # Socket creation
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # To allow the ESP through the firewall (if u had firewall problems, and u're on Linux):
        # $ sudo iptables -I INPUT -s ESP.IP.GOES.HERE -p tcp --dport 15000 -j ACCEPT 
        soc.bind(('0.0.0.0', port))
        soc.listen(0)

        # Start the show
        self._threads = [
            threading.Thread(target=self.__listener_thread, daemon=True),
            threading.Thread(target=self.__sender_thread, daemon=True),
            threading.Thread(target=self.__wait_for_connection_thread, daemon=True, args=[soc]),
        ]
        for thread in self._threads:
            thread.start()

    def get_message(self) -> InMessage:
        return self._incoming_messages_queue.get()

    def send_message(self, message: OutMessage) -> None:

        self._outgoing_messages_queue.put(message)

    def destroy(self):

        if self._client is not None:
            self._client.close()
        
        self._rip = True
        for thread in self._threads:
            thread.join(0.1)

    def __wait_for_connection_thread(self, soc: socket.socket) -> None:

        self._client, self._client_address = soc.accept()
        self._have_client = True

    def __decode(self, in_bytes: bytes) -> 'None|InMessage':

        message = in_bytes.decode()
        if not len(message):
            return None

        ack = message[0] == self.ACKNOWLEDGMENT_FLAG
        data = message[1 * ack:]
        return InMessage(data=data, require_ack=ack, client_addr=self._client_address)

    def __listener_thread(self):
        '''
        '''
        while not self._rip:
            if not self._have_client:
                time.sleep(self.CPU_RELEASE_SLEEP)
                continue

            message = self._client.recv(self._max_buffer_size)
            decoded_msg = self.__decode(message)
            if decoded_msg is not None:
                self._incoming_messages_queue.put(decoded_msg)

    def __encode(self, message: OutMessage) -> bytes:
        '''
        Encodes the outgoing message into the required sendable format
        '''
        return message.data.encode()

    def __sender_thread(self):
        '''
        '''
        while not self._rip:
            if not self._have_client:
                time.sleep(self.CPU_RELEASE_SLEEP)
                continue

            # This is blocking on purpose, if not, we'd have to handle getting no-data when timing-out
            msg = self._outgoing_messages_queue.get()
            self._client.send(self.__encode(msg))
