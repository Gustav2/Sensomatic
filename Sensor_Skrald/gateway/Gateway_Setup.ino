// To be done:
// LoRa setup data response is not currently received by sensor
// UID is not currently being set either by server nor gateway
// Time intervals are not currently given
// Potential handling of on-the-fly setting adjustment of sensors

// Include required libraries
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <SPI.h>
#include <LoRa.h>
#include "time.h"

// Define the pins used by the LoRa module
const int csPin = 0;     // LoRa radio chip select
const int resetPin = 1;  // LoRa radio reset
const int irqPin = 2;    // Must be a hardware interrupt pin

// Information for WiFi connection
const char* ssid = "Sensomatic";
const char* password = "password12!";

// Information for NTP connection
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;

// Variables for sensor data storage
String msgCount;
String distance;

int NTP;
int transmitInterval;

// JSON size
char jsonOutput[128];

void wifi_setup() {
  delay(1000);
  WiFi.begin(ssid, password);   //Connects to the WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");    // Prints connecting message if not connected
  }
  Serial.println("Connected succesfully!");     // Connected
}

void lora_setup() {
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
}


// Function for getting current time in UNIX format
time_t getTime()  {
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  time_t now = time(nullptr);
  while (now < 1000000000) {
    delay(500);
    now = time(nullptr);
  }
  return now;
}

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;

  wifi_setup();
  lora_setup();
}
 
void loop() {
  int packetSize = LoRa.parsePacket(); // Try to parse the packet

  if (packetSize) {   // When LoRa packet received
    Serial.println("Received packet!");
    
    // Read packet
    while (LoRa.available()) {
      String payload = LoRa.readString();
      Serial.println(payload); 

      if (String(payload[0]) == "@") {
        Serial.println("Setup request received");
        int pos1 = payload.indexOf("#");
        
        String requestUID = payload.substring(pos1+1, payload.length());
        
        time_t currentTime = getTime();
        Serial.println(currentTime);
      
        String(outbound) = "?responseSetup&" + String(requestUID) + "%" + String(currentTime) + "#" + String(transmitInterval);
      
        delay(2000);
      
        Serial.print("Current outbound String: ");
        Serial.println(outbound);
        
        LoRa.beginPacket();
        LoRa.print(outbound);
        LoRa.endPacket();
      
        Serial.println("Outbound package sent");
      }

      else {
        // Read data from string
        // Format "UID#distance/msgCount
        int pos1 = payload.indexOf("#");
        int pos2 = payload.indexOf("/");
    
        String MAC = payload.substring(0, pos1);
        distance = payload.substring(pos1+1, pos2);
        msgCount = payload.substring(pos2+1, payload.length());
      
        // POST this to the HTTP connection
        if (WiFi.status() == WL_CONNECTED) {
          HTTPClient http;
    
          http.begin("http://192.168.0.102:8000/datacollector/handle_post/"); // Specify destination for HTTP request
          http.addHeader("Content-Type", "application/json"); // Specify content-type header
    
          const size_t CAPACITY = JSON_OBJECT_SIZE(1);
          StaticJsonDocument<CAPACITY> doc;
    
          JsonObject object = doc.to<JsonObject>();
          object["MAC"] = MAC;
          object["distance"] = distance;
          object["message count"] = msgCount;
          object["rssi"] = LoRa.packetRssi();
    
          serializeJson(doc, jsonOutput);
          
    
          int httpResponseCode = http.POST(String(jsonOutput)); // Actual POST request
    
            
          String response = http.getString();       // Get response and print in Serial
          Serial.print("httpResponseCode: ");
          Serial.println(httpResponseCode);
          Serial.print("response: ");
          Serial.println(response);
        
          http.end();   // Ends HTTP to free resources
        
        }
        
        else {
          Serial.println("Error in WiFi connection");
          }
      }

    // NO DELAY IN THIS CODE
    // Delay is currently implemented on the individual sensor transmission. 
    // The gateway relays the LoRa data to the server as fast as possible
    }
  }
}