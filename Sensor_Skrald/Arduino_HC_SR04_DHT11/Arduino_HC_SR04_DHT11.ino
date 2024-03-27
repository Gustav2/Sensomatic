
#include <NewPing.h>  // https://bitbucket.org/teckel12/arduino-new-ping/wiki/Home
#include "DHT.h"

#define TRIGGER_PIN  18
#define ECHO_PIN     19
#define MAX_DISTANCE 400
#define DHTPIN 3     // Digital pin connected to the DHT sensor

#define DHTTYPE DHT11   // DHT 11

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
DHT dht(DHTPIN, DHTTYPE);

int readDHT, temp, hum;
float speedOfSound, distance, duration;

void setup() {
  Serial.begin(115200);

  dht.begin();

}

void loop() {
  delay(100);

  // Read temperature and humidity from DHT22 sensor
float temp = dht.readTemperature(); // Gets the values of the temperature
 float hum = dht.readHumidity(); // Gets the values of the humidity


  speedOfSound = 331.4 + (0.6 * temp) + (0.0124 * hum); // Calculate speed of sound in m/s

  duration = sonar.ping_median(10); // 10 interations - returns duration in microseconds
  duration = duration/1000000; // Convert mircroseconds to seconds
  distance = (speedOfSound * duration)/2;
  distance = distance * 100; // meters to centimeters

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println("cm");

}