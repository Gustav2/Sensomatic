// To be done:
// LoRa setup data response is not currently received
// Implement setting up with received data once functional


// Include required libraries
#include <SPI.h>
#include <LoRa.h>
#include "Adafruit_VL53L1X.h"

#define IRQ_PIN 18
#define XSHUT_PIN 19

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Define the pins used by the LoRa module
const int csPin = 0;     // LoRa radio chip select
const int resetPin = 1;  // LoRa radio reset
const int irqPin = 2;    // Must be a hardware interrupt pin

String UID = "0";
String NTP_Time;
String interval;

bool setupReceived = false; // Flag for ascertaining whether setup data has been received

// Message counter
byte msgCount = 0;

void initial_setup()  {
  while (!setupReceived)  {    
    // Requests setup data
    LoRa.beginPacket();
    LoRa.print("@requestSetup");
    LoRa.endPacket();
    Serial.println("@requestSetup package sent!");
    
    delay(1000);
    
    unsigned long startTime;
    unsigned long waitTime = 5000;

    startTime = millis();

    int packetSize = LoRa.parsePacket(); // Try to parse the packet

    while (millis() - startTime < waitTime)  {
      if (packetSize) {
        Serial.println("Received packet!");
        break;
        }
      }
  
    if (packetSize) {   // When LoRa packet received
      Serial.println("Received packet!");
      // Read packet
      while (LoRa.available()) {
        String receivedSetup = LoRa.readString();
        Serial.println(receivedSetup);
  
        // Read data from string
        // Incoming format: Your UID # Current NTP time & Your transmit interval
        int pos1 = receivedSetup.indexOf("#");
        int pos2 = receivedSetup.indexOf("&");
  
        if (UID == "0"){
          UID = receivedSetup.substring(0, pos1);
        }
        
        NTP_Time = receivedSetup.substring(pos1+1, pos2);
        interval = receivedSetup.substring(pos2+1, receivedSetup.length());     

        setupReceived = true;
        
        }
      }
      else {
        Serial.println("No setupReceived, repeating...");
        }
        
      delay(5000);
    }
    Serial.println("setupReceived successful");
    delay(1000);
  }


void setup_lora() {
  // Setup LoRa module
  LoRa.setPins(csPin, resetPin, irqPin);
 
  Serial.println("LoRa Receiver Test");
 
  // Start LoRa module at local frequency
  // 433E6 for Europe
  // 866E6 for Europe
  // 915E6 for North America
 
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1)
      ;
  }

  // Set spreading factor to highest
  LoRa.setSpreadingFactor(12);

  // Set signal bandwith. Must be 125 kHz or 250 kHz in Europe
  LoRa.setSignalBandwidth(125E3);

  // This combination results in an approximate bitrate of 250 bits/second according to TTN

  Serial.println("setup_lora() successful");
}

void setup_tof() {
  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();
  if (! vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  if (! vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());

  /*
  vl.VL53L1X_SetDistanceThreshold(100, 300, 3, 1);
  vl.VL53L1X_SetInterruptPolarity(0);
  */

  Serial.println("setup_tof() successful");

}

void setup() {
  Serial.begin(115200);

  while (!Serial) {
    delay(10);     // will pause Zero, Leonardo, etc until serial console opens
  }
  setup_lora();
  initial_setup();
  setup_tof();
  Serial.println("setup() successful");
}

void loop() {

 // TOF reading part
  int16_t distance;
  if (vl53.dataReady()) {
    // new measurement for the taking!
    distance = vl53.distance();
    if (distance == -1) {
      // something went wrong!
      Serial.print(F("Couldn't get distance: "));
      Serial.println(vl53.vl_status);
      return;
    }
    Serial.print(F("Distance: "));
    Serial.print(distance);
    Serial.println(" mm");

    // LoRa transmission part
    // Create payload for packet
    // Format "UID#distance/msgCount
    String payload = String(UID) + "#" + String(distance) + "/" + String(msgCount);

    // LoRa packet sending
    Serial.print("Sending packet: ");
    Serial.println(msgCount);
    Serial.println("UID: ");
    Serial.println(UID);

    // Send packet
    LoRa.beginPacket();
    LoRa.print(payload);
    LoRa.endPacket();
 
    // Increment packet counter
    msgCount++;

    // data is read out, time for another reading!
    vl53.clearInterrupt();
  }
  // Delay between transmissions
  delay(5000);
}