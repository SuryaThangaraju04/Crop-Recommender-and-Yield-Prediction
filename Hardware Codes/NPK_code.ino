#include <SoftwareSerial.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define RE 8
#define DE 7

const byte nitro[] = {0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c};
const byte phos[] = {0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc};
const byte pota[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};

byte values[11];
SoftwareSerial mod(2,3); // RX, TX

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  mod.begin(9600);
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("NPK Monitor");
  delay(2000); // Show the initial message for 2 seconds
}

void loop() {
  byte val1, val2, val3;
  val1 = nitrogen();
  delay(250);
  val2 = phosphorous();
  delay(250);
  val3 = potassium();
  delay(250);

  // Send data in a formatted string
  Serial.print("N:");
  Serial.print(val1);
  Serial.print(",P:");
  Serial.print(val2);
  Serial.print(",K:");
  Serial.println(val3);

  // Send data to ESP32 via SoftwareSerial
  sendToESP32(val1, val2, val3);

  lcd.setCursor(0, 0);
  lcd.print("N:");
  lcd.print(val1);
  lcd.print(" P:");
  lcd.print(val2);
  lcd.print(" K:");
  lcd.print(val3);

  delay(2000); // Wait for 2 seconds before updating the values
}

byte nitrogen() {
  return requestValue(nitro);
}

byte phosphorous() {
  return requestValue(phos);
}

byte potassium() {
  return requestValue(pota);
}

byte requestValue(const byte *command) {
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(10);
  mod.write(command, sizeof(nitro));
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  delay(10); // Wait for response

  // Read the response
  for (byte i = 0; i < 7; i++) {
    if (mod.available()) {
      values[i] = mod.read();
    } else {
      values[i] = 0; // Default to 0 if no data
    }
  }
  return values[4]; // Value typically at this index
}

void sendToESP32(byte val1, byte val2, byte val3) {
  // Send data to ESP32 via SoftwareSerial
  mod.print("N:");
  mod.print(val1);
  mod.print(",P:");
  mod.print(val2);
  mod.print(",K:");
  mod.println(val3);
}
