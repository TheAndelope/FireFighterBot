#include <BluetoothSerial.h>

// Initialize Bluetooth serial
BluetoothSerial SerialBT;

// Define flame sensor data pins (example)
const int flameSensorPin = A0;

// Function to get the current state
String getCurrentState() {
  int frontDistance = analogRead(A1); // Replace with actual sonar logic
  int leftDistance = analogRead(A2);  // Replace with actual sonar logic
  int rightDistance = analogRead(A3); // Replace with actual sonar logic
  int flameSensorAngle = 90;          // Example angle
  int flameDetected = (analogRead(flameSensorPin) < 300) ? 1 : 0;

  return String(frontDistance) + "," + 
         String(leftDistance) + "," + 
         String(rightDistance) + "," + 
         String(flameSensorAngle) + "," + 
         String(flameDetected);
}

void setup() {
  SerialBT.begin("FirefighterBot"); // Name for Bluetooth device
  Serial.begin(115200);
  Serial.println("Bluetooth Started. Waiting for pairing...");
}

void loop() {
  // Get the current state and send to the laptop
  String state = getCurrentState();
  SerialBT.println(state);
  Serial.println("State sent: " + state);

  // Wait for action from the laptop
  while (!SerialBT.available()) {
    delay(10); // Avoid hogging CPU
  }

  String action = SerialBT.readStringUntil('\n');
  action.trim(); // Remove any extra whitespace
  Serial.println("Action received: " + action);

  // Execute the action
  int actionID = action.toInt();
  switch (actionID) {
    case 0: moveForward(); break;
    case 1: turnLeft(); break;
    case 2: turnRight(); break;
    case 3: rotateFlameSensorLeft(); break;
    case 4: rotateFlameSensorRight(); break;
    default: Serial.println("Unknown action!"); break;
  }
}

// Example movement functions
void moveForward() { Serial.println("Moving forward"); }
void turnLeft() { Serial.println("Turning left"); }
void turnRight() { Serial.println("Turning right"); }
void rotateFlameSensorLeft() { Serial.println("Rotating flame sensor left"); }
void rotateFlameSensorRight() { Serial.println("Rotating flame sensor right"); }
