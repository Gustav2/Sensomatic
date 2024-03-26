//LoRa
// Include required libraries
#include <SPI.h>
#include <LoRa.h>

//Sensor
// defines pins numbers
const int trigPin = 18;
const int echoPin = 19;

//LoRa
// Define the pins used by the LoRa module
const int csPin = 0;     // LoRa radio chip select
const int resetPin = 1;  // LoRa radio reset
const int irqPin = 2;    // Must be a hardware interrupt pin

// Message counter
byte msgCount = 0;

//Sensor
// defines variables
long duration;
int distance;
void setup() {
  //Sencor
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(115200); // Starts the serial communication

  //LoRa
  while (!Serial)
    ;
  // Setup LoRa module
  LoRa.setPins(csPin, resetPin, irqPin);
 
  Serial.println("LoRa Sender Test");
  
  // Start LoRa module at local frequency
  // 433E6 for Asia
  // 866E6 for Europe
  // 915E6 for North America
 
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1)
      ;
  }
}
void loop() {
  //Sensor
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);


  // LoRa
  Serial.print("Sending packet: ");
  Serial.println(msgCount);
 
  // Send packet
  LoRa.beginPacket();
  LoRa.print("Sensor 0, ");
  LoRa.print("Packet ");
  LoRa.print(msgCount);
  LoRa.print(", Distance: ");
  LoRa.print(distance);
  LoRa.endPacket();
 
  // Increment packet counter
  msgCount++;
 
  // 5-second delay
  delay(5000);

}

