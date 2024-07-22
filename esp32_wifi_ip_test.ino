#include <WiFi.h>


const char* ssid     = "";
const char* password = "";

void setup() {
  Serial.begin(9600);
  delay(10);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected.");
  
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {

}
