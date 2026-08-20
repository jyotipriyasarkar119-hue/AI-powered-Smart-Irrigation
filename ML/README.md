# AI Irrigation Predictive Model (`irrigation_model.pkl`)

This directory contains the machine learning pipeline and pre-trained Random Forest model used by the **AI-Powered Smart Irrigation System**. The model processes real-time micro-climate telemetry from the ESP32 node alongside external weather forecasts to dynamically determine optimal pump actuation.

---

## 📌 Model Overview

* **Algorithm:** `RandomForestClassifier` (Scikit-Learn)
* **File Format:** Joblib Serialized Binary (`irrigation_model.pkl`)
* **Task Type:** Binary Classification (`1` = Pump ON, `0` = Pump OFF)
* **Hyperparameters:** `n_estimators=100`, `max_depth=10`, `random_state=42`

---

## 📊 Feature Schema

The model evaluates a 7-parameter feature vector combining physical telemetry with weather forecast metrics:

| Feature Name | Source | Type | Description |
| :--- | :--- | :--- | :--- |
| `temp` | ESP32 (DHT11) | Float (°C) | Current ambient field temperature |
| `hum` | ESP32 (DHT11) | Float (%) | Current ambient relative humidity |
| `soil` | ESP32 (ADC) | Float (%) | Current soil moisture percentage |
| `rain` | OpenWeatherMap API | Float (mm) | Expected rainfall volume in the next 3 hours |
| `prob` | OpenWeatherMap API | Float (%) | Probability of precipitation |
| `f_temp` | OpenWeatherMap API | Float (°C) | Forecasted temperature for upcoming window |
| `f_hum` | OpenWeatherMap API | Float (%) | Forecasted relative humidity |

### Target Variable
* `1` (**Turn Pump ON**): Triggered when soil moisture is critically low and precipitation probability/volume is insufficient to hydrate crops naturally.
* `0` (**Keep Pump OFF**): Triggered when soil moisture is adequate or imminent rain is forecasted.

---

## ⚙️ Automated Training & Initialization

The model file is automatically trained and compiled if missing on system boot:

1. **Auto-Generation:** If `irrigation_model.pkl` is not found, `app.py` triggers `initialize_and_load_ai_model()`.
2. **Data Generation:** Synthesizes 3,000 domain-specific agricultural samples based on soil types and crop threshold conditions.
3. **Model Saving:** Fits the `RandomForestClassifier` and serializes it to disk via `joblib.dump()`.

---

## 🧪 Independent Testing & Verification

Run this single-line verification script in terminal to load the model and test sample dry and wet field inputs:

```bash
python3 -c "import joblib; model = joblib.load('irrigation_model.pkl'); dry = [[35.0, 30.0, 15.0, 0.0, 10.0, 36.0, 28.0]]; wet = [[22.0, 80.0, 75.0, 12.0, 90.0, 20.0, 85.0]]; print(f'Dry Field (Pump ON): {bool(model.predict(dry)[0])}'); print(f'Wet Field (Pump OFF): {bool(model.predict(wet)[0])}')"
