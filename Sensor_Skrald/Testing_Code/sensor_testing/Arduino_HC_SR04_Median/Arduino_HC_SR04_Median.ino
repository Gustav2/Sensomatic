// Define pins numbers
const int trigPin = 18;
const int echoPin = 19;

// Define variables
const int NUM_MEASUREMENTS = 1000; // Number of measurements
const float OUTLIER_THRESHOLD = 3.0; // Threshold for outlier detection
long duration;
float distances[NUM_MEASUREMENTS];

void setup() {
  pinMode(trigPin, OUTPUT); // Set the trigPin as an Output
  pinMode(echoPin, INPUT);  // Set the echoPin as an Input
  Serial.begin(115200);     // Start the serial communication
}

void loop() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Set the trigPin on HIGH state for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  float distance = duration * 0.034 / 2; // Speed of sound in air is approximately 0.034 cm/µs
  
  // Store the distance in the array
  static int measurements_count = 0;
  if (measurements_count < NUM_MEASUREMENTS) {
    distances[measurements_count++] = distance;
  } else {
    // Sort distances
    std::sort(distances, distances + NUM_MEASUREMENTS);

    // Calculate median
    float median;
    if (NUM_MEASUREMENTS % 2 == 0) {
      median = (distances[NUM_MEASUREMENTS / 2 - 1] + distances[NUM_MEASUREMENTS / 2]) / 2.0;
    } else {
      median = distances[NUM_MEASUREMENTS / 2];
    }

    // Print the median
    Serial.print("Median: ");
    Serial.println(median*10);
    Serial.println(" mm");

    // Reset measurements count for next iteration
    measurements_count = 0;
  }

  delay(100); // Delay before taking next measurement
}
