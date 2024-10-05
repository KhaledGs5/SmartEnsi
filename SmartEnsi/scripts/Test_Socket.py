import socket

def send_message_to_esp32(message, esp32_ip='192.168.1.84', esp32_port=12345):

    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the ESP32
        sock.connect((esp32_ip, esp32_port))

        # Send the message
        sock.sendall(message.encode())

        print("Message sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the socket
        sock.close()
