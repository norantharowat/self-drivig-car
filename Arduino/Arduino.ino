
char value ;
//String value ;
void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);
  
  
}
 
void loop(){
  
  
  



   if (Serial.available() > 0) {
//     read the incoming byte:
    value = Serial.read(); 
    // say what you got:
    Serial.print(value);
//    Serial.println("");
    
    
  }
}
