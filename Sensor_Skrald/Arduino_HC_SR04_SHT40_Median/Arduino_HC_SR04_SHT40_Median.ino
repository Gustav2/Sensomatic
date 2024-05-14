#include <NewPing.h>
#include "Adafruit_SHT4x.h"

Adafruit_SHT4x sht4 = Adafruit_SHT4x();

#define TRIGGER_PIN  18
#define ECHO_PIN     19
#define MAX_DISTANCE 400

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

// Define the number of measurements
const int NUM_MEASUREMENTS = 1000;

void setup() {
  Serial.begin(115200);

  while (!Serial)
    delay(10);     

  Serial.println("Adafruit SHT4x test");
  if (!sht4.begin()) {
    Serial.println("Couldn't find SHT4x");
    while (1) delay(1);
  }
  Serial.println("Found SHT4x sensor");
  Serial.print("Serial number 0x");
  Serial.println(sht4.readSerial(), HEX);

  sht4.setPrecision(SHT4X_HIGH_PRECISION);
  switch (sht4.getPrecision()) {
     case SHT4X_HIGH_PRECISION: 
       Serial.println("High precision");
       break;
     case SHT4X_MED_PRECISION: 
       Serial.println("Med precision");
       break;
     case SHT4X_LOW_PRECISION: 
       Serial.println("Low precision");
       break;
  }

  sht4.setHeater(SHT4X_NO_HEATER);
  switch (sht4.getHeater()) {
     case SHT4X_NO_HEATER: 
       Serial.println("No heater");
       break;
     case SHT4X_HIGH_HEATER_1S: 
       Serial.println("High heat for 1 second");
       break;
     case SHT4X_HIGH_HEATER_100MS: 
       Serial.println("High heat for 0.1 second");
       break;
     case SHT4X_MED_HEATER_1S: 
       Serial.println("Medium heat for 1 second");
       break;
     case SHT4X_MED_HEATER_100MS: 
       Serial.println("Medium heat for 0.1 second");
       break;
     case SHT4X_LOW_HEATER_1S: 
       Serial.println("Low heat for 1 second");
       break;
     case SHT4X_LOW_HEATER_100MS: 
       Serial.println("Low heat for 0.1 second");
       break;
  }
}

void loop() {
  delay(100);
  sensors_event_t humidity, temperature;
  
  uint32_t timestamp = millis();
  sht4.getEvent(&humidity, &temperature);
  timestamp = millis() - timestamp;

  float t = temperature.temperature;
  float h = humidity.relative_humidity;

  float speedOfSound = 331.4 + (0.6 * t) + (0.0124 * h);
  
  float duration = sonar.ping_median(10) / 1000000.0; // microseconds to seconds
  float distance = (speedOfSound * duration) / 2 * 100; // meters to centimeters

  if (distance == -1) {
    Serial.println("Couldn't get distance");
    return;
  }

  // Array to store distance measurements
  float measurements[NUM_MEASUREMENTS];

  // Store distance measurements in array
  for (int i = 0; i < NUM_MEASUREMENTS; i++) {
    measurements[i] = distance;
  }

  // Sort measurements
  std::sort(measurements, measurements + NUM_MEASUREMENTS);

  // Calculate median
  float median;
  if (NUM_MEASUREMENTS % 2 == 0) {
    median = (measurements[NUM_MEASUREMENTS / 2 - 1] + measurements[NUM_MEASUREMENTS / 2]) / 2.0;
  } else {
    median = measurements[NUM_MEASUREMENTS / 2];
  }

  // Print the median
  Serial.print("Median: ");
  Serial.println(median*10); // Convert median from meters to millimeters
  Serial.println(" mm");
}
