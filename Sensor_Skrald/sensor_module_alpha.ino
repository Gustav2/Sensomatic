// Include required libraries
#include <SPI.h>
#include <LoRa.h>
#include <WiFi.h>
#include "Adafruit_VL53L1X.h"

#define IRQ_PIN 18
#define XSHUT_PIN 19

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Define the pins used by the LoRa module
const int csPin = 0;     // LoRa radio chip select
const int resetPin = 1;  // LoRa radio reset
const int irqPin = 2;    // Must be a hardware interrupt pin

String UID = WiFi.macAddress();

int sleepInterval;
RTC_DATA_ATTR int oldNtp;

bool setupReceived = false; // Flag for ascertaining whether setup data has been received

// Message counter
byte msgCount = 0;

void initial_setup()  {
  // This function runs the first time the ESP is active without any settings collected from the gateway
  
  while (!setupReceived)  {    
    // Requests setup data
    LoRa.beginPacket();
    LoRa.print("@requestSetup");
    LoRa.print("#");
    LoRa.print(WiFi.macAddress());
    LoRa.endPacket();
    Serial.println("@requestSetup package sent!");
    
    delay(1000);
    
    unsigned long startTime;
    unsigned long waitTime = 5000;

    startTime = millis();
    while (millis() - startTime < waitTime)  {
      int packetSize = LoRa.parsePacket(); // Try to parse the packet
      if (packetSize) {   // When LoRa packet received
        Serial.println("Received packet!");
        while (LoRa.available()) {          // Read packet
          String receivedSetup = LoRa.readString();
          Serial.println(receivedSetup);
    
          // Read data from string
          // Incoming format: ?responseSetup&requestUID%currentTime#transmitInterval
          
          int pos1 = receivedSetup.indexOf("&");
          int pos2 = receivedSetup.indexOf("%");
          int pos3 = receivedSetup.indexOf("#");
          
          String responseUID = receivedSetup.substring(pos1+1, pos2);

          Serial.print("Personal UID: ");
          Serial.println(UID);
          Serial.print("Received UID: ");
          Serial.println(responseUID);
          
          if (responseUID == UID) {
            String ntpTimeString = receivedSetup.substring(pos2+1, pos3);
            String newIntervalString = receivedSetup.substring(pos3+1, receivedSetup.length());
            
            int ntpTime = (ntpTimeString.toInt());
            sleepInterval = newIntervalString.toInt();

            int ntpPassed = (ntpTime - oldNtp)*1000;

            Serial.println("");
            Serial.print("NTP time from transmission: ");
            Serial.println(ntpTime);
            Serial.print("NTP time since last transmission: ");
            Serial.println(ntpPassed);
            Serial.println("");
            
            oldNtp = ntpTime;
            setupReceived = true;
            }
            
          else {
            Serial.println("Data for other UID received, repeating...");
            delay(1000);
            }
          }
        }
      }
    }
    Serial.println("setupReceived successful");
    Serial.println("");
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
  Serial.println("");
  /*
  vl.VL53L1X_SetDistanceThreshold(100, 300, 3, 1);
  vl.VL53L1X_SetInterruptPolarity(0);
  */

  Serial.println("setup_tof() successful");

}

void sensor() {
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
    Serial.print("UID: ");
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
  delay(1000);
}

void initialise() {
  setup_lora();
  delay(100);
  initial_setup();
  delay(100);
  setup_tof();
  delay(100);
  Serial.println("initialise successful");
}



void setup() {
  Serial.begin(115200);
  Serial.println("------------------------------------------------");
  delay(500);
  initialise();
  Serial.println("");
  Serial.println("Running sensor program...");
  delay(500);
  sensor();
  delay(500);
  setupReceived = false;
  Serial.println("");
  Serial.print("Entering sleep for: ");
  Serial.println(sleepInterval);
  Serial.println("================================================");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(sleepInterval * 1000);
  esp_deep_sleep_start();
}

void loop() {
  // loop() is never ran due to the sleep functionality.
}