# Backend Processing Node | AI-Powered Smart Irrigation System

The central REST API and orchestration engine for the AI-Powered Smart Irrigation System. Built with **Flask** and **SQLAlchemy**, this service ingests real-time telemetry from ESP32 edge nodes, enriches sensor data with live weather forecasts from OpenWeatherMap, executes predictive machine learning inference, and manages automated/manual hardware relay states.

---

## 🛠️ Technology Stack

* **Framework:** Flask (Python)
* **Database:** SQLite via Flask-SQLAlchemy
* **Machine Learning:** Scikit-Learn, Joblib, NumPy, Pandas
* **Task Scheduling:** APScheduler (Background Scheduler)
* **External Integrations:** OpenWeatherMap API (Weather Forecasts), Ntfy.sh (Push Notifications)

---

## ⚙️ Core Architecture & Features

1. **Telemetry Processing Pipeline (`/api/telemetry`):**
   * Receives real-time temperature, humidity, and soil moisture readings from the ESP32.
   * Fetches atmospheric forecasts (3-hour rain volume, rain probability, forecasted temp/humidity) via OpenWeatherMap.
   * Feeds the merged 7-feature payload into `irrigation_model.pkl`.
   * Determines active relay state based on model decision or manual override rules, returning the target hardware state to the ESP32.

2. **Automated ML Initialization:**
   * Automatically trains and serializes a `RandomForestClassifier` on startup if `irrigation_model.pkl` is missing.

3. **Dashboard & Control Interface (`/api/dashboard/*`):**
   * Exposes latest telemetry, AI decision explanations, and weather metrics to the frontend.
   * Accepts manual actuation overrides (`Force ON`, `Force OFF`, `Return to Auto`).

4. **Automated Weekly Field Health Summary:**
   * Background task scheduled via APScheduler that aggregates 7-day field telemetry metrics and broadcasts push notifications via Ntfy.sh.

## 🏗️ System Architecture & Data Pipeline

```text
+-------------------+      HTTP POST /api/telemetry     +-------------------+
|    ESP32 NODE     | --------------------------------> |   FLASK BACKEND   |
|  - DHT11 (GPIO 4) |                                   |     (Python)      |
|  - Soil (GPIO 34) | <-------------------------------- |                   |
|  - Relay (GPIO 26)|        JSON Relay Response        +---------+---------+
+-------------------+                                             |
                                                                  |
            +---------------------------------+-------------------+---------------------------------+
            |                                 |                                                     |
            v                                 v                                                     v
+-----------------------+         +-----------------------+                             +-----------------------+
|  OpenWeatherMap API   |         |   Random Forest ML    |                             |   Tailwind Dashboard  |
|  - 3-Hour Rain Vol    |         | (`irrigation_model`)  |                             |   - 3s Live Polling   |
|  - Rain Probability   |         |  - 7 Feature Vector   |                             |   - Telemetry Visuals |
|  - Forecast Temp/Hum  |         |  - Binary Inference   |                             |   - Manual Override   |
+-----------------------+         +-----------------------+                             +-----------------------+

```

## 📡 API Endpoints

### 1. Ingest Telemetry (ESP32 Node)
* **Endpoint:** `POST /api/telemetry`
* **Content-Type:** `application/json`
* **Request Payload:**
```json
{
  "temperature": 30.8,
  "humidity": 72.0,
  "soil_moisture": 35.5
}
