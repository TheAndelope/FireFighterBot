#include <LiquidCrystal_I2C.h>
#include <ESP32Servo.h> 
#include <Wire.h>

#define scl 22
#define sda 21
// Define pins for sensors
#define leftTrigPin 18
#define leftEchoPin 19
#define rightTrigPin 33
#define rightEchoPin 32
#define frontTrigPin 15
#define frontEchoPin 2
#define flameSensorPin 13
#define leftLineSensor 36
#define rightLineSensor 39
// Define motor encoder pins

#define leftEncoderA 27
#define leftEncoderB 26
#define rightEncoderA 17
#define rightEncoderB 16

// Flame threshold
#define flameThreshold 300

Servo flameSensorServo;

LiquidCrystal_I2C lcd(0x27, 16, 2);

int flameSensorAngle = 90; // Starts at 90 degrees (facing forward)
const float wheelCircumference = 20.0;
const int ppr = 1024; // Pulses per revolution

volatile int leftEncoderCount = 0;
volatile int rightEncoderCount = 0;

void IRAM_ATTR handleLeftEncoderA() {
  if (digitalRead(leftEncoderA) == HIGH) {
    if (digitalRead(leftEncoderB) == LOW) {
      leftEncoderCount++;
    } else {
      leftEncoderCount--;
    }
  }
}

void IRAM_ATTR handleRightEncoderA() {
  if (digitalRead(rightEncoderA) == HIGH) {
    if (digitalRead(rightEncoderB) == LOW) {
      rightEncoderCount++;
    } else {
      rightEncoderCount--;
    }
  }
}

void setup() {
  pinMode(leftEchoPin, INPUT);
  pinMode(rightEchoPin, INPUT);
  pinMode(frontEchoPin, INPUT);
  pinMode(leftTrigPin, OUTPUT);
  pinMode(rightTrigPin, OUTPUT);
  pinMode(frontTrigPin, OUTPUT);

  pinMode(leftLineSensor, INPUT);
  pinMode(rightLineSensor, INPUT);

  pinMode(flameSensorPin, INPUT);

  pinMode(12, OUTPUT);

  pinMode(leftEncoderA, INPUT);
  pinMode(leftEncoderB, INPUT);
  pinMode(rightEncoderA, INPUT);
  pinMode(rightEncoderB, INPUT);

  
  attachInterrupt(digitalPinToInterrupt(leftEncoderA), handleLeftEncoderA, RISING);
  attachInterrupt(digitalPinToInterrupt(rightEncoderA), handleRightEncoderA, RISING);

  flameSensorServo.attach(12); // Servo connected to pin 12
  flameSensorServo.write(flameSensorAngle);

  lcd.init();
  lcd.clear();
  lcd.backlight();      // Make sure backlight is on

  // Print a message on both lines of the LCD.
  Serial.begin(115200);
  delay(500);
}

void loop() {
  
  int leftDistance = readSonar(leftTrigPin, leftEchoPin);
  int frontDistance = readSonar(frontTrigPin, frontEchoPin);
  int rightDistance = readSonar(rightTrigPin, rightEchoPin);
  int flameReading = analogRead(flameSensorPin);

  lcd.setCursor(0, 0);
  lcd.print(leftDistance);
  Serial.print("Left: ");
  Serial.println(leftDistance);
  /*
  lcd.setCursor(1, 0);
  lcd.print(frontDistance);
  Serial.println (frontDistance);
  */
  
  lcd.setCursor(0, 1);
  lcd.print(rightDistance);
  Serial.print("Right: ");
  Serial.println(rightDistance);
  // Check for flame
  
  /*
  if (flameReading < flameThreshold) {
    Serial.println("Flame detected!");
    extinguishFlame(leftDistance, rightDistance);
  }
  
  // Right-hand rule navigation
  if (frontDistance < 20) {
    // Obstacle ahead, turn right
    turnRight(90);
  } else if (rightDistance > 20) {
    // Follow right-hand wall
    moveForward(10); // Move forward 10 cm
  } else {
    // Adjust to stay close to the right wall
    turnLeft(90);
  }
  */
  
  delay(50);

}

int readSonar(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  long duration = pulseIn(echo, HIGH);
  int distance = duration * 0.034 / 2; // Convert to centimeters
  return distance;
}

void extinguishFlame(int leftDistance, int rightDistance) {
  stopMovement();

  // Determine turn direction based on available space
  if (leftDistance > rightDistance) {
    turnLeft(180);
  } else {
    turnRight(180);
  }

  Serial.println("Balloon deployed to extinguish flame.");
  delay(2000); // Simulate extinguishing time
}

void moveForward(float distance) {
  int targetPulses = (distance / wheelCircumference) * ppr;
  leftEncoderCount = 0;
  rightEncoderCount = 0;

  setMotorSpeeds(100, 100); // Move forward at full speed
  while (abs(leftEncoderCount) < targetPulses && abs(rightEncoderCount) < targetPulses) {
    // Wait until target distance is reached
  }
  stopMovement();
}

void turnLeft(int angle) {
  int targetPulses = (angle / 360.0) * (wheelCircumference / 8.5) * ppr;
  leftEncoderCount = 0;
  rightEncoderCount = 0;

  setMotorSpeeds(-100, 100); // Rotate left in place
  while (abs(leftEncoderCount) < targetPulses && abs(rightEncoderCount) < targetPulses) {
    // Wait until target angle is reached
  }
  stopMovement();
}

void turnRight(int angle) {
  int targetPulses = (angle / 360.0) * (wheelCircumference / 8.5) * ppr;
  leftEncoderCount = 0;
  rightEncoderCount = 0;

  setMotorSpeeds(100, -100); // Rotate right in place
  while (abs(leftEncoderCount) < targetPulses && abs(rightEncoderCount) < targetPulses) {
    // Wait until target angle is reached
  }
  stopMovement();
}

void stopMovement() {
  setMotorSpeeds(0, 0); // Stop both motors
}

void setMotorSpeeds(int leftSpeed, int rightSpeed) {
  
}
