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

// Message counter
byte msgCount = 0;

void setup_lora() {
  // Setup LoRa module
  LoRa.setPins(csPin, resetPin, irqPin);
 
  Serial.println("LoRa Receiver Test");
 
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
}

void setup() {
  Serial.begin(115200);

  while (!Serial) {
    delay(10);     // will pause Zero, Leonardo, etc until serial console opens
  }
    
  setup_lora();
  setup_tof();
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
    String payload = String(msgCount) + "#" + String(distance) ;

    // LoRa packet sending
    Serial.print("Sending packet: ");
    Serial.println(msgCount);

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
