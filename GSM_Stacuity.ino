#include <SoftwareSerial.h>

//Create software serial object to communicate with SIM800L
SoftwareSerial mySerial(3, 2); //SIM800L Tx & Rx is connected to Arduino #3 & #2

String message;

void setup()
{
  //Begin serial communication with Arduino and Arduino IDE (Serial Monitor)
  Serial.begin(9600);
  
  //Begin serial communication with Arduino and SIM800L
  mySerial.begin(9600);

  Serial.println("Initializing..."); 
  delay(1000);

  mySerial.println("AT"); //Once the handshake test is successful, it will back to OK
  updateSerial();

  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  mySerial.println("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
  updateSerial();
  mySerial.println("AT+SAPBR=3,1,\"APN\",\"stacuity.flex\"");
  updateSerial();

  // Open a GPRS context
  mySerial.println("AT+SAPBR=1,1");
  updateSerial();

  // Initialize HTTP service
  mySerial.println("AT+HTTPINIT");
  updateSerial();
}

void loop()
{
 if (mySerial.available())
  {
    while (mySerial.available())
    {
      char c = mySerial.read();
      message += c; // Build the message from received characters
    }
    Serial.print("Received message: ");
    Serial.println(message);

    // Send the message to the endpoint
    sendHTTPPostRequest("https://9549-102-217-4-50.ngrok-free.app/api/bulk-sms", message);

    message = ""; // Clear the message for the next round
  }
}

void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    mySerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while(mySerial.available()) 
  {
    Serial.write(mySerial.read());//Forward what Software Serial received to Serial Port
  }
}

void sendHTTPPostRequest(String url, String data)
{
  mySerial.print("AT+HTTPPARA=\"URL\",\"");
  mySerial.print(url);
  mySerial.println("\"");
  updateSerial();

  mySerial.println("AT+HTTPDATA=" + String(data.length()) + ",10000");
  updateSerial();
  mySerial.println(data);
  updateSerial();

  mySerial.println("AT+HTTPACTION=1");
  updateSerial();
}