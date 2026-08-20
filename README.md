# 🌱 AI-Powered Smart Irrigation System

> **An IoT + Machine Learning based autonomous irrigation platform that combines real-time environmental sensing, weather forecasting, predictive intelligence, and automated pump control.**

[![ESP32](https://img.shields.io/badge/Hardware-ESP32-blue?logo=espressif)](https://www.espressif.com/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/UI-Tailwind%20CSS-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

The **AI-Powered Smart Irrigation System** is a closed-loop agricultural automation system designed to make irrigation decisions using a combination of **real-time field measurements and short-term weather forecasts**.

An ESP32 edge node continuously collects:

- 🌡️ Temperature
- 💧 Relative humidity
- 🌱 Soil moisture

The telemetry is transmitted to a Python/Flask processing server, where it is combined with weather information such as:

- 🌧️ Forecast rainfall
- ☔ Rain probability
- 🌡️ Forecast temperature
- 💦 Forecast humidity

A **Random Forest Classifier** processes these seven features and produces an irrigation recommendation.

The final decision is then returned to the ESP32, which controls an **active-LOW relay and water pump**.

```text
                   🌱 SMART IRRIGATION SYSTEM
                              │
                              ▼
                     ┌─────────────────┐
                     │  Field Sensors  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │      ESP32      │
                     │   Edge Node     │
                     └────────┬────────┘
                              │
                       HTTP Telemetry
                              │
                              ▼
                     ┌─────────────────┐
                     │ Flask Backend   │
                     └────────┬────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
      ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
      │   Weather   │  │   SQLite    │  │ Random Forest│
      │     API     │  │  Database   │  │     Model    │
      └──────┬──────┘  └─────────────┘  └───────┬──────┘
             │                                   │
             └────────────────┬──────────────────┘
                              ▼
                     ┌─────────────────┐
                     │ Decision Engine │
                     └────────┬────────┘
                              │
                        Relay Command
                              │
                              ▼
                     ┌─────────────────┐
                     │ Water Pump      │
                     └────────┬────────┘
                              │
                              ▼
                           🌱 Soil
                              │
                              └───────────↺
```

---

# ✨ Key Features

- 📡 **Real-time IoT sensing** using ESP32
- 🌡️ Temperature and humidity monitoring
- 🌱 Analog soil-moisture measurement
- 🌦️ Weather forecast integration
- 🤖 Random Forest based irrigation prediction
- 🔄 Closed-loop automated control
- 💾 Persistent SQLite telemetry storage
- 📊 Live web dashboard
- 🎛️ Manual `AUTO / FORCE ON / FORCE OFF` control
- 🛡️ Weather API fallback handling
- 🧯 ML model failure safety logic
- ⚡ Active-LOW relay control
- 🔌 Pump power isolation
- 📝 AI decision explanation
- ⏱️ Background maintenance using APScheduler
- 🔔 Optional field-health notifications through Ntfy.sh

---

# 🏗️ System Architecture

The project is organized into four primary operational layers:

```text
┌───────────────────────────────────────────────────────────────┐
│                     EDGE HARDWARE                             │
│                                                               │
│ ESP32 + DHT11 + Soil Moisture Sensor + Relay + Pump          │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            │ HTTP POST
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                     PROCESSING LAYER                          │
│                                                               │
│ Flask + Data Fusion + Decision Engine + API Routing          │
└──────────────┬────────────────┬────────────────┬─────────────┘
               │                │                │
               ▼                ▼                ▼
        Weather API          SQLite       Random Forest
               │                │                │
               └────────────────┼────────────────┘
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                        │
│                                                               │
│       Tailwind CSS + JavaScript Live Dashboard                │
└───────────────────────────────────────────────────────────────┘
```

Detailed architecture documentation is available in:

```text
docs/architecture/system-architecture.md
```

---

# 🔄 End-to-End Data Flow

The system follows a five-stage control cycle:

```text
1. Sampling
      ↓
2. Ingestion
      ↓
3. Weather Fusion
      ↓
4. ML Inference
      ↓
5. Actuation
      ↓
Next Sensor Cycle
      ↺
```

## 1. Sampling

The ESP32 reads:

```text
Temperature
Humidity
Soil Moisture
```

at a configurable interval, typically around **3–5 seconds**.

---

## 2. Ingestion

The ESP32 constructs a JSON payload and sends it to:

```http
POST /api/telemetry
```

Example:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7
}
```

---

## 3. Weather Fusion

The Flask backend obtains forecast information using the configured field coordinates.

The weather data is combined with the ESP32 measurements.

```text
ESP32 Data
    +
Weather Forecast
    ↓
Feature Vector
```

---

## 4. ML Inference

The Random Forest receives:

```text
[
    temperature,
    humidity,
    soil_moisture,
    rainfall,
    rain_probability,
    forecast_temperature,
    forecast_humidity
]
```

The model returns:

```text
0 → Irrigation not required
1 → Irrigation required
```

---

## 5. Actuation

The backend applies:

```text
ML Prediction
      +
Manual Override
      +
Safety Logic
      ↓
Final Relay State
```

The result is returned to the ESP32.

```text
relay = true
    ↓
GPIO 26 = LOW
    ↓
Relay ON
    ↓
Pump ON
```

---

# 🧠 Machine Learning

## Model

The current system uses:

```text
RandomForestClassifier
```

from Scikit-Learn.

The model uses seven input features:

| Feature | Source | Unit |
|---|---|---|
| `temperature` | DHT11 | °C |
| `humidity` | DHT11 | % |
| `soil_moisture` | Soil Sensor | % |
| `rainfall` | Weather API | mm |
| `rain_probability` | Weather API | % |
| `forecast_temperature` | Weather API | °C |
| `forecast_humidity` | Weather API | % |

The model output is:

```text
0 → OFF
1 → ON
```

### Model Artifact

```text
irrigation_model.pkl
```

The trained model is serialized using `joblib`.

For development, the backend can automatically generate a model when the expected model artifact is missing.

> **Important:** A generated/synthetic training dataset is suitable for testing the software pipeline but should not be considered a validated agricultural model. Production deployment should use properly labeled real-world field data.

Detailed documentation:

```text
machine-learning/model.md
machine-learning/features.md
```

---

# 🔌 Hardware

## Main Components

| Component | Purpose |
|---|---|
| ESP32 Dev Module | Edge controller |
| DHT11 | Temperature and humidity |
| Analog Soil Sensor | Soil moisture |
| 5V Relay Module | Pump switching |
| Water Pump | Irrigation actuator |

---

## ESP32 Pinout

| ESP32 Pin | Component | Function |
|---|---|---|
| GPIO 4 | DHT11 | Temperature/Humidity DATA |
| GPIO 34 | Soil Sensor | Analog input |
| GPIO 26 | Relay | Pump control |
| 3.3V | Sensors | Sensor supply where supported |
| GND | Sensors/Relay | Low-voltage ground |

### Relay Logic

The relay is **active-LOW**:

```text
GPIO 26 = LOW
    ↓
Relay ON
    ↓
Pump ON
```

```text
GPIO 26 = HIGH
    ↓
Relay OFF
    ↓
Pump OFF
```

The pump should use a suitable external power supply.

> ⚠️ Do not connect a pump directly to an ESP32 GPIO. For mains-powered equipment, use appropriately rated switching hardware, protection, isolation, enclosure, and qualified installation.

Hardware documentation:

```text
hardware/circuit-diagram.md
hardware/sensor-connections.md
hardware/pinout.md
```

---

# 🗄️ Database

The current implementation uses:

```text
SQLite
```

Database:

```text
telemetry.db
```

The main telemetry table stores:

```text
id
timestamp
temperature
humidity
soil_moisture
rainfall
rain_probability
forecast_temperature
forecast_humidity
relay_status
ai_suggestion
```

Example record:

```text
Temperature       → 28.4 °C
Humidity          → 72.1 %
Soil Moisture     → 34.7 %
Rainfall          → 1.2 mm
Rain Probability  → 60 %
Forecast Temp     → 27.9 °C
Forecast Humidity → 75 %
Relay Status      → OFF
AI Suggestion     → Irrigation not required
```

---

# 🌐 REST API

## Telemetry

```http
POST /api/telemetry
```

Receives sensor data from the ESP32.

Example:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7
}
```

Response:

```json
{
  "relay": false
}
```

---

## Dashboard

```http
GET /api/dashboard/latest
```

Returns the latest system state.

Example:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7,
  "rainfall": 1.2,
  "rain_probability": 60,
  "forecast_temperature": 27.9,
  "forecast_humidity": 75,
  "relay_status": false,
  "ai_suggestion": "Irrigation not required"
}
```

---

## Manual Override

```http
POST /api/dashboard/override
```

Supported modes:

```text
AUTO
FORCE_ON
FORCE_OFF
```

Example:

```json
{
  "mode": "FORCE_ON"
}
```

---

# 🎛️ Control Modes

The system supports three operating modes.

## AUTO

```text
Sensor Data
     +
Weather
     ↓
Random Forest
     ↓
Relay Decision
```

---

## FORCE ON

The pump is manually forced ON.

```text
FORCE_ON
    ↓
Relay ON
    ↓
Pump ON
```

---

## FORCE OFF

The pump is manually forced OFF.

```text
FORCE_OFF
     ↓
Relay OFF
     ↓
Pump OFF
```

Manual control takes precedence over the automatic ML decision until the system is returned to `AUTO`.

---

# 🛡️ Reliability & Fail-Safe Design

The system contains multiple fallback mechanisms.

## Weather API Failure

If the weather API becomes unavailable, the backend can use configured fallback values:

```text
Forecast Temperature = 25 °C
Forecast Humidity    = 50 %
Rain Probability     = 0 %
Rainfall             = 0 mm
```

The failure should also be logged.

---

## ML Model Failure

If the model cannot be loaded or inference fails, a deterministic safety rule can be used.

Example:

```text
IF soil_moisture < 30%
    → Pump ON
ELSE
    → Pump OFF
```

This is a fallback mechanism rather than a substitute for a properly trained production model.

---

## Hardware Failure

The relay uses a normally-open configuration so that loss of ESP32 power can cause the pump circuit to default to an open state.

```text
ESP32 Power Loss
       ↓
Relay De-energized
       ↓
NO Contact Open
       ↓
Pump OFF
```

---

# 📊 Live Dashboard

The frontend is designed as a single-page monitoring dashboard.

Technologies:

```text
HTML
CSS
JavaScript
Tailwind CSS
Font Awesome 6
```

The browser periodically requests:

```http
GET /api/dashboard/latest
```

approximately every **3 seconds**.

The dashboard can display:

- Current temperature
- Current humidity
- Soil moisture
- Rainfall
- Rain probability
- Forecast temperature
- Forecast humidity
- Pump state
- AI recommendation
- Control mode
- System status

---

# 📁 Repository Structure

```text
smart-irrigation/
│
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── backend/
│   ├── app.py
│   │
│   ├── models/
│   │   └── telemetry.py
│   │
│   ├── services/
│   │   ├── weather_service.py
│   │   ├── ml_service.py
│   │   └── irrigation_service.py
│   │
│   ├── scheduler/
│   │   └── tasks.py
│   │
│   ├── ml/
│   │   ├── train.py
│   │   ├── dataset_generator.py
│   │   └── irrigation_model.pkl
│   │
│   └── database/
│       └── telemetry.db
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
│
├── esp32/
│   ├── src/
│   │   ├── main.ino
│   │   ├── config.h
│   │   ├── sensors.h
│   │   ├── sensors.cpp
│   │   ├── network.h
│   │   └── network.cpp
│   │
│   └── config/
│       └── config.example.h
│
├── machine-learning/
│   ├── model.md
│   └── features.md
│
├── hardware/
│   ├── circuit-diagram.md
│   ├── sensor-connections.md
│   └── pinout.md
│
├── docs/
│   └── architecture/
│       ├── system-architecture.md
│       ├── data-flow.md
│       └── control-flow.md
│
├── tests/
│   ├── test_api.py
│   ├── test_ml.py
│   └── test_irrigation.py
│
└── scripts/
    ├── init_database.py
    └── train_model.py
```

---

# ⚙️ Technology Stack

## Hardware

```text
ESP32
DHT11
Analog Soil Moisture Sensor
5V Relay
Water Pump
```

## Backend

```text
Python
Flask
SQLAlchemy
APScheduler
Requests
Joblib
Scikit-Learn
```

## Machine Learning

```text
Random Forest Classifier
Scikit-Learn
Joblib
```

## Database

```text
SQLite
```

## Frontend

```text
HTML
CSS
JavaScript
Tailwind CSS
Font Awesome
```

## External Services

```text
OpenWeatherMap
Ntfy.sh
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd smart-irrigation
```

---

# 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Configure Environment Variables

Copy:

```bash
cp .env.example .env
```

Configure the required values.

Example:

```env
OPENWEATHER_API_KEY=your_api_key
FIELD_LAT=your_latitude
FIELD_LON=your_longitude

DATABASE_URL=sqlite:///telemetry.db

SECRET_KEY=change_this_secret
```

Do **not** commit `.env` to Git.

---

# 5. Initialize the Database

Run the project's database initialization script if provided:

```bash
python scripts/init_database.py
```

---

# 6. Start the Backend

```bash
python backend/app.py
```

The Flask server should start on the configured local host/port.

Typical development URL:

```text
http://127.0.0.1:5000
```

---

# 7. Open the Dashboard

Open the frontend through the configured Flask route or local development server.

The dashboard should display:

```text
Sensor Data
Weather Data
AI Recommendation
Pump State
Control Mode
```

---

# 🔌 ESP32 Setup

Configure the ESP32 using:

```text
esp32/config/config.example.h
```

Create your local configuration:

```text
esp32/config/config.h
```

Configure:

```text
Wi-Fi SSID
Wi-Fi Password
Backend URL
API endpoint
GPIO assignments
```

Example pin configuration:

```cpp
#define DHT_PIN       4
#define SOIL_PIN      34
#define RELAY_PIN     26
```

Upload the firmware to the ESP32.

---

# 🧪 Testing the System

A recommended testing order is:

```text
1. Test DHT11
       ↓
2. Test soil sensor
       ↓
3. Test ESP32 Wi-Fi
       ↓
4. Test Flask API
       ↓
5. Test database insertion
       ↓
6. Test weather API
       ↓
7. Test ML inference
       ↓
8. Test relay
       ↓
9. Test dashboard
       ↓
10. Test complete closed-loop operation
```

Start with the pump disconnected and verify the relay logic before connecting the complete actuator circuit.

---

# 📈 Model Development

The ML development workflow is:

```text
Collect Data
     ↓
Clean Data
     ↓
Create Labels
     ↓
Feature Engineering
     ↓
Train Model
     ↓
Validate Model
     ↓
Evaluate Metrics
     ↓
Serialize Model
     ↓
Deploy
```

Recommended evaluation metrics:

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

For agricultural deployment, also evaluate the practical consequences of false positives and false negatives.

---

# 🔬 Research & Development Direction

This project can evolve into a more advanced research platform.

Potential future directions include:

### Predictive Soil Moisture

```text
Current Conditions
       ↓
Time-Series Model
       ↓
Future Soil Moisture
```

### Multi-Zone Irrigation

```text
ESP32 Zone 1 ─┐
ESP32 Zone 2 ─┤
ESP32 Zone 3 ─┼──→ Central Processing
ESP32 Zone 4 ─┘
```

### Edge AI

```text
ESP32
  ↓
Local ML Inference
  ↓
Immediate Control

        +
        
Cloud/Local Server
  ↓
Analytics + Dashboard
```

### Physics-Informed Irrigation

Future versions can incorporate:

- Evapotranspiration
- Soil-water balance
- Crop coefficients
- Root-zone moisture
- Solar radiation
- Wind speed
- Vapor pressure deficit

---

# 🌍 Sustainability

The system is designed around the principle:

> **Irrigate when the field requires water, not simply when a fixed timer says it is time.**

By combining field measurements with forecast information, the system can potentially reduce:

- Unnecessary water consumption
- Unnecessary pump operation
- Energy consumption
- Manual irrigation effort

Actual water savings should be measured experimentally rather than assumed.

---

# ⚠️ Safety Notes

This project controls physical equipment.

Before deploying the system:

- Verify sensor voltage compatibility.
- Verify ESP32 GPIO voltage limits.
- Use an appropriately rated relay.
- Use a separate suitable supply for the pump.
- Do not power the pump directly from the ESP32.
- Use appropriate protection for inductive loads.
- Keep hazardous-voltage wiring isolated from low-voltage electronics.
- Use an enclosure for outdoor deployment.
- Protect electronics from water and condensation.
- Use appropriate fuses and circuit protection.
- Follow local electrical safety requirements.

For mains-powered pumps, use qualified electrical installation practices.

---

# 📚 Documentation

Detailed documentation is organized under:

```text
docs/
hardware/
machine-learning/
```

Important documents:

```text
docs/architecture/system-architecture.md
hardware/circuit-diagram.md
machine-learning/model.md
machine-learning/features.md
```

---

# 🗺️ Development Roadmap

## Phase 1 — Hardware

- [x] ESP32 integration
- [x] DHT11 integration
- [x] Soil moisture sensing
- [x] Relay control
- [ ] Outdoor enclosure
- [ ] Long-term power solution

## Phase 2 — Backend

- [x] Flask API
- [x] Telemetry ingestion
- [x] SQLite storage
- [x] Weather integration
- [ ] Authentication
- [ ] HTTPS deployment

## Phase 3 — Machine Learning

- [x] Random Forest pipeline
- [x] Feature vector
- [x] Model serialization
- [x] Fallback model logic
- [ ] Real field dataset
- [ ] Hyperparameter optimization
- [ ] Model versioning
- [ ] Automated retraining

## Phase 4 — Dashboard

- [x] Live telemetry
- [x] Pump status
- [x] AI recommendation
- [x] Manual override
- [ ] Historical charts
- [ ] Model confidence visualization
- [ ] Alert center

## Phase 5 — Advanced System

- [ ] MQTT
- [ ] Multiple ESP32 nodes
- [ ] Multi-zone irrigation
- [ ] Predictive soil moisture
- [ ] Edge ML
- [ ] Crop-specific models
- [ ] Physics-informed features
- [ ] Automated model lifecycle

---

# 🤝 Contributing

Contributions are welcome.

A typical workflow is:

```bash
git checkout -b feature/your-feature
```

Make your changes, test them, and then:

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Open a pull request describing:

- What changed
- Why it changed
- How it was tested
- Any hardware requirements
- Any database/model changes

---

# 📄 License

This project is intended to be released under the **Apache 2.0 License**.

See:

```text
LICENSE
```

for the complete license text.

---

# 👨‍💻 Author

**Jyotipriya Sarkar**

Electronics Engineering | Microelectronics & VLSI | IoT | Machine Learning

- GitHub: `https://github.com/jyotipriyasarkar119-hue`
- LinkedIn: `https://www.linkedin.com/in/jyotipriya-sarkar`

---

