#include <SocketIoClient.h>
#include <ArduinoJson.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include "ESPAsyncWebServer.h"
//#define USER_SERIAL Serial


//void event(const char * auto_direction, size_t length) {
//  Serial.write(String(auto_direction).c_str());
////      for (size_t i = 0; i < length; i++) {
////
////        Serial.write(auto_direction[i]);
////
////          
////      }
//     
//      Serial.println("");
////  Serial.printf("gotauto_direction message: %s\n", auto_direction);
//}

const char* ssid = "STUDBME2";
const char* pass = "BME2Stud";




//const char* ssid = "ZoZo";
//const char* pass = "123456790";

AsyncWebServer server(80);
String RFID;



SocketIoClient webSocket;


void setup() {



  Serial.begin(115200);


  connectWiFi();


server.on( "/direction", HTTP_POST, [](AsyncWebServerRequest * request){}, NULL,
    [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {

      for (size_t i = 0; i < len; i++) {

        Serial.write(data[i]);

          
      }
     
      Serial.println();
      request->send(200);
  });
  
   server.begin(); 
  

  webSocket.begin("172.28.135.133", 5000);
//   webSocket.begin("192.168.43.226", 5000);
//  webSocket.on("auto_direction", event); 
  
 
  
}

void loop() {


 if (Serial.available() > 0 ) //check if the arduino is receiving data or not
{
  RFID=Serial.readString();
//  Serial.println(RFID); 
  String msg = String("\"");
  msg += RFID;
  msg += "\"";
 if(RFID == "F" || RFID == "B" || RFID == "L" || RFID == "R" || RFID == "S" || RFID == "K" || RFID == "O" || RFID == " " ){
  // do nothing
  } else{
    webSocket.emit("test", msg.c_str() );  
    }
  
      
  
}



  webSocket.loop();

}

//void controlled(const char* auto_direction, size_t length){
//  Serial.println(auto_direction);
//
//
//  
//  
//}




void connectWiFi(){
  WiFi.begin(ssid, pass);
  while(WiFi.status() != WL_CONNECTED){
//    Serial.print(".");
    delay(1000);
  }

//  Serial.print("");
//  Serial.println("WiFi connected");
//  Serial.print("IP Address : ");
//  Serial.println(WiFi.localIP());
  
}
