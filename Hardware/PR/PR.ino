#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "DIXIT";
const char* password = "12345678";
const char* serverAddress = "192.168.1.48";

int sensorValue = 0;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");  
  }

  Serial.println("Connected to WiFi");

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  delay(1000);

  int sensorValue = analogRead(A0);
  sendCounterValue(sensorValue);
}

void sendCounterValue(int value) {
  HTTPClient http;
  WiFiClient client;
  http.begin(client, serverAddress, 5000);
  http.addHeader("Content-Type", "application/json");

  // Create JSON payload
  String payload = "{\"value\": " + String(value) + "}";

  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}
