// Include required libraries
#include <SPI.h>
#include <LoRa.h>
#include <WiFi.h>
#include <math.h>
#include "Adafruit_VL53L1X.h"
#include "esp_sleep.h"

#define IRQ_PIN 18
#define XSHUT_PIN 19

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
const int NUM_MEASUREMENTS = 1000;  // Define the number of measurements

// Define the pins used by the LoRa module
const int csPin = 0;     // LoRa radio chip select
const int resetPin = 1;  // LoRa radio reset
const int irqPin = 2;    // Must be a hardware interrupt pin

String UID = WiFi.macAddress();

uint64_t sleepInterval;
int randomDelay = 0;

bool setupReceived = false; // Flag for ascertaining whether setup data has been received

void initial_setup()  {
  // This function runs the first time the ESP is active without any settings collected from the gateway
  
  while (!setupReceived)  {    
    // Requests setup data
    LoRa.beginPacket();
    LoRa.print("@");
    LoRa.print(WiFi.macAddress());
    LoRa.endPacket();
    Serial.println("@requestSetup package sent!");
    // Format: @macAddress
    delay(1000);
    
    unsigned long startTime;
    unsigned long waitTime = 15000;

    startTime = millis();
    while (millis() - startTime < waitTime)  {
      int packetSize = LoRa.parsePacket(); // Try to parse the packet
      if (packetSize) {   // When LoRa packet received
        Serial.println("Received packet!");
        while (LoRa.available()) {          // Read packet
          String receivedSetup = LoRa.readString();
          Serial.println(receivedSetup);
    
          // Read data from string
          // Incoming format: ?requestUID%transmitInterval
          
          int pos1 = receivedSetup.indexOf("%");
          
          String responseUID = receivedSetup.substring(1, pos1);

          Serial.print("Personal UID: ");
          Serial.println(UID);
          Serial.print("Received UID: ");
          Serial.println(responseUID);
          
          if (responseUID == UID) {
            String newIntervalString = receivedSetup.substring(pos1+1, receivedSetup.length());            
            sleepInterval = newIntervalString.toInt();
            setupReceived = true;
            }
            
          else {
            Serial.println("Data for other UID received, repeating...");
            randomDelay = random(20000, 60000);
            Serial.print("Delay  is: ");
            Serial.println(randomDelay);
            delay(randomDelay);
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
  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();
  if (!vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }
  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  if (!vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }
  Serial.println(F("Ranging started"));

  vl53.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());

  Serial.println("setup_tof() successful");

  }

void hibernation()  {
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH,   ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_XTAL,         ESP_PD_OPTION_OFF);
  
  esp_sleep_enable_timer_wakeup(sleepInterval*1000);
  esp_deep_sleep_start();
  }

void sensor() {
   // TOF reading part
  float measurements[NUM_MEASUREMENTS];
  if (vl53.dataReady()) {
    // Read distance and store in array
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
      measurements[i] = vl53.distance();
      if (measurements[i] == -1) {
        Serial.print(F("Couldn't get distance: "));
        Serial.println(vl53.vl_status);
        return;
      } 
    }

    // Sort measurements
    std::sort(measurements, measurements + NUM_MEASUREMENTS);

    // Calculate median = distance
    float distance = 0.0;
    if (NUM_MEASUREMENTS % 2 == 0) {
      distance = (measurements[NUM_MEASUREMENTS / 2 - 1] + measurements[NUM_MEASUREMENTS / 2]) / 2.0;
      } 
    else {
      distance = measurements[NUM_MEASUREMENTS / 2];
      }

    Serial.print(F("Distance: "));
    Serial.print(distance);
    Serial.println(" mm");

    digitalWrite(LED_BUILTIN, LOW);

    // LoRa transmission part
    // Create payload for packet
    // Format "&data#UID
    String payload = "&" + String(distance) + "#" + String(UID);
    // LoRa packet sending
    Serial.print("Sending packet as: ");
    Serial.print("UID: ");
    Serial.println(UID);
    Serial.println(payload);

    // Send packet
    LoRa.beginPacket();
    LoRa.print(payload);
    LoRa.endPacket();

    // data is read out, time for another reading!
    vl53.clearInterrupt();
  // Delay between transmissions
  delay(1000);
  }
}

void initialise() {
  pinMode(LED_BUILTIN, OUTPUT);
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
  Serial.print(sleepInterval / 60000);
  Serial.println(" minutes");
  Serial.println("================================================");
  Serial.flush();
  hibernation();
  }


void loop() {
  // loop() is never ran due to the sleep functionality.
  }
