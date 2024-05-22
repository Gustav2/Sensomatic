// Include
#include "Adafruit_VL53L1X.h"
#include <math.h>

// Set pins
#define IRQ_PIN 18
#define XSHUT_PIN 19

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);

// Define the number of measurements
const int NUM_MEASUREMENTS = 1000;
// Adjust this threshold as needed
const float OUTLIER_THRESHOLD = 3.0;

void setup() {
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
}

void loop() {
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

    // Calculate mean
    float sum = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
      sum += measurements[i];
    }
    float mean = sum / NUM_MEASUREMENTS;

    // Calculate standard deviation
    float sumSquaredDiffs = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
      sumSquaredDiffs += pow(measurements[i] - mean, 2);
    }
    float variance = sumSquaredDiffs / NUM_MEASUREMENTS;
    float standardDeviation = sqrt(variance);

    // Remove outliers
    int validMeasurements = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
      if (fabs(measurements[i] - mean) <= OUTLIER_THRESHOLD * standardDeviation) {
        measurements[validMeasurements++] = measurements[i];
      }
    }

    // Recalculate mean after removing outliers
    sum = 0;
    for (int i = 0; i < validMeasurements; i++) {
      sum += measurements[i];
    }
    mean = sum / validMeasurements;

    // Print the mean after removing outliers
    Serial.print(F("Mean after removing outliers: "));
    Serial.println(mean);
    Serial.println(F("mm"));

    vl53.clearInterrupt();
  }
}
