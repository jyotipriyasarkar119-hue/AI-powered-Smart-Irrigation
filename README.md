# 🌱 AI-Powered Smart Irrigation System

> An IoT + Machine Learning based autonomous irrigation platform that combines real-time environmental sensing, weather forecasting, predictive intelligence, and automated pump control.

[![Hardware](https://img.shields.io/badge/Hardware-ESP32-blue?logo=espressif)](https://www.espressif.com/)
[![Backend](https://img.shields.io/badge/Backend-Flask-black?logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python)](https://www.python.org/)
[![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

---

## 📌 Overview

The **AI-Powered Smart Irrigation System** is a closed-loop agricultural automation project that combines edge sensing, weather intelligence, machine learning, a backend processing layer, persistent telemetry storage, and automated pump control.

An ESP32 sensing node collects:

- 🌡️ Temperature
- 💧 Relative humidity
- 🌱 Soil moisture

The backend combines this telemetry with forecast information such as:

- 🌧️ Rainfall
- ☔ Rain probability
- 🌡️ Forecast temperature
- 💦 Forecast humidity

A **Random Forest Classifier** uses these seven features to produce an irrigation recommendation. The final command is returned to the ESP32, which drives an **active-LOW relay** controlling the irrigation pump.

```text
                         🌱 SMART IRRIGATION SYSTEM

 ┌──────────────────────┐
 │   FIELD SENSORS      │
 │  DHT11 + Soil Sensor │
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │        ESP32         │
 │      Edge Node       │
 └──────────┬───────────┘
            │ HTTP Telemetry
            ▼
 ┌──────────────────────────────┐
 │       FLASK BACKEND          │
 │ Ingestion + Fusion + Control │
 └──────────────┬───────────────┘
                │
        ┌───────┼────────┬──────────┐
        │       │        │          │
        ▼       ▼        ▼          ▼
   Weather   SQLite   Random     Dashboard
     API    Database   Forest      APIs
        │       │        │          │
        └───────┴────────┴──────────┘
                │
                ▼
       ┌──────────────────┐
       │ Decision Engine  │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Relay / Pump     │
       └────────┬─────────┘
                │
                ▼
             🌱 SOIL
                │
                └───────────────↺
```

---

## ✨ Key Features

- 📡 Real-time IoT sensing with ESP32
- 🌡️ Temperature and humidity monitoring using DHT11
- 🌱 Analog soil-moisture monitoring
- 🌦️ External weather forecast integration
- 🤖 Random Forest irrigation classification
- 🔄 Closed-loop automated irrigation
- 💾 SQLite telemetry storage
- 📊 Live browser dashboard
- 🎛️ `AUTO`, `FORCE_ON`, and `FORCE_OFF` control modes
- 🛡️ Weather API fallback handling
- 🧯 ML inference fallback safety logic
- ⚡ Active-LOW relay control
- 🔌 Separate pump power path
- 📝 Human-readable AI decision suggestion
- ⏱️ Background task support with APScheduler
- 🔔 Optional notifications through Ntfy.sh

---

# 🏗️ System Architecture

The system is organized into four functional layers.

```text
┌────────────────────────────────────────────────────────────────────┐
│                         EDGE / HARDWARE                            │
│                                                                    │
│ ESP32 + DHT11 + Soil Moisture Sensor + Relay + Pump               │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                │ HTTP POST
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                         BACKEND / PROCESSING                      │
│                                                                    │
│ Flask API + Data Fusion + Decision Logic + Database Interface    │
└──────────────────────┬───────────────────────┬─────────────────────┘
                       │                       │
                       ▼                       ▼
                ┌─────────────┐        ┌──────────────┐
                │ Weather API │        │ ML / Dataset │
                └──────┬──────┘        └──────┬───────┘
                       │                      │
                       └──────────┬───────────┘
                                  ▼
                         ┌─────────────────┐
                         │ SQLite Storage  │
                         └────────┬────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                        FRONTEND / DASHBOARD                       │
│                                                                    │
│                    HTML + JavaScript UI                           │
└────────────────────────────────────────────────────────────────────┘
```

Detailed system documentation is available in [`docs/system-architecture.md`](docs/system-architecture.md).

---

# 🔄 End-to-End Data Flow

```text
1. Sensor Sampling
       ↓
2. ESP32 Telemetry
       ↓
3. Flask Ingestion
       ↓
4. Weather Data Fusion
       ↓
5. Random Forest Inference
       ↓
6. Manual Override / Safety Logic
       ↓
7. Relay Command
       ↓
8. Pump Actuation
       ↓
9. Telemetry Persistence
       ↓
10. Next Cycle ↺
```

The ESP32 typically samples the environment every few seconds, constructs a JSON payload, and posts it to the backend.

Example telemetry:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7
}
```

The backend enriches the request with weather data and creates the seven-feature ML input:

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

---

# 🤖 Machine Learning

## Model

The current ML pipeline uses:

```text
RandomForestClassifier
```

with the following features:

| Feature | Source | Unit |
|---|---|---|
| `temperature` | DHT11 | °C |
| `humidity` | DHT11 | % |
| `soil_moisture` | Soil sensor | % |
| `rainfall` | Weather API | mm |
| `rain_probability` | Weather API | % |
| `forecast_temperature` | Weather API | °C |
| `forecast_humidity` | Weather API | % |

Output:

```text
0 → Irrigation not required
1 → Irrigation required
```

The ML research/development material currently lives under [`ML/`](ML/), including:

- [`ML/README.md`](ML/README.md)
- [`ML/notebooks/Smart_Irrigation.ipynb`](ML/notebooks/Smart_Irrigation.ipynb)
- [`ML/rice_irrigation_dataset_v2.csv`](ML/rice_irrigation_dataset_v2.csv)

> **Important:** Training-data quality directly affects model reliability. A development dataset or synthetic labels should not be treated as a field-validated irrigation policy without appropriate agronomic validation.

---

# 🔌 Hardware

## Main Components

| Component | Purpose |
|---|---|
| ESP32 Dev Module | Edge controller and Wi-Fi node |
| DHT11 | Temperature and relative humidity |
| Analog soil-moisture sensor | Soil moisture measurement |
| 5V active-LOW relay | Pump switching |
| Water pump | Irrigation actuator |

## Current ESP32 Pin Mapping

| ESP32 Pin | Component | Function |
|---|---|---|
| GPIO 4 | DHT11 | Temperature / humidity data |
| GPIO 34 | Soil sensor | Analog input |
| GPIO 26 | Relay | Pump control |

Relay logic:

```text
GPIO 26 = LOW  → Relay ON  → Pump ON
GPIO 26 = HIGH → Relay OFF → Pump OFF
```

The pump should be powered from an appropriately rated external supply. Do not drive the pump directly from an ESP32 GPIO.

Hardware documentation is currently maintained in [`docs/circuit-diagram.md`](docs/circuit-diagram.md).

> ⚠️ For mains-powered pumps, use suitable isolation, switching hardware, protection, enclosure, wiring, and qualified electrical installation practices.

---

# 🗄️ Data Storage

The backend uses SQLite for local telemetry persistence.

The logical telemetry record contains fields for:

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

The database file is intentionally treated as runtime data and should not be committed as a source artifact.

---

# 🌐 Backend

The backend entry point currently present in the repository is:

```text
backend/app.py
```

A backend overview is available at [`backend/README.md`](backend/README.md).

The Flask server is responsible for:

- Receiving ESP32 telemetry
- Validating and processing input data
- Calling the weather service
- Constructing ML features
- Running irrigation inference
- Applying manual overrides
- Persisting telemetry
- Serving dashboard data

Conceptual endpoints used by the system include:

```http
POST /api/telemetry
GET  /api/dashboard/latest
POST /api/dashboard/override
```

The exact endpoint behavior should be treated as defined by the current implementation in `backend/app.py`.

---

# 🌐 Frontend

The live dashboard source is maintained under [`frontend/`](frontend/).

Current repository files include:

```text
frontend/
├── README.md
├── index.html
└── assets/
    └── Screenshot From 2026-08-21 01-05-32.png
```

The dashboard is intended to present current telemetry, weather information, AI recommendations, pump state, and manual controls.

Frontend documentation: [`frontend/README.md`](frontend/README.md)

---

# 📡 Firmware

The ESP32 firmware is maintained under [`firmware/`](firmware/).

The current repository contains the source at:

```text
firmware/ esp32/Source_Code.ino
```

> **Note:** The current directory name contains a leading space (`"firmware/ esp32"`). This README intentionally reflects the repository as it exists today rather than inventing a different path.

The firmware is responsible for:

1. Initializing the sensors
2. Connecting to Wi-Fi
3. Sampling environmental data
4. Sending telemetry to the backend
5. Receiving the relay decision
6. Driving GPIO 26
7. Repeating the control cycle

---

# 📚 Documentation

The current documentation tree is:

```text
docs/
├── circuit-diagram.md
├── machine_learning_model.md
└── system-architecture.md
```

Recommended entry points:

- [System Architecture](docs/system-architecture.md)
- [Circuit Diagram](docs/circuit-diagram.md)
- [Machine Learning Model](docs/machine_learning_model.md)

---

# 📁 Repository Structure

This is the repository structure currently present on the `main` branch:

```text
AI-powered-Smart-Irrigation/
│
├── .gitignore
├── LICENSE
├── README.md
│
├── ML/
│   ├── README.md
│   ├── notebooks/
│   │   └── Smart_Irrigation.ipynb
│   └── rice_irrigation_dataset_v2.csv
│
├── backend/
│   ├── README.md
│   └── app.py
│
├── docs/
│   ├── circuit-diagram.md
│   ├── machine_learning_model.md
│   └── system-architecture.md
│
├── firmware/
│   └──  esp32/
│       └── Source_Code.ino
│
└── frontend/
    ├── README.md
    ├── index.html
    └── assets/
        └── Screenshot From 2026-08-21 01-05-32.png
```

> GitHub currently reports the firmware directory as `firmware/ esp32` with a leading space. Renaming that directory to `firmware/esp32` would make the structure cleaner, but this README does not assume that change has been made.

---

# ⚙️ Local Development

## 1. Clone the repository

```bash
git clone https://github.com/jyotipriyasarkar119-hue/AI-powered-Smart-Irrigation.git
cd AI-powered-Smart-Irrigation
```

## 2. Backend environment

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project's Python dependencies using the dependency specification used by your current backend setup.

> The repository root currently does not contain a `requirements.txt` file, so the README does not prescribe a dependency file that is not present in the repository.

## 3. Environment variables

Keep API keys, Wi-Fi credentials, and other secrets outside source control.

Typical configuration includes:

```text
OPENWEATHER_API_KEY
FIELD_LAT
FIELD_LON
DATABASE_URL
SECRET_KEY
```

Use your actual backend configuration rather than committing credentials to Git.

## 4. Start the backend

The current backend entry point is:

```bash
python backend/app.py
```

The exact runtime URL and configuration are determined by the current Flask application.

## 5. Program the ESP32

Open:

```text
firmware/ esp32/Source_Code.ino
```

Configure the board's Wi-Fi and backend settings as required by the source code, then flash the firmware using the Arduino IDE or another compatible ESP32 development environment.

---

# 🧪 Testing Strategy

A practical testing sequence is:

```text
1. Test DHT11 readings
        ↓
2. Test soil-moisture ADC readings
        ↓
3. Test ESP32 Wi-Fi connectivity
        ↓
4. Test Flask telemetry ingestion
        ↓
5. Verify SQLite persistence
        ↓
6. Verify weather-data retrieval
        ↓
7. Verify ML inference
        ↓
8. Test relay without the pump connected
        ↓
9. Test the pump power circuit safely
        ↓
10. Run the complete closed loop
```

Always verify relay behavior before connecting a high-power actuator.

---

# 🛡️ Reliability and Safety

The control architecture includes several fallback concepts:

### Weather API Failure

Use a defined fallback state when external forecast data is unavailable, and log that fallback condition.

### ML Failure

If model inference is unavailable, use a deterministic safety rule rather than allowing an undefined actuator state.

### Manual Override

`FORCE_ON` and `FORCE_OFF` are intended to take priority over automatic inference until the controller returns to `AUTO`.

### Power Loss

A normally-open relay path can help keep the pump off when the controller loses power, assuming the relay and pump circuit are wired accordingly.

---

# 🌍 Sustainability Goal

The core objective is to move irrigation from a fixed-timer approach toward a data-driven control strategy:

```text
Current Field Conditions
          +
Weather Forecast
          +
Machine Learning
          ↓
Context-Aware Irrigation
```

The project is intended to reduce unnecessary irrigation and pump operation while maintaining responsive control to changing environmental conditions. Actual water and energy savings should be measured experimentally.

---

# 🚀 Future Development

Potential extensions include:

- MQTT-based telemetry
- Multiple ESP32 sensor nodes
- Zone-based irrigation
- Historical analytics and charts
- Real-field model retraining
- Soil-moisture forecasting
- Crop-specific models
- Physics-informed irrigation features
- Edge ML inference
- PostgreSQL / time-series storage
- Secure authentication and HTTPS
- Automated model evaluation and deployment

---

# 🤝 Contributing

Contributions, bug reports, and documentation improvements are welcome.

Before submitting changes:

1. Keep secrets and local runtime data out of Git.
2. Test hardware-facing changes carefully.
3. Document API or database changes.
4. Document ML feature changes and retraining requirements.
5. Update the relevant documentation under `docs/`.

---

# 📜 License

Copyright © 2026 Jyotipriya Sarkar

This project is licensed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE) for the full license text.

```text
Apache-2.0
```

---

# 👨‍💻 Author

**Jyotipriya Sarkar**

Electronics Engineering | Microelectronics & VLSI | IoT | Machine Learning

- GitHub: https://github.com/jyotipriyasarkar119-hue
- LinkedIn: https://www.linkedin.com/in/jyotipriya-sarkar

---

## ⭐ Core Principle

```text
SENSE → FUSE → PREDICT → DECIDE → ACT → OBSERVE → REPEAT
```

The system turns environmental sensing and weather information into an automated irrigation decision while keeping the architecture modular enough for future research and real-world agricultural deployment.
