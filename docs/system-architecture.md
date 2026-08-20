# 🏛️ System Architecture | AI-Powered Smart Irrigation System

This document describes the complete end-to-end technical architecture, component interactions, data-processing pipeline, machine-learning workflow, database structure, control logic, and reliability mechanisms of the **AI-Powered Smart Irrigation System**.

The system is designed as an autonomous, closed-loop irrigation platform that combines **IoT sensing, edge computing, weather forecasting, machine learning, persistent telemetry storage, and automated pump control**.

---

## 📑 Table of Contents

1. [System Overview](#-system-overview)
2. [High-Level Architecture](#-high-level-architecture)
3. [Architecture Layers](#-architecture-layers)
4. [Hardware & Edge Tier](#-hardware--edge-tier)
5. [Backend Engine](#-backend-engine)
6. [External API Tier](#-external-api-tier)
7. [Database Tier](#-database-tier)
8. [Machine Learning Tier](#-machine-learning-tier)
9. [Web Frontend Tier](#-web-frontend-tier)
10. [End-to-End Data Pipeline](#-end-to-end-data-pipeline)
11. [ML Feature Vector](#-machine-learning-feature-vector)
12. [Irrigation Decision Logic](#-irrigation-decision-logic)
13. [Manual Override System](#-manual-override-system)
14. [Database Schema](#-database-schema)
15. [API Architecture](#-api-architecture)
16. [Reliability & Fail-Safe Strategy](#-reliability--fail-safe-strategy)
17. [Control-Loop Sequence](#-control-loop-sequence)
18. [Software Component Architecture](#-software-component-architecture)
19. [Project Directory Structure](#-project-directory-structure)
20. [Security Considerations](#-security-considerations)
21. [Future Extensions](#-future-extensions)
22. [Conclusion](#-conclusion)

---

# 🌱 System Overview

The AI-Powered Smart Irrigation System is a **closed-loop cyber-physical system** designed to automatically determine whether agricultural irrigation is required.

The system combines:

- ESP32-based edge sensing
- Temperature and humidity monitoring
- Soil-moisture measurement
- Wi-Fi communication
- REST-based telemetry transmission
- Real-time weather forecast integration
- SQLite telemetry storage
- Random Forest machine-learning inference
- Automatic relay control
- Manual irrigation override
- Web-based live monitoring
- Fail-safe irrigation control

The fundamental operating principle is:

```text
Environmental Sensing
        ↓
Telemetry Transmission
        ↓
Weather Data Fusion
        ↓
Machine Learning Inference
        ↓
Irrigation Decision
        ↓
Relay Actuation
        ↓
Physical Irrigation
        ↓
Changed Environmental Conditions
        ↓
New Sensor Reading
        ↺
```

This creates a continuous feedback loop between the physical agricultural environment and the computational intelligence layer.

---

# 📊 High-Level Architecture

The complete system consists of five major logical tiers:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EDGE HARDWARE TIER                                  │
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────────────┐  │
│  │ DHT11 Sensor │    │ Soil Sensor  │    │ Active-LOW 5V Relay         │  │
│  └──────┬───────┘    └──────┬───────┘    └──────────────▲──────────────┘  │
│         │                   │                           │                  │
│         └───────────────────┼───────────────────────────┤                  │
│                             ▼                           │                  │
│                    ┌─────────────────┐                  │                  │
│                    │      ESP32      │──────────────────┘                  │
│                    │   Wi-Fi Node    │                                     │
│                    └────────┬────────┘                                     │
└─────────────────────────────┼───────────────────────────────────────────────┘
                              │
                              │ HTTP POST /api/telemetry
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND ENGINE                                      │
│                                                                             │
│                    ┌────────────────────────┐                               │
│                    │      Flask Server      │                               │
│                    │                        │                               │
│                    │ REST API               │                               │
│                    │ Data Fusion             │                               │
│                    │ Decision Orchestrator   │                               │
│                    │ Override Manager        │                               │
│                    └───────────┬────────────┘                               │
│                                │                                            │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────────┐
│ EXTERNAL API TIER  │ │   DATABASE TIER    │ │ MACHINE LEARNING TIER  │
│                    │ │                    │ │                        │
│ OpenWeatherMap     │ │ SQLite             │ │ Random Forest          │
│                    │ │ telemetry.db       │ │ Classifier             │
│ Forecast Data      │ │                    │ │                        │
└─────────┬──────────┘ └─────────▲──────────┘ └───────────┬────────────┘
          │                      │                        │
          └──────────────────────┼────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WEB FRONTEND TIER                                   │
│                                                                             │
│                    ┌────────────────────────┐                               │
│                    │ Live Web Dashboard     │                               │
│                    │                        │                               │
│                    │ Tailwind CSS           │                               │
│                    │ JavaScript             │                               │
│                    │ REST API Polling       │                               │
│                    │ Manual Control         │                               │
│                    └────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 🏗️ Architecture Layers

## Layer 1 — Edge Hardware

Responsible for:

- Environmental sensing
- ADC conversion
- Wi-Fi communication
- Receiving actuator commands
- Relay switching

Main components:

- ESP32
- DHT11
- Soil-moisture sensor
- Relay module
- Water pump

---

## Layer 2 — Backend Processing

Responsible for:

- Receiving telemetry
- Validating sensor data
- Obtaining weather information
- Combining local and forecast data
- Running ML inference
- Applying manual overrides
- Recording telemetry
- Returning actuator commands

Main technology:

```text
Python
Flask
SQLAlchemy
APScheduler
Requests
Joblib
Scikit-Learn
```

---

## Layer 3 — Data & Intelligence

This layer contains:

- SQLite database
- Weather forecast data
- ML model
- Feature engineering
- Prediction logic
- Historical telemetry

---

## Layer 4 — Presentation

The frontend provides:

- Live environmental readings
- Weather information
- Soil moisture status
- AI irrigation recommendation
- Pump status
- Manual controls
- System health information

---

## Layer 5 — Actuation

The final decision is converted into a physical control signal.

```text
AI Decision
     ↓
Final Relay State
     ↓
HTTP Response
     ↓
ESP32
     ↓
GPIO 26
     ↓
Relay
     ↓
Water Pump
```

---

# 🔌 Hardware & Edge Tier

The physical layer handles real-time environmental sampling and low-level hardware switching.

```text
┌───────────────────────┐
│       DHT11           │
│ Temperature/Humidity  │
└──────────┬────────────┘
           │ GPIO 4
           ▼
┌────────────────────────────────┐
│                                │
│             ESP32              │
│                                │
│       Wi-Fi Enabled Node       │
│                                │
└───────────────┬────────────────┘
                │
        GPIO 34 │
                ▼
┌────────────────────────┐
│ Soil Moisture Sensor   │
│ Analog Output          │
└────────────────────────┘

                GPIO 26
                   │
                   ▼
        ┌──────────────────┐
        │ 5V Active-LOW    │
        │ Relay Module     │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │   Water Pump     │
        └──────────────────┘
```

---

## ESP32 Microcontroller

The ESP32 acts as the central edge-computing node.

Responsibilities:

1. Initialize sensors.
2. Connect to Wi-Fi.
3. Read environmental measurements.
4. Convert soil sensor ADC values.
5. Construct telemetry JSON.
6. Send telemetry to Flask.
7. Receive the irrigation decision.
8. Control the relay.
9. Repeat the cycle continuously.

The ESP32 operates using a **2.4 GHz Wi-Fi network**.

---

# 🌡️ Sensor Subsystem

## DHT11 Sensor

The DHT11 provides:

- Ambient temperature
- Relative humidity

Connection:

```text
DHT11 DATA → ESP32 GPIO 4
```

Output:

```text
temperature → °C
humidity    → %
```

---

## Soil Moisture Sensor

The soil-moisture sensor provides an analog signal representing soil moisture.

Connection:

```text
Soil Sensor AO → ESP32 GPIO 34
```

The ESP32 ADC provides a 12-bit reading:

```text
ADC Range = 0–4095
```

The raw ADC measurement can be converted into a normalized moisture percentage using a calibration function.

Conceptually:

```text
Raw ADC
   ↓
Calibration
   ↓
Soil Moisture %
```

The exact conversion depends on the sensor and field calibration.

---

# ⚡ Actuation Subsystem

The irrigation actuator consists of:

```text
ESP32 GPIO 26
      ↓
5V Relay Module
      ↓
Water Pump
      ↓
Irrigation System
```

The relay is configured as **active-LOW**.

Therefore:

```text
GPIO 26 = LOW  → Relay ON  → Pump ON
GPIO 26 = HIGH → Relay OFF → Pump OFF
```

The relay provides electrical isolation between the ESP32 control circuitry and the pump circuit.

> **Important:** The pump's power circuit should be electrically isolated and designed according to the pump's voltage/current requirements. Mains-voltage wiring should use appropriate protection and qualified installation practices.

---

# 🔄 End-to-End Data Pipeline

Every control cycle follows the following lifecycle:

```text
┌──────────────────┐
│ 1. SENSOR READ   │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 2. DATA INGESTION│
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 3. WEATHER FUSION│
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 4. ML INFERENCE  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 5. ACTUATION     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ PHYSICAL PUMP    │
└────────┬─────────┘
         │
         └───────────────→ Next Sensor Cycle
```

---

# 1️⃣ Stage 1 — Edge Sampling

The ESP32 periodically samples:

```text
Temperature
Humidity
Soil Moisture
```

Recommended sampling interval:

```text
3–5 seconds
```

Example telemetry structure:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7
}
```

---

# 2️⃣ Stage 2 — Telemetry Ingestion

The ESP32 sends the sensor data to the Flask backend.

Endpoint:

```text
POST /api/telemetry
```

Conceptual request:

```http
POST /api/telemetry
Content-Type: application/json
```

Payload:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7
}
```

The Flask server receives and validates the payload.

---

# 3️⃣ Stage 3 — Weather Data Fusion

After receiving local sensor data, the backend requests forecast information from OpenWeatherMap.

The request uses the configured field coordinates:

```text
FIELD_LAT
FIELD_LON
```

Relevant forecast parameters include:

- Forecast temperature
- Forecast humidity
- Rain probability
- Rainfall volume

The backend combines local measurements and forecast information.

```text
ESP32 Data
    +
Weather API
    ↓
Feature Fusion
```

---

# 4️⃣ Stage 4 — Machine Learning Inference

The backend constructs the ML feature vector:

```text
X =
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

The trained Random Forest classifier evaluates the vector.

The prediction is:

```text
Y ∈ {0, 1}
```

where:

```text
Y = 1 → Irrigation required
Y = 0 → Irrigation not required
```

---

# 5️⃣ Stage 5 — Actuation

The final decision is determined by combining:

```text
ML Decision
     +
Manual Override State
     +
Safety Rules
```

The backend returns:

```json
{
  "relay": true
}
```

or:

```json
{
  "relay": false
}
```

The ESP32 translates this into the physical relay signal:

```text
relay = true
      ↓
GPIO 26 = LOW
      ↓
Relay ON
      ↓
Pump ON
```

and:

```text
relay = false
      ↓
GPIO 26 = HIGH
      ↓
Relay OFF
      ↓
Pump OFF
```

---

# 🧠 Machine Learning Feature Vector

The Random Forest classifier uses seven features.

Mathematically:

$$
\vec{X}
=
[
T,
H,
SM,
R,
P_r,
T_f,
H_f
]
$$

where:

| Feature | Description | Unit |
|---|---|---|
| `T` | Current temperature | °C |
| `H` | Current humidity | % |
| `SM` | Current soil moisture | % |
| `R` | Forecast rainfall | mm |
| `P_r` | Rain probability | % |
| `T_f` | Forecast temperature | °C |
| `H_f` | Forecast humidity | % |

The classifier generates:

$$
Y = f(\vec{X})
$$

where:

$$
Y \in \{0,1\}
$$

---

# 🌦️ Weather Data Fusion

The weather API extends the information available from local sensors.

Local sensing provides:

```text
Current field conditions
```

Weather forecasting provides:

```text
Expected future conditions
```

Combining both allows the irrigation system to reason about upcoming rainfall.

For example:

```text
Current Soil Moisture = Low
Current Temperature   = High
Rain Probability      = 90%
Expected Rainfall     = 8 mm
```

The system can determine that immediate irrigation may not be necessary because substantial rainfall is expected.

---

# 🧮 Irrigation Decision Logic

The decision pipeline can be represented as:

```text
              ┌────────────────────┐
              │ Current Telemetry  │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Weather Forecast   │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Feature Vector     │
              │      X[7]          │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Random Forest      │
              │ Classifier         │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Prediction Y       │
              │       0 / 1        │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Override Manager   │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Safety Layer       │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Final Relay State  │
              └────────────────────┘
```

---

# 🎛️ Manual Override System

The system provides three control modes:

```text
AUTO
FORCE ON
FORCE OFF
```

## AUTO

The Random Forest model determines the irrigation state.

```text
AUTO
 ↓
ML Prediction
 ↓
Relay Decision
```

---

## FORCE ON

The pump is forced ON regardless of the ML prediction.

```text
FORCE ON
   ↓
Relay = ON
```

---

## FORCE OFF

The pump is forced OFF regardless of the ML prediction.

```text
FORCE OFF
    ↓
Relay = OFF
```

The manual override takes precedence over the model decision until the system is returned to `AUTO`.

---

# 🖥️ Backend Engine

The Flask backend acts as the central orchestration layer.

Conceptually:

```text
                  ┌─────────────────────┐
                  │      Flask App      │
                  └──────────┬──────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ REST Routes  │     │ Data Fusion  │     │ ML Inference │
└──────────────┘     └──────────────┘     └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                     ┌──────────────┐
                     │ Decision     │
                     │ Orchestrator │
                     └──────────────┘
```

---

# 🧩 Flask Core Orchestrator

The main application is responsible for:

- REST API routing
- Telemetry ingestion
- Input validation
- Weather API communication
- Data normalization
- ML inference
- Relay decision generation
- Database persistence
- Manual override management
- Dashboard API responses

---

# 🔗 REST Routing Engine

The backend exposes endpoints for:

```text
ESP32 → Flask
Dashboard → Flask
Flask → ESP32
```

Core routes include:

```text
POST /api/telemetry
GET  /api/dashboard/latest
POST /api/dashboard/override
```

Additional health and configuration endpoints can be added as required.

---

# 🗄️ Database Interface

SQLAlchemy ORM is used as the database abstraction layer.

The database stores:

- Sensor measurements
- Weather information
- ML decision
- Relay state
- AI reasoning
- Timestamp

Database:

```text
SQLite
```

Database file:

```text
telemetry.db
```

---

# ⏱️ Background Scheduler

APScheduler can execute periodic maintenance tasks.

Potential scheduled tasks include:

```text
Weekly telemetry aggregation
Database maintenance
Field-health notifications
System-health checks
Data cleanup
```

Notifications can be delivered using Ntfy.sh.

---

# 🌐 External API Tier

The system integrates OpenWeatherMap to obtain forecast information.

Conceptual flow:

```text
Flask Backend
     │
     │ API Request
     ▼
OpenWeatherMap
     │
     │ Forecast Response
     ▼
Flask Backend
     │
     ▼
Feature Fusion
```

The weather layer provides:

- Forecast temperature
- Forecast humidity
- Rain probability
- Rainfall volume

The forecast information becomes part of the ML input.

---

# 🗃️ Database Tier

SQLite is used as the persistent telemetry store.

```text
Application
     │
     ▼
SQLAlchemy ORM
     │
     ▼
SQLite
     │
     ▼
telemetry.db
```

SQLite is appropriate for the current single-node/local processing architecture because it provides:

- Simple deployment
- Zero database server configuration
- Persistent storage
- SQL compatibility
- Low resource requirements

For large-scale deployments, the storage layer can later be migrated to PostgreSQL or another time-series database.

---

# 🤖 Machine Learning Tier

The machine-learning subsystem uses:

```text
Scikit-Learn
RandomForestClassifier
Joblib
```

Model file:

```text
irrigation_model.pkl
```

---

# 🌲 Random Forest Classifier

The classifier maps the seven environmental and weather features to an irrigation decision.

```text
7 Input Features
       ↓
Random Forest
       ↓
Multiple Decision Trees
       ↓
Voting
       ↓
Class Prediction
       ↓
0 / 1
```

Random Forest is useful because it can model nonlinear relationships between:

- Soil moisture
- Temperature
- Humidity
- Rainfall
- Rain probability
- Forecast conditions

---

# 💾 Model Persistence

The trained model is serialized using `joblib`.

```text
Training
   ↓
Random Forest
   ↓
joblib.dump()
   ↓
irrigation_model.pkl
```

During application startup:

```text
Load irrigation_model.pkl
```

If the model exists:

```text
Load Model
    ↓
Ready for inference
```

If the model does not exist:

```text
Model Missing
    ↓
Generate Dataset
    ↓
Train Random Forest
    ↓
Serialize Model
    ↓
Start Application
```

This provides a self-healing initialization mechanism.

---

# 🧪 Model Training Pipeline

The model-development pipeline is:

```text
Historical / Generated Dataset
            ↓
       Data Cleaning
            ↓
       Feature Selection
            ↓
       Train / Validation Split
            ↓
     Random Forest Training
            ↓
       Model Evaluation
            ↓
       Model Serialization
            ↓
 irrigation_model.pkl
```

For a production system, the generated training dataset should eventually be replaced or supplemented with **real field telemetry and validated irrigation labels**.

---

# 💻 Web Frontend Tier

The frontend is a single-page dashboard.

Technologies:

```text
HTML
CSS
JavaScript
Tailwind CSS
Font Awesome 6
```

The dashboard provides real-time visualization of system state.

---

# 📡 Dashboard Synchronization

The frontend periodically requests the latest state:

```text
GET /api/dashboard/latest
```

The browser performs asynchronous polling approximately every:

```text
3000 ms
```

Conceptual flow:

```text
Browser
   │
   │ fetch()
   ▼
/api/dashboard/latest
   │
   ▼
Flask
   │
   ▼
SQLite / Current State
   │
   ▼
JSON Response
   │
   ▼
Dashboard Update
```

---

# 📊 Dashboard Information

The dashboard can display:

```text
┌──────────────────────────────────────────────┐
│           SMART IRRIGATION DASHBOARD         │
├──────────────────────────────────────────────┤
│ Temperature       28.4 °C                    │
│ Humidity          72.1 %                     │
│ Soil Moisture     34.7 %                     │
│ Rain Probability  60 %                       │
│ Rainfall          1.2 mm                     │
│ Forecast Temp     27.9 °C                    │
│ Forecast Humidity 75 %                       │
├──────────────────────────────────────────────┤
│ AI Recommendation: IRRIGATION NOT REQUIRED   │
│ Pump Status: OFF                              │
│ Mode: AUTO                                    │
├──────────────────────────────────────────────┤
│ [ FORCE ON ] [ FORCE OFF ] [ AUTO ]          │
└──────────────────────────────────────────────┘
```

---

# 🗄️ Database Architecture

The system uses a telemetry table optimized for continuous environmental logging.

```text
┌────────────────────────┬───────────────┬────────────────────────────────────┐
│ Column                 │ Data Type     │ Description                        │
├────────────────────────┼───────────────┼────────────────────────────────────┤
│ id                     │ INTEGER       │ Primary key                       │
│ timestamp              │ DATETIME      │ UTC timestamp                     │
│ temperature            │ FLOAT         │ ESP32 temperature                 │
│ humidity               │ FLOAT         │ ESP32 humidity                    │
│ soil_moisture          │ FLOAT         │ Soil moisture                     │
│ rainfall               │ FLOAT         │ Forecast rainfall in mm           │
│ rain_probability       │ FLOAT         │ Rain probability                  │
│ forecast_temperature   │ FLOAT         │ Forecast temperature              │
│ forecast_humidity      │ FLOAT         │ Forecast humidity                 │
│ relay_status           │ BOOLEAN       │ Final pump command                │
│ ai_suggestion           │ VARCHAR(200)  │ AI decision explanation           │
└────────────────────────┴───────────────┴────────────────────────────────────┘
```

---

# 📋 Database Schema

Conceptual SQLAlchemy model:

```text
Telemetry
│
├── id
├── timestamp
├── temperature
├── humidity
├── soil_moisture
├── rainfall
├── rain_probability
├── forecast_temperature
├── forecast_humidity
├── relay_status
└── ai_suggestion
```

The `timestamp` field should preferably use UTC to provide consistent time-series records.

---

# 🔌 API Architecture

## Telemetry Endpoint

```text
POST /api/telemetry
```

Purpose:

```text
Receive ESP32 telemetry
```

Request:

```json
{
  "temperature": 28.4,
  "humidity": 72.1,
  "soil_moisture": 34.7
}
```

Processing:

```text
Receive
  ↓
Validate
  ↓
Fetch Weather
  ↓
Construct Features
  ↓
Run ML
  ↓
Apply Override
  ↓
Save Database Record
  ↓
Return Relay State
```

Response:

```json
{
  "relay": false
}
```

---

# 📡 Dashboard Latest Endpoint

```text
GET /api/dashboard/latest
```

Purpose:

Return the most recent system state to the web frontend.

Example response:

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

# 🎛️ Override Endpoint

```text
POST /api/dashboard/override
```

Purpose:

Allow the dashboard to change the control mode.

Conceptual request:

```json
{
  "mode": "FORCE_ON"
}
```

Possible values:

```text
AUTO
FORCE_ON
FORCE_OFF
```

---

# 🛡️ Reliability & Fail-Safe Strategy

The system implements multiple layers of fault tolerance.

```text
                 ┌──────────────────┐
                 │ Normal Operation │
                 └────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
       Weather Fail   ML Fail      Manual Mode
             │            │            │
             ▼            ▼            ▼
       Safe Defaults  Thresholds   Override
             │            │            │
             └────────────┼────────────┘
                          ▼
                  Final Safe Decision
```

---

# 🌦️ Weather API Failure

If OpenWeatherMap fails or times out, the backend can use safe fallback values.

Configured fallback values:

```text
Forecast Temperature = 25 °C
Forecast Humidity    = 50 %
Rain Probability     = 0 %
Rainfall             = 0 mm
```

The objective is to prevent a temporary external API failure from stopping the irrigation-control pipeline.

The system should also log the API failure so that the operator can distinguish real forecast data from fallback data.

---

# 🤖 ML Model Failure

If the `.pkl` model becomes unavailable or corrupted, the backend can use a deterministic safety rule.

Example:

```text
IF soil_moisture < 30%
    → Pump ON
ELSE
    → Pump OFF
```

Conceptual flow:

```text
ML Model Available?
       │
   ┌───┴───┐
  YES      NO
   │        │
   ▼        ▼
Random    Safety
Forest    Threshold
   │        │
   └───┬────┘
       ▼
Final Decision
```

---

# 🎚️ Manual Override Safety

Manual control takes precedence over AI inference.

Priority:

```text
1. FORCE OFF / FORCE ON
2. Safety fallback
3. ML prediction
```

The exact priority should be implemented consistently throughout the backend.

When returned to:

```text
AUTO
```

the ML-based decision becomes active again.

---

# ⚡ Active-LOW Relay Safety

The relay uses an active-LOW control signal.

```text
GPIO LOW
   ↓
Relay ON
   ↓
Pump ON
```

and:

```text
GPIO HIGH
   ↓
Relay OFF
   ↓
Pump OFF
```

The relay's normally-open configuration provides an additional hardware-level protection mechanism.

If the ESP32 loses power:

```text
ESP32 OFF
   ↓
GPIO no longer drives relay
   ↓
Relay returns to default state
   ↓
Normally-Open circuit opens
   ↓
Pump OFF
```

This prevents an ESP32 power failure from automatically causing continuous irrigation.

---

# 🔁 Complete Control-Loop Sequence

The complete control sequence is:

```text
┌──────────────────────────────────────────┐
│              ESP32 START                 │
└────────────────────┬─────────────────────┘
                     ↓
             Initialize Sensors
                     ↓
                Connect Wi-Fi
                     ↓
              Read Sensors
                     ↓
        ┌────────────────────────┐
        │ Temperature            │
        │ Humidity               │
        │ Soil Moisture          │
        └────────────┬───────────┘
                     ↓
             Create JSON Payload
                     ↓
             HTTP POST Telemetry
                     ↓
┌──────────────────────────────────────────┐
│              FLASK SERVER                │
└────────────────────┬─────────────────────┘
                     ↓
             Validate Payload
                     ↓
             Request Forecast
                     ↓
          Weather Data Available?
                /         \
              YES          NO
               │            │
               │       Use Safe Defaults
               │            │
               └─────┬──────┘
                     ↓
             Feature Construction
                     ↓
              Random Forest
                     ↓
               ML Prediction
                     ↓
            Manual Override?
                /       \
              YES        NO
               │          │
               ▼          ▼
         Override State  ML Result
               │          │
               └────┬─────┘
                    ↓
              Final Relay State
                    ↓
              Store Telemetry
                    ↓
             HTTP JSON Response
                    ↓
┌──────────────────────────────────────────┐
│                 ESP32                    │
└────────────────────┬─────────────────────┘
                     ↓
                GPIO 26
                     ↓
                  Relay
                     ↓
                  Pump
                     ↓
               Irrigation
                     ↓
            Environmental Change
                     ↓
              Next Sensor Cycle
                     ↺
```

---

# 🧩 Software Component Architecture

## Backend Components

```text
backend/
│
├── app.py
│   └── Flask application
│
├── models/
│   └── telemetry.py
│       └── SQLAlchemy database model
│
├── services/
│   ├── weather_service.py
│   │   └── OpenWeatherMap integration
│   │
│   ├── ml_service.py
│   │   └── Model loading and inference
│   │
│   └── irrigation_service.py
│       └── Irrigation decision logic
│
├── scheduler/
│   └── tasks.py
│       └── APScheduler jobs
│
├── ml/
│   ├── train.py
│   ├── dataset_generator.py
│   └── irrigation_model.pkl
│
└── database/
    └── telemetry.db
```

---

# 🌐 Frontend Components

```text
frontend/
│
├── index.html
│
├── css/
│   └── style.css
│
└── js/
    └── dashboard.js
```

Responsibilities:

```text
index.html
    → Dashboard structure

style.css
    → Custom visual styling

dashboard.js
    → API polling
    → Dashboard updates
    → Manual controls
```

---

# 🔌 ESP32 Components

```text
esp32/
│
├── src/
│   ├── main.ino
│   ├── config.h
│   ├── sensors.h
│   ├── sensors.cpp
│   ├── network.h
│   └── network.cpp
│
└── config/
    └── config.example.h
```

Main responsibilities:

```text
main.ino
    ↓
System initialization
    ↓
Sensor reading
    ↓
Telemetry creation
    ↓
HTTP communication
    ↓
Relay control
```


---

# 🔐 Security Considerations

Although this is currently a local IoT system, several security measures should be considered.

## API Authentication

Production deployments should authenticate ESP32 requests.

Possible approach:

```text
ESP32
   ↓
API Key / Token
   ↓
Flask
```

---

## Environment Variables

Sensitive configuration should not be hardcoded.

Example:

```text
OPENWEATHER_API_KEY
FIELD_LAT
FIELD_LON
DATABASE_URL
SECRET_KEY
MQTT_USERNAME
MQTT_PASSWORD
```

These values should be stored in environment variables or a protected configuration file.

---

## HTTPS

When the backend is deployed outside a trusted local network:

```text
ESP32
   ↓
HTTPS
   ↓
Flask Server
```

should be preferred over unencrypted HTTP.

---

# 📈 Observability

The system should maintain logs for:

```text
Sensor failures
Wi-Fi failures
HTTP failures
Weather API failures
ML inference failures
Relay transitions
Manual overrides
Database failures
```

A useful logging hierarchy is:

```text
INFO
WARNING
ERROR
CRITICAL
```

Example:

```text
INFO     Telemetry received
INFO     ML prediction generated
INFO     Relay state changed
WARNING  Weather API unavailable
WARNING  Using fallback forecast
ERROR    ML model loading failed
CRITICAL Database unavailable
```

---

# 🧪 Testing Strategy

The system should be tested at multiple levels.

## Unit Testing

Test individual functions:

```text
Sensor conversion
Weather parsing
Feature construction
ML inference
Override logic
Database insertion
```

---

## API Testing

Test:

```text
POST /api/telemetry
GET /api/dashboard/latest
POST /api/dashboard/override
```

---

## ML Testing

Evaluate:

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

For an irrigation system, evaluation should also consider the operational cost of:

```text
False Positive
False Negative
```

because unnecessary irrigation wastes water, while missed irrigation can stress crops.

---

# 🔄 Operational States

The complete system can be represented using the following states:

```text
                  ┌─────────────┐
                  │    START    │
                  └──────┬──────┘
                         ↓
                  ┌─────────────┐
                  │ SENSOR READ │
                  └──────┬──────┘
                         ↓
                  ┌─────────────┐
                  │ TRANSMIT    │
                  └──────┬──────┘
                         ↓
                  ┌─────────────┐
                  │ PROCESS     │
                  └──────┬──────┘
                         ↓
                ┌───────────────────┐
                │ CONTROL MODE      │
                └───────┬───────────┘
                        │
             ┌──────────┼──────────┐
             ↓          ↓          ↓
          AUTO       FORCE ON   FORCE OFF
             │          │          │
             ↓          ↓          ↓
            ML         ON         OFF
             │          │          │
             └──────────┼──────────┘
                        ↓
                  ┌─────────────┐
                  │   ACTUATE   │
                  └──────┬──────┘
                         ↓
                  ┌─────────────┐
                  │ LOG DATA    │
                  └──────┬──────┘
                         ↓
                  ┌─────────────┐
                  │ NEXT CYCLE  │
                  └──────┬──────┘
                         │
                         └──────────────↺
```

---

# 🚨 Failure Handling Matrix

| Failure | Detection | Fallback |
|---|---|---|
| DHT11 failure | Invalid reading | Ignore invalid sample / log error |
| Soil sensor failure | Out-of-range ADC | Use safety logic |
| Wi-Fi failure | Connection timeout | Retry connection |
| Backend unavailable | HTTP failure | Retry request |
| Weather API failure | Timeout/API error | Safe forecast defaults |
| ML model missing | File not found | Train/rebuild model |
| ML model corrupted | Load/inference exception | Safety threshold |
| Database failure | SQL exception | Log error and continue control where safe |
| Manual override | Override state active | Use forced state |
| ESP32 power loss | Hardware failure | Relay defaults to OFF |

---

# 🔄 Data Lifecycle

Every telemetry record follows this lifecycle:

```text
Physical Environment
        ↓
Sensor
        ↓
ESP32 ADC / GPIO
        ↓
JSON Payload
        ↓
HTTP
        ↓
Flask
        ↓
Validation
        ↓
Weather Fusion
        ↓
Feature Vector
        ↓
Random Forest
        ↓
Final Decision
        ↓
SQLite Storage
        ↓
HTTP Response
        ↓
ESP32 Relay
        ↓
Physical Pump
```

---

# 🧠 AI Decision Reasoning

The `ai_suggestion` field provides a human-readable explanation of the current decision.

Example:

```text
"Irrigation required: soil moisture below desired level."
```

or:

```text
"Irrigation postponed: high probability of rainfall."
```

or:

```text
"Irrigation disabled by manual override."
```

or:

```text
"Safety threshold activated because ML inference failed."
```

This makes the system more interpretable than exposing only a binary:

```text
0 / 1
```

decision.

---

# 📊 Example End-to-End Transaction

Assume the ESP32 measures:

```text
Temperature      = 31.2 °C
Humidity         = 58 %
Soil Moisture    = 24 %
```

The weather API returns:

```text
Forecast Temp    = 32.0 °C
Forecast Humidity= 55 %
Rain Probability = 10 %
Rainfall         = 0 mm
```

The resulting feature vector is:

```text
X =
[
    31.2,
    58,
    24,
    0,
    10,
    32.0,
    55
]
```

The Random Forest evaluates:

```text
Prediction = 1
```

Therefore:

```text
Irrigation Required
       ↓
Relay = ON
       ↓
GPIO 26 = LOW
       ↓
Pump = ON
```

The transaction is saved into SQLite.

---

# 📐 Mathematical System Model

The system can be represented mathematically as a feedback controller.

Let the environmental state at time $t$ be:

$$
S_t =
[
T_t,
H_t,
SM_t
]
$$

and weather forecast state be:

$$
W_t =
[
R_t,
P_{r,t},
T_{f,t},
H_{f,t}
]
$$

The complete model input becomes:

$$
X_t = [S_t,W_t]
$$

The ML controller generates:

$$
Y_t = f_{\mathrm{RF}}(X_t)
$$

where:

$$
Y_t \in \{0,1\}
$$

The final control signal is:

$$
U_t =
\begin{cases}
U_{\mathrm{override}}, & \text{if manual override is active}\\
Y_t, & \text{if ML inference succeeds}\\
U_{\mathrm{safe}}, & \text{if ML inference fails}
\end{cases}
$$

The actuator receives:

$$
GPIO_{26} =
\begin{cases}
LOW, & U_t = 1\\
HIGH, & U_t = 0
\end{cases}
$$

Thus, the complete closed-loop system becomes:

$$
Environment
\rightarrow Sensors
\rightarrow ESP32
\rightarrow Backend
\rightarrow Weather + ML
\rightarrow Relay
\rightarrow Pump
\rightarrow Environment
$$

---

# 🚀 Future Extensions

The current architecture can be extended substantially.

## MQTT Communication

Instead of HTTP telemetry:

```text
ESP32
   ↓
MQTT Broker
   ↓
Processing Node
```

This can provide efficient publish/subscribe communication for multiple sensor nodes.

---

## PostgreSQL / Time-Series Database

SQLite can eventually be replaced with:

```text
PostgreSQL
TimescaleDB
InfluxDB
```

for larger deployments.

---

## Multi-Node Agriculture

The architecture can support multiple ESP32 nodes:

```text
ESP32 Node 1 ─┐
ESP32 Node 2 ─┤
ESP32 Node 3 ─┼──→ Backend
ESP32 Node 4 ─┤
ESP32 Node 5 ─┘
```

Each node can represent a different irrigation zone.

---

## Zone-Based Irrigation

The system can control:

```text
Zone 1 → Pump/Valve 1
Zone 2 → Pump/Valve 2
Zone 3 → Pump/Valve 3
```

allowing irrigation based on local soil conditions.

---

## Improved Machine Learning

Future models can include:

```text
Random Forest
XGBoost
LightGBM
Gradient Boosting
LSTM
Temporal Fusion Transformer
```

Time-series models can use historical environmental measurements to predict future soil moisture.

---

## Automated Model Retraining

A future architecture can periodically retrain the model using newly collected field data.

```text
New Telemetry
      ↓
Database
      ↓
Data Validation
      ↓
Feature Engineering
      ↓
Model Retraining
      ↓
Evaluation
      ↓
Model Registry
      ↓
Deployment
```

A production implementation should only replace the active model after validation passes.

---

## Edge AI

The Random Forest model could eventually be deployed directly on the ESP32 or another edge device.

```text
Current:

ESP32 → Server → ML → ESP32


Future:

ESP32 → Local ML → Relay
             │
             └──→ Server for logging/dashboard
```

This reduces dependence on network availability for immediate control.

---

## Predictive Soil Moisture

Instead of only predicting:

```text
Irrigation: YES / NO
```

the system could predict:

```text
Soil Moisture in 1 hour
Soil Moisture in 3 hours
Soil Moisture in 6 hours
```

This would enable predictive irrigation scheduling.

---

# 🌍 Sustainability Objective

The system is intended to reduce unnecessary irrigation by combining:

```text
Real-Time Soil Conditions
          +
Weather Forecast
          +
Machine Learning
          +
Automated Control
```

The objective is to irrigate when required rather than relying exclusively on fixed schedules.

Potential benefits include:

- Reduced water wastage
- Reduced unnecessary pump operation
- Automated irrigation
- Better utilization of weather forecasts
- Continuous environmental monitoring
- Data-driven agricultural decisions

---

# 🏁 Conclusion

The AI-Powered Smart Irrigation System is a complete cyber-physical architecture combining **IoT sensing, edge computing, REST communication, weather intelligence, machine learning, persistent telemetry storage, web visualization, and automated actuation**.

The system operates as a closed-loop controller:

```text
┌───────────────────────────────────────────────┐
│                                               │
│              PHYSICAL ENVIRONMENT             │
│                       │                       │
│                       ▼                       │
│                    SENSORS                   │
│                       │                       │
│                       ▼                       │
│                     ESP32                    │
│                       │                       │
│                       ▼                       │
│                  FLASK BACKEND               │
│                       │                       │
│            ┌──────────┼──────────┐            │
│            ▼          ▼          ▼            │
│         WEATHER      DATABASE     ML          │
│            │                     │            │
│            └──────────┬──────────┘            │
│                       ▼                       │
│                DECISION ENGINE                │
│                       │                       │
│                       ▼                       │
│                    RELAY                     │
│                       │                       │
│                       ▼                       │
│                     PUMP                     │
│                       │                       │
│                       ▼                       │
│              PHYSICAL ENVIRONMENT             │
│                                               │
└───────────────────────────────────────────────┘
```

The resulting architecture provides a foundation for evolving the project from a prototype into a **multi-zone, predictive, data-driven agricultural automation platform**.

---

## 📌 System Summary

| Component | Technology | Primary Responsibility |
|---|---|---|
| Microcontroller | ESP32 | Edge processing and communication |
| Temperature/Humidity | DHT11 | Microclimate sensing |
| Soil Sensor | Analog ADC | Soil-moisture measurement |
| Actuator | Active-LOW Relay | Pump switching |
| Backend | Flask | System orchestration |
| Database | SQLite | Telemetry persistence |
| ORM | SQLAlchemy | Database abstraction |
| Weather | OpenWeatherMap | Forecast data |
| ML | Random Forest | Irrigation prediction |
| Serialization | Joblib | Model persistence |
| Scheduler | APScheduler | Background tasks |
| Notification | Ntfy.sh | Field/system notifications |
| Frontend | HTML/CSS/JS | Dashboard |
| UI Framework | Tailwind CSS | Dashboard styling |
| Icons | Font Awesome 6 | UI icons |
| Communication | HTTP/REST | ESP32 ↔ Backend |
| Control | GPIO 26 | Relay actuation |

---

## 🔑 Core Design Principle

> **Sense → Fuse → Predict → Decide → Act → Observe → Repeat**

This principle forms the foundation of the entire AI-powered smart irrigation architecture.
