// Include required libraries
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <SPI.h>
#include <LoRa.h>

// Define the pins used by the LoRa module
const int csPin = 0;     // LoRa radio chip select
const int resetPin = 1;  // LoRa radio reset
const int irqPin = 2;    // Must be a hardware interrupt pin

// Information for WiFi connection
const char* ssid = "Sensomatic";
const char* password = "password12!";

// Variables for sensor data storage
String msgCount;
String temperature;
String humidity;

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
  // 433E6 for Asia
  // 866E6 for Europe
  // 915E6 for North America
 
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1)
      ;
  }
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
      // payload format: msgCount#temperature/humidity
      // String example: 45#20.94/47.22
      Serial.print(payload); 

      // Read data from string
      int pos1 = payload.indexOf("#");
      int pos2 = payload.indexOf("/");

      msgCount = payload.substring(0, pos1);
      temperature = payload.substring(pos1 + 1, pos2);
      humidity = payload.substring(pos2 + 1, payload.length());
    }
  
    // POST this to the HTTP connection
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      http.begin("http://192.168.0.102:8000/datacollector/handle_post/"); // Specify destination for HTTP request
      http.addHeader("Content-Type", "application/json"); // Specify content-type header

      const size_t CAPACITY = JSON_OBJECT_SIZE(1);
      StaticJsonDocument<CAPACITY> doc;

      JsonObject object = doc.to<JsonObject>();
      object["sensor"] = "termometer";
      object["temperature"] = temperature;
      object["humidity"] = humidity;
      object["message count"] = msgCount;

      serializeJson(doc, jsonOutput);
      

      int httpResponseCode = http.POST(String(jsonOutput)); // Actual POST request

        
      String response = http.getString();       // Get response and print in Serial
      Serial.println(httpResponseCode);
      Serial.println(response);
    
      http.end();   // Ends HTTP to free resources
    
    }
    else {
      Serial.println("Error in WiFi connection");
      }

    // NO DELAY IN THIS CODE
    // Delay is currently implemented on the individual sensor transmission. 
    // The gateway relays the LoRa data to the server as fast as possible
      
    }
 }