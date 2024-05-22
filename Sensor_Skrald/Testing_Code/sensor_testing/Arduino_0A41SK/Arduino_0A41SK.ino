#define pin 2

const int NUM_MEASUREMENTS = 1000; // Number of measurements
const float OUTLIER_THRESHOLD = 3.0; // Threshold for outlier detection
double distances[NUM_MEASUREMENTS];

void setup () {
    Serial.begin (115200);
    pinMode(pin, INPUT);
}

void loop () {
    // Array to store distance measurements
    double measurements[NUM_MEASUREMENTS];

    // Collect distance measurements
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        uint16_t value = analogRead (pin);
        double distance = get_IR (value); // Convert the analog voltage to the distance
        measurements[i] = distance * 1000; // Store distance in millimeters
        delay(5); // Delay between measurements to stabilize sensor
    }

    // Calculate mean
    double sum = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        sum += measurements[i];
    }
    double mean = sum / NUM_MEASUREMENTS;

    // Calculate standard deviation
    double sumSquaredDiffs = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        sumSquaredDiffs += pow(measurements[i] - mean, 2);
    }
    double variance = sumSquaredDiffs / NUM_MEASUREMENTS;
    double standardDeviation = sqrt(variance);

    // Remove outliers
    int validMeasurements = 0;
    double sumWithoutOutliers = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        if (fabs(measurements[i] - mean) <= OUTLIER_THRESHOLD * standardDeviation) {
            validMeasurements++;
            sumWithoutOutliers += measurements[i];
        }
    }

    // Calculate mean after removing outliers
    mean = sumWithoutOutliers / validMeasurements;

    Serial.print("Mean after removing outliers: ");
    Serial.print(mean);
    Serial.println(" mm");
}

// Function to convert analog value to distance (mm)
double get_IR (uint16_t value) {
    return 2076.0 / (value);
}
