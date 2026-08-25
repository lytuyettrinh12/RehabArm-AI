/*
 * RehabArm AI - ESP32 Firmware
 * 
 * Hardware Pin Connections:
 * - AD8232 sEMG Output -> GPIO 36 (VP / Analog ADC1_CH0)
 * - MPU6050 SDA         -> GPIO 21
 * - MPU6050 SCL         -> GPIO 22
 * - Servo SG90 Signal   -> GPIO 4
 */

#include <Wire.h>
#include <ESP32Servo.h>

// Pin Definitions
#define SEMG_PIN 36
#define SERVO_PIN 4

// MPU6050 I2C Address
#define MPU6050_ADDR 0x68

Servo tensionServo;

// Variables
int semgValue = 0;
int16_t ax, ay, az, gx, gy, gz;

void setupMPU6050() {
  Wire.begin(21, 22);
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0);    // Wake up MPU6050
  Wire.endTransmission(true);
}

void readMPU6050() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B); // Starting register for Accel Data
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 14, true);

  ax = Wire.read() << 8 | Wire.read();
  ay = Wire.read() << 8 | Wire.read();
  az = Wire.read() << 8 | Wire.read();
  Wire.read(); Wire.read(); // Skip temperature
  gx = Wire.read() << 8 | Wire.read();
  gy = Wire.read() << 8 | Wire.read();
  gz = Wire.read() << 8 | Wire.read();
}

void setup() {
  Serial.begin(115200);
  
  // Attach Servo
  tensionServo.attach(SERVO_PIN);
  tensionServo.write(0); // Initial position: Normal tension (0 degrees)

  // Dedicated Power Pins for MPU6050 (Allowing 1-to-1 direct wiring)
  pinMode(19, OUTPUT);
  digitalWrite(19, HIGH); // GPIO 19 outputs 3.3V VCC
  pinMode(18, OUTPUT);
  digitalWrite(18, LOW);  // GPIO 18 acts as GND
  delay(100);

  // Initialize Sensors
  pinMode(SEMG_PIN, INPUT);
  setupMPU6050();
}

void loop() {
  // 1. Read sEMG Analog Value
  semgValue = analogRead(SEMG_PIN);

  // 2. Read IMU MPU6050 Data
  readMPU6050();

  // 3. Stream data as CSV over Serial
  // Format: sEMG,Ax,Ay,Az,Gx,Gy,Gz
  Serial.print(semgValue); Serial.print(",");
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.println(gz);

  // 4. Check for incoming control commands from PC (Intel OpenVINO decision)
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "STOP" || command == "FATIGUE") {
      tensionServo.write(90); // Rotate Servo to 90 deg -> Release strap tension
    } else if (command == "RESET" || command == "NORMAL") {
      tensionServo.write(0);  // Reset Servo to 0 deg -> Apply normal tension
    }
  }

  delay(10); // ~100Hz sampling rate
}
