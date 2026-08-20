#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// --- DHT11 CONFIGURATION ---
#define DHTPIN 4         // GPIO pin connected to DHT11 DATA
#define DHTTYPE DHT11    // DHT 11
DHT dht(DHTPIN, DHTTYPE);

// --- NETWORK & BACKEND CONFIGURATION ---
const char* WIFI_SSID = "Your_Wifi";
const char* WIFI_PASSWORD = "Your_Wifi_Name";
const char* SERVER_URL = "http://10.30.102.xx.xxxx/api/telemetry";

// --- HARDWARE & RELAY CONFIGURATION ---
#define RELAY_PIN 26          // Relay Module IN pin
#define SOIL_PIN 34           // Soil Moisture Analog Pin (ADC1)
#define RELAY_ACTIVE_LOW false // Set 'true' for Active-LOW relays (most common), 'false' for Active-HIGH

// Sampling Interval (10 seconds)
const unsigned long POST_INTERVAL_MS = 10000; 
unsigned long lastPostTime = 0;

// Helper function to handle inverted or standard relay logic
void setRelayState(bool turnOn) {
  if (RELAY_ACTIVE_LOW) {
    digitalWrite(RELAY_PIN, turnOn ? LOW : HIGH);
  } else {
    digitalWrite(RELAY_PIN, turnOn ? HIGH : LOW);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n====================================");
  Serial.println("   SMART IRRIGATION ESP32 NODE      ");
  Serial.println("====================================");

  // Configure Relay Pin and ensure default state is OFF on startup
  pinMode(RELAY_PIN, OUTPUT);
  setRelayState(false);

  // Initialize DHT11 Sensor
  dht.begin();
  Serial.println("[STATUS] DHT11 Sensor Initialized!");

  // Connect to Wi-Fi
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n[STATUS] Wi-Fi Connected!");
  Serial.print("[INFO] ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("====================================\n");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - lastPostTime >= POST_INTERVAL_MS) {
    lastPostTime = currentMillis;

    if (WiFi.status() == WL_CONNECTED) {
      readSensorsAndSync();
    } else {
      Serial.println("[WARNING] Wi-Fi Lost! Reconnecting...");
      WiFi.reconnect();
    }
  }
}

void readSensorsAndSync() {
  // 1. READ SOIL MOISTURE
  int rawSoilVal = analogRead(SOIL_PIN);
  float soilMoisture = map(rawSoilVal, 4095, 1500, 0, 100); 
  soilMoisture = constrain(soilMoisture, 0.0, 100.0);

  // 2. READ DHT11 TEMP & HUMIDITY
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if readings failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("[ERROR] Failed to read from DHT11 sensor!");
    temperature = 0.0;
    humidity = 0.0;
  }

  // --- PRINT TO SERIAL MONITOR ---
  Serial.println("---------- [SENSOR READINGS] ----------");
  Serial.printf("Raw Soil ADC  : %d\n", rawSoilVal);
  Serial.printf("Soil Moisture : %.1f %%\n", soilMoisture);
  Serial.printf("Temperature   : %.1f °C\n", temperature);
  Serial.printf("Humidity      : %.1f %%\n", humidity);
  Serial.println("---------------------------------------");

  // 3. BUILD & SEND JSON PAYLOAD
  JsonDocument doc;
  doc["soil_moisture"] = soilMoisture;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(5000);

  Serial.println("[HTTP] Sending telemetry...");
  int httpCode = http.POST(jsonPayload);

  // 4. HANDLE RESPONSE & PUMP CONTROL
  if (httpCode == HTTP_CODE_OK || httpCode == 200) {
    String responseString = http.getString();
    Serial.println("[RX Response]: " + responseString);

    JsonDocument responseDoc;
    DeserializationError err = deserializeJson(responseDoc, responseString);

    if (!err) {
      bool relayState = responseDoc["relay"]; 
      
      // Update hardware relay state
      setRelayState(relayState);

      Serial.println("---------- [PUMP ACTION] ----------");
      Serial.printf("Target Relay State : %s\n", relayState ? "ON" : "OFF");
      Serial.printf("Physical Pin %d    : %s\n", RELAY_PIN, 
        (digitalRead(RELAY_PIN) == HIGH) ? "HIGH" : "LOW");
      Serial.println("====================================\n");
    } else {
      Serial.print("[ERROR] Failed to parse JSON response: ");
      Serial.println(err.f_str());
    }
  } else {
    Serial.printf("[HTTP ERROR] Code: %d\n\n", httpCode);
  }

  http.end();
}
