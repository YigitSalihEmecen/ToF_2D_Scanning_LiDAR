#include <Wire.h>
#include <TFLI2C.h>

// === Pin Config ===
const int hallPin = 2;
const int motorPin1 = 9;
const int motorPin2 = 10;

// === RPM Calculation ===
volatile unsigned long lastPulseTime = 0;
volatile unsigned long pulseInterval = 0;
volatile bool newRPMReady = false;
const unsigned long debounceMicros = 100000; // 100ms = 600 RPM max

// === TF-Luna I2C ===
TFLI2C tflI2C;
int16_t tfDist;
const int16_t tfAddr = TFL_DEF_ADR; // 0x10

// === Set TF-Luna Frame Rate (e.g., 240 Hz) ===
void setTFMiniFrameRate(uint16_t rateHz) {
  Wire.beginTransmission(tfAddr);
  Wire.write(0x5A);                     // Header
  Wire.write(0x06);                     // Length
  Wire.write(0x03);                     // Set frame rate command
  Wire.write(rateHz & 0xFF);           // LSB
  Wire.write((rateHz >> 8) & 0xFF);    // MSB
  Wire.endTransmission();
}

void setup() {
  //TCCR1B = TCCR1B & 0b11111000 | 0x01;  // Set prescaler to 1

  Serial.begin(115200);
  Wire.begin();

  delay(100); // Let TF-Luna boot
  setTFMiniFrameRate(240);  // Set TF-Luna to 240 Hz
  delay(50);                // Let command apply

  // Motor setup
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  analogWrite(motorPin1, 120);  // PWM
  digitalWrite(motorPin2, LOW); // Direction

  // Hall sensor setup
  pinMode(hallPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(hallPin), onHallChange, CHANGE);
}

void loop() {
  // === Send distance constantly ===
  if (tflI2C.getData(tfDist, tfAddr)) {
    if (tfDist > 0 && tfDist < 800) {
      Serial.print("D:");
      Serial.println(tfDist);
    }
  }

  // === Send RPM when ready ===
  if (newRPMReady) {
    newRPMReady = false;

    float rpm = 0;
    if (pulseInterval > 0) {
      rpm = 60.0 * 1000000.0 / pulseInterval;
    }

    Serial.print("R:");
    Serial.println(rpm, 1);
  }

  delay(1); // Prevent spamming Serial buffer
}

// === Hall Sensor ISR ===
void onHallChange() {
  unsigned long now = micros();
  static unsigned long lastTriggerTime = 0;

  if (digitalRead(hallPin) == LOW && (now - lastTriggerTime > debounceMicros)) {
    pulseInterval = now - lastPulseTime;
    lastPulseTime = now;
    newRPMReady = true;
    lastTriggerTime = now;
  }
}
