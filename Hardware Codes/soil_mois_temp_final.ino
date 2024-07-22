#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

// Moisture sensor setup
#define moistureSensor A0
#define wet 210
#define dry 510

// DS18B20 setup
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// LCD setup (adjust address if needed)
LiquidCrystal_I2C lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

SoftwareSerial espSerial(0, 1); // RX, TX

void setup() {
  Serial.begin(9600);
  sensors.begin();

  espSerial.begin(9600); // Start software serial at 9600 baud

  delay(1000);
}

void loop() {
  // Reading soil moisture
  int moistureValue = analogRead(moistureSensor);
  
  // Map the moisture value to a percentage
  int moisturePercent = map(moistureValue, wet, dry, 100, 0);
  Serial.print("Moisture Percentage: ");
  Serial.print(moisturePercent);
  Serial.println("%");

  // Reading temperature from DS18B20
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);
  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.println(" °C");

  // Send data to ESP32
  espSerial.print(moisturePercent);
  espSerial.print(",");
  espSerial.println(temperatureC);

  delay(1000);

  delay(1000);
}
