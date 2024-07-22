#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const char* ssid     = "";
const char* password = "";

WiFiUDP udp;
unsigned int localUdpPort = ;  // Local port to listen on

char incomingPacket[255];  // Buffer for incoming packets

const int greenLEDPin = 2; // GPIO pin for LED
const int buzzerPin = 4;   // GPIO pin for Buzzer

// Initialize the LCD with I2C address 0x27 and 16x2 size
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("connected");

  udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  pinMode(greenLEDPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(greenLEDPin, LOW); // Turn off the LED initially
  digitalWrite(buzzerPin, LOW);   // Turn off the Buzzer initially

  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Waiting for data");
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    digitalWrite(greenLEDPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
    delay(500);
    digitalWrite(greenLEDPin, LOW);
    digitalWrite(buzzerPin, LOW);
    delay(500);
    digitalWrite(greenLEDPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
    delay(500);
    digitalWrite(greenLEDPin, LOW);
    digitalWrite(buzzerPin, LOW);
    delay(500);
    digitalWrite(greenLEDPin, HIGH);
    digitalWrite(buzzerPin, HIGH);

    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0; // Null-terminate the string

      // Check if the incoming packet contains recommended crop
      if (strncmp(incomingPacket, "RECOMMENDED:", 12) == 0) {
        // Print recommended crop to serial monitor
        Serial.printf("RECOMMENDED CROP: %s\n", incomingPacket + 12);
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Recommended:");
        lcd.setCursor(0, 1);
        lcd.print(incomingPacket + 12);
      }
      else {
        // Convert incoming packet to a number for comparison
        float yieldValue = atof(incomingPacket);

        // Clear the LCD before writing new data
        lcd.clear();

        if (yieldValue > 500) {
          // If yieldValue is more than 500, print in kg/Hectare
          Serial.printf("PREDICTED YIELD OF CROP IS: %s kg/Hectare\n", incomingPacket);
          lcd.setCursor(0, 0);
          lcd.print("Yield:");
          lcd.setCursor(0, 1);
          lcd.print(incomingPacket);
          lcd.print(" kg/H");
        } else {
          // If yieldValue is less than or equal to 500, print in Tonne/Hectare
          Serial.printf("PREDICTED YIELD OF CROP IS: %s Tonne/Hectare\n", incomingPacket);
          lcd.setCursor(0, 0);
          lcd.print("Yield:");
          lcd.setCursor(0, 1);
          lcd.print(incomingPacket);
          lcd.print(" T/H");
        }
      }
    }

    delay(1000); // Delay between receiving packets
    digitalWrite(greenLEDPin, LOW); // Turn off the LED
    digitalWrite(buzzerPin, LOW);   // Turn off the Buzzer
  }

  delay(10); // Small delay to avoid overwhelming the processor
}
