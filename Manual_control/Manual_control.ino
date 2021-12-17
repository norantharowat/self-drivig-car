#include <SPI.h>
#include <RFID.h>
#define SS_PIN 10
#define RST_PIN 8
RFID rfid(SS_PIN, RST_PIN);

String rfidCard;


//Motor driver setup L298N
const int IN1 = 7; 
const int IN2 = 6; 
const int IN3 = 5; 
const int IN4 = 4; 

/* this will allow you to control the speed of the motors */

const int ENA = 9; 
const int ENB = 3; 

int command = 0;


int trig = A0; 
int echo = A1; 


void setup() {
  Serial.begin(9600);
  //Serial.println("Starting the RFID Reader...");
  SPI.begin();
  rfid.init();


  // set motor driver`s pins to output
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (ENA, OUTPUT);
  pinMode (ENB, OUTPUT);

  //set trig pin as output and the echo pin as input for the ultrasonic sesor
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  
}

void loop() {
  if (rfid.isCard()) {
    if (rfid.readCardSerial()) {
      rfidCard = String(rfid.serNum[0]) + " " + String(rfid.serNum[1]) + " " + String(rfid.serNum[2]) + " " + String(rfid.serNum[3]);
      Serial.println(rfidCard);
    }
    rfid.halt();
  }




  if (Serial.available() > 0) //check if the arduino is receiving data or not
{
  command=Serial.read(); 
}
if (command == '0')//moving Forward

  {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2,LOW );
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 100);
    analogWrite(ENB, 100);
    command=0; 
  }
else if(command == '1') // moving backward
  {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 100);
    analogWrite(ENB, 100);
    
    command=0; 
  }
 else if (command == '2') //moving left
 {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 80);
    analogWrite(ENB, 80);
    command=0; 
  }
else if (command == '3') //moving right
{
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 80);
    analogWrite(ENB, 80);
    command=0; 
  }
else if (command == '4') //stop the motors
{
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, HIGH);
    command=0; 
  }


else if (command == '5') 
{


long du = 0, ds = 0; // Transmitting pulse
digitalWrite(trig, LOW); //set trig pin to high
delayMicroseconds(10); //wait 2MS
digitalWrite(trig, HIGH); //set trig pin to high to send pulse
delayMicroseconds(10); //wait 10MS
digitalWrite(trig, LOW);// Waiting for pulse
du = pulseIn(echo, HIGH);// check for the pulse
ds = du*0.034/2 ;// Calculating distance
Serial.println(ds);
//move the motors forward

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 90);
    analogWrite(ENB, 90);

if (ds<=10) //if the space betwen the robot and the object less than 10 or 10 then turn right until the robot gets a space more than 10
{
    
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 60);
    analogWrite(ENB, 60);
    delay(1000);
     
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 40);
    analogWrite(ENB, 40);
   delay(1000);
} 
command='5'; //here we will let the robot do the same job untill the we press stop bottom from mobile or press any bottom so we control it manualy 
}



  
}
