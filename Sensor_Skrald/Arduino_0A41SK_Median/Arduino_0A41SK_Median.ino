#define pin 2

const int NUM_MEASUREMENTS = 1000; // Number of measurements
const float OUTLIER_THRESHOLD = 3.0; // Threshold for outlier detection
double measurements[NUM_MEASUREMENTS];

// Function prototype
double get_IR(uint16_t value);

void setup() {
    Serial.begin(115200);
    pinMode(pin, INPUT);
}

void loop() {
    // Collect distance measurements
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        uint16_t value = analogRead(pin);
        double distance = get_IR(value); // Convert the analog voltage to the distance
        measurements[i] = distance * 1000; // Store distance in millimeters
        delay(5); // Delay between measurements to stabilize sensor
    }

    // Sort measurements
    qsort(measurements, NUM_MEASUREMENTS, sizeof(double), [](const void *a, const void *b) {
        double arg1 = *static_cast<const double*>(a);
        double arg2 = *static_cast<const double*>(b);
        return (arg1 > arg2) - (arg1 < arg2);
    });

    // Calculate median
    double median;
    if (NUM_MEASUREMENTS % 2 == 0) {
        median = (measurements[NUM_MEASUREMENTS / 2 - 1] + measurements[NUM_MEASUREMENTS / 2]) / 2.0;
    } else {
        median = measurements[NUM_MEASUREMENTS / 2];
    }

    // Print the median
    Serial.print("Median: ");
    Serial.println(median/10);
    Serial.println(" mm");
}

// Function to convert analog value to distance
double get_IR(uint16_t value) {
    return 2076.0 / value;
}
