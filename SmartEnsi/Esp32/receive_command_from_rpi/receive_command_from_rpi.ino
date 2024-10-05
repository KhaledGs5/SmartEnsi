#include <WiFi.h>
#include <Stepper.h>


int isclosed = 1;


 
// settings stepper motor
const int STEPS_PER_REV = 200;
Stepper stepper_NEMA17(STEPS_PER_REV, 32, 33, 25, 26);



// setting up wifi and port
const char* ssid = "Khaled";
const char* password = "Khaled5";
const int port = 12345;

WiFiServer server(port);


 // course formula in cm
  int x = 33;
  int step_number = (x*10/1.5)*200;

void setup() {

  pinMode(5,OUTPUT);
  digitalWrite(5,HIGH);


  pinMode(32,OUTPUT);
  pinMode(33,OUTPUT);
  pinMode(25,OUTPUT);
  pinMode(26,OUTPUT);

  //open();

  pinMode(2,OUTPUT);
  Serial.begin(115200);
  delay(100);

  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("Connected to WiFi");

  // Start the server
  server.begin();
  Serial.println("Server started");

  stop();


 
 
}


 


void loop() {
  // Check if a client has connected
  
  stop();
  
  
  WiFiClient client = server.available();
  if (client) {
    
    Serial.println("Client connected");

    // Read the incoming data
    String request = client.readStringUntil('\r');
    Serial.print("Received message: ");
    Serial.println(request);

    if(request == "open" && isclosed){
      //open();
      //play_led(5);
      open();
      stop();

      isclosed = 0;
      
    }
    else if(request == "close" ){
      //close();
      //play_led(5);
      close();
      stop();
      isclosed = 1;
   
    }

    




    // Send a response back to the client
    client.print("Message received by ESP32!");

    // Close the connection
    client.stop();
    Serial.println("Client disconnected");
  }
}

void play_led(int n) {
  for(int i=0 ; i<n ; i++){
    digitalWrite(2,HIGH);
    delay(200);
    digitalWrite(2,LOW);
    delay(200);
  }
  
}

void close(){

  

    stepper_NEMA17.setSpeed(300);
  
    stepper_NEMA17.step(step_number);
    //stepper_NEMA17.step(0 );
    stop();
    
}

void open(){

    stepper_NEMA17.setSpeed(300);
    
    stepper_NEMA17.step(-step_number);
    //stepper_NEMA17.step(0 );
    stop();
    
}


void stop(){

  
  digitalWrite(32,LOW);
  digitalWrite(33,LOW);
  digitalWrite(25,LOW);
  digitalWrite(26,LOW);

  delay(500);
   
  
    
}
