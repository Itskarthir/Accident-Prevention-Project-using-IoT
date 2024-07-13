/*
import serial

# Open a serial connection to the Arduino
ser = serial.Serial('COM3', 9600)  # Change the port and baud rate as necessary

# Send data to the Arduino
data = 'off'
ser.write(data.encode())

# Close the serial connection
ser.close()
   
    
    */
#include <TinyGPS++.h>
#include <SoftwareSerial.h>//Library used to create software serial port                                  
                  // library used to enable i2c port 

String str="";
int relay= 12 ;
 long lastrep =0;
int Number_of_SATS;       // Variable used to store number of satellite  
String latitude;         // variable to store latitude
String longitude;       // variable to store longitude                                 
TinyGPSPlus gps;         // create oject gps to class TinyGPSPLUS
SoftwareSerial serial2(10, 11);
void setup() {
   
 
  pinMode(relay,OUTPUT);
  digitalWrite(relay,LOW);
  serial2.begin(9600);
  Serial.begin(9600);  // Set the baud rate to match the Python program
}
void getGPS()                                                 // Get Latest GPS coordinates
{

  while (serial2.available() > 0)             //check for gps data available in serial port
  {
    gps.encode(serial2.read());
  }                 // encode the gps data into latitude and longitude 

latitude =String( gps.location.lat(),6); //fe tch latitude and store 
longitude =String (gps.location.lng(),6); // fetch longitude and store 

}
void sendsms(){
  getGPS();                 // Get gps data
str = String ("Driver is in Emgergency Situation his live location= http://maps.google.com/maps?q="+latitude+"," +longitude);


Serial.println("AT+CMGF=1");    //Sets the GSM Module in Text Mode
  delay(1000);  // Delay of 1000 milli seconds or 1 second
  Serial.println("AT+CMGS=\"+919110686998\"\r"); // Replace x with mobile number
  delay(1000);
Serial.println(str);// The SMS text you want t,m nb  o send
  delay(100);
   Serial.println((char)26);// ASCII code of CTRL+Z
  delay(8000);

   Serial.println("ATD+ +919110686998;");
delay(20000);
Serial.println("ATH");



  Serial.println("AT+CMGF=1");    //Sets the GSM Module in Text Mode
  delay(1000);  // Delay of 1000 milli seconds or 1 second
  Serial.println("AT+CMGS=\"+919008930036\"\r"); // Replace x with mobile number
  delay(1000);
Serial.println(str);// The SMS text you want t,m nb  o send
  delay(100);
   Serial.println((char)26);// ASCII code of CTRL+Z
  delay(8000);
 

  }
 


void loop() {
  getGPS();
  if (Serial.available() > 0) {
    String data = Serial.readString();  // Read the data from the serial port
    //Serial.println(data);  // Print the data to the serial monitor
    digitalWrite(relay,HIGH);
      sendsms();
    
  }
}
