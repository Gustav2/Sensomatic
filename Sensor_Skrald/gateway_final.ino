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

const char* httpDestination = "https://api.faauzite.com/datacollector/handle_post/";

// Information for NTP connection
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;

unsigned long epochTime;

// Variables for sensor data storage
String distance;

int NTP;
int sleepInterval = 1; // Default in minutes

// JSON size
char jsonOutput[128];

void wifi_setup() {
  delay(1000);
  WiFi.begin(ssid, password);   //Connects to the WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("------------------------------------------------");
    Serial.println("Connecting to WiFi...");    // Prints connecting message if not connected
  }
  Serial.println("Connected succesfully!");     // Connected
}

void lora_setup() {
  // Setup LoRa module
  LoRa.setPins(csPin, resetPin, irqPin);
 
  Serial.println("LoRa setup begun");
 
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
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;

  wifi_setup();
  configTime(0, 0, ntpServer);
  lora_setup();
}
 
void loop() {
  int packetSize = LoRa.parsePacket(); // Try to parse the packet
  if (packetSize) {   // When LoRa packet received
    time_t currentTime = getTime(); // Get current time
    struct tm * timeinfo = localtime(&currentTime); // Convert UNIX time to struct tm
    
    Serial.print("Received packet at: ");
    // Print current time in 24-hour format
    char timeString[20];
    strftime(timeString, sizeof(timeString), "%Y-%m-%d %H:%M:%S", timeinfo);
    Serial.println(timeString);
    
    // Read packet
    // Request format: @UID
    // Data format: &data#UID
    
    while (LoRa.available()) {
      String payload = LoRa.readString();

      int pos1 = payload.indexOf("#");
      String requestUID = payload.substring(1, payload.length());
      
      Serial.print("From: ");
      Serial.println(requestUID);
      Serial.println("");
      Serial.println(payload); 
      Serial.println("");

      if (String(payload[0]) == "@") {
        Serial.println("Setup request received");
        epochTime = getTime();
        Serial.print("Epoch time: ");
        Serial.println(epochTime);

        // Outbound format: ?requestUID%sleepInterval
        String(outbound) = "?" + String(requestUID) + "%" + String(sleepInterval);
      
        delay(2000);
      
        Serial.print("Current outbound String: ");
        Serial.println(outbound);
        
        LoRa.beginPacket();
        LoRa.print(outbound);
        LoRa.endPacket();
      
        Serial.println("Outbound package sent");
        Serial.println("------------------------------------------------");
      }

      else if (String(payload[0]) == "&") {
        // Read data from string
        // Format "&data#UID
        int pos1 = payload.indexOf("#");
    
        distance = payload.substring(1, pos1);
        String MAC = payload.substring(pos1+1, payload.length());

        Serial.print("Data received from: ");
        Serial.println(MAC);
        Serial.print("Measured distance is: ");
        Serial.println(distance);
        Serial.println("");
      
        // POST this to the HTTP connection
        if (WiFi.status() == WL_CONNECTED) {
          HTTPClient http;
    
          http.begin(httpDestination); // Specify destination for HTTP request
          http.addHeader("Content-Type", "application/json"); // Specify content-type header
    
          const size_t CAPACITY = JSON_OBJECT_SIZE(1);
          StaticJsonDocument<CAPACITY> doc;
    
          JsonObject object = doc.to<JsonObject>();
          // Read from incoming
          object["MAC"] = MAC;
          object["distance"] = distance;

          // Extrapolated locally
          object["rssi"] = LoRa.packetRssi();
    
          serializeJson(doc, jsonOutput);
          
          int httpResponseCode = http.POST(String(jsonOutput)); // Actual POST request
    
          String jsonResponse = http.getString();       // Get response and print in Serial
          
          deserializeJson(doc, jsonResponse);
          
          int sleepInterval = doc["sleepInterval"];
          
          Serial.print("httpResponseCode: ");
          Serial.println(httpResponseCode);
          Serial.print("Json Response: ");
          Serial.println(jsonResponse);
          Serial.print("Sleep interval set to: ");
          Serial.println(sleepInterval);
        
          http.end();   // Ends HTTP to free resources
          Serial.println("HTTP communication ended");
          Serial.println("------------------------------------------------");
        }
        
        else {
          Serial.println("Error in WiFi connection");
          }
      }

      else if (String(payload[0]) == "?") {Serial.println("Other gateway packet received, be cautious of interference");}
      else {Serial.println("Erroneous packet received");}
    }
  }
}
