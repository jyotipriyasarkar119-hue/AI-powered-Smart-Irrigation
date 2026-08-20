import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///irrigation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")
LAT = os.getenv("FIELD_LAT", "28.6139")
LON = os.getenv("FIELD_LON", "77.2090")
SOIL_TYPE = "Sandy Loam"
CROP_TYPE = "Tomato"

NTFY_TOPIC = os.getenv("NTFY_TOPIC", "my_smart_irrigation_field_99")
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

db = SQLAlchemy(app)
manual_relay_override = None 
loaded_model = None  # Global in-memory AI model

# --- AI MODEL AUTO-GENERATOR & LOADER ---
MODEL_PATH = 'irrigation_model.pkl'

def initialize_and_load_ai_model():
    global loaded_model
    if not os.path.exists(MODEL_PATH):
        print("[AI] Model file not found. Auto-training new Random Forest Model...")
        np.random.seed(42)
        samples = 3000
        
        temp = np.random.uniform(15.0, 45.0, samples)
        humidity = np.random.uniform(20.0, 90.0, samples)
        soil_moisture = np.random.uniform(10.0, 90.0, samples)
        rainfall = np.random.exponential(scale=1.5, size=samples)
        rain_prob = np.random.uniform(0.0, 100.0, samples)
        forecast_temp = temp + np.random.uniform(-3.0, 3.0, samples)
        forecast_hum = humidity + np.random.uniform(-10.0, 10.0, samples)

        pump_on = (
            (soil_moisture < 35.0) & 
            (rain_prob < 50.0) & 
            (rainfall < 2.0)
        ) | (
            (soil_moisture < 20.0) & 
            (rainfall < 5.0)
        )

        X = pd.DataFrame({
            'temp': temp, 'hum': humidity, 'soil': soil_moisture,
            'rain': rainfall, 'prob': rain_prob, 'f_temp': forecast_temp, 'f_hum': forecast_hum
        })
        y = pump_on.astype(int)

        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X.values, y)
        joblib.dump(model, MODEL_PATH)
        print("[AI] Model compiled and saved.")

    try:
        loaded_model = joblib.load(MODEL_PATH)
        print("[AI] Model loaded successfully into memory.")
    except Exception as e:
        print(f"[AI ERROR] Failed to load model: {e}")

# Initialize and load model into RAM
initialize_and_load_ai_model()

# --- DATABASE MODEL ---
class Telemetry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    soil_moisture = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False, default=0.0)
    rain_probability = db.Column(db.Float, nullable=False, default=0.0)
    forecast_temperature = db.Column(db.Float, nullable=False, default=0.0)
    forecast_humidity = db.Column(db.Float, nullable=False, default=0.0)
    relay_status = db.Column(db.Boolean, nullable=False)
    ai_suggestion = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

# --- PUSH NOTIFICATION HELPER ---
def send_push_notification(title, message, priority="default", tags=None):
    headers = {"Title": title, "Priority": priority}
    if tags:
        headers["Tags"] = tags

    try:
        res = requests.post(NTFY_URL, data=message.encode('utf-8'), headers=headers, timeout=5)
        if res.status_code == 200:
            print(f"[NOTIFY] Delivered: {title}")
    except Exception as e:
        print(f"[NOTIFY ERROR] {e}")

# --- HELPER FUNCTIONS ---
def get_weather_forecast():
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}&units=metric"
    default_weather = {"rainfall": 0.0, "rain_probability": 0.0, "forecast_temperature": 25.0, "forecast_humidity": 50.0}
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("cod") == "200":
            first_slot = res['list'][0]
            return {
                "rainfall": float(first_slot.get('rain', {}).get('3h', 0.0)),
                "rain_probability": float(first_slot.get('pop', 0.0)) * 100.0,
                "forecast_temperature": float(first_slot['main']['temp']),
                "forecast_humidity": float(first_slot['main']['humidity'])
            }
    except Exception as e:
        print(f"[WEATHER API ERROR] {e}")
    return default_weather

def predict_irrigation(temp, humidity, soil_moisture, weather):
    global loaded_model
    if loaded_model is not None:
        try:
            features = [[
                temp, humidity, soil_moisture, 
                weather['rainfall'], weather['rain_probability'], 
                weather['forecast_temperature'], weather['forecast_humidity']
            ]]
            prediction = loaded_model.predict(features)
            return bool(prediction[0])
        except Exception as e:
            print(f"[INFERENCE ERROR] {e}")

    # Fallback heuristic if model prediction fails
    if soil_moisture < 35.0 and weather['rain_probability'] < 50.0 and weather['rainfall'] < 2.0:
        return True
    return False

def send_weekly_field_report():
    with app.app_context():
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        records = Telemetry.query.filter(Telemetry.timestamp >= one_week_ago).all()
        
        avg_moisture = (sum(r.soil_moisture for r in records) / len(records)) if records else 0.0
        avg_temp = (sum(r.temperature for r in records) / len(records)) if records else 0.0
        total_irrigations = sum(1 for r in records if r.relay_status) if records else 0

        summary = (
            f"Crop: {CROP_TYPE} | Soil: {SOIL_TYPE}\n"
            f"Avg Moisture: {avg_moisture:.1f}%\n"
            f"Avg Field Temp: {avg_temp:.1f}°C\n"
            f"Pump Activations (7 days): {total_irrigations} cycles"
        )
        
        send_push_notification(
            title="Weekly Field Health Summary",
            message=summary,
            priority="high",
            tags="seedling,chart_with_upwards_trend"
        )

# --- API ENDPOINTS ---
@app.route('/api/telemetry', methods=['POST'])
def receive_telemetry():
    global manual_relay_override
    data = request.get_json() or {}  # Prevent NoneType AttributeError
    
    temp = data.get('temperature', 0.0)
    humidity = data.get('humidity', 0.0)
    soil_moisture = data.get('soil_moisture', 0.0)

    weather = get_weather_forecast()
    ai_decision = predict_irrigation(temp, humidity, soil_moisture, weather)
    suggestion_text = f"AI Decision: {'Turn Pump ON' if ai_decision else 'Keep Pump OFF'}. Rain Prob: {weather['rain_probability']}%, Rain Vol: {weather['rainfall']}mm for {CROP_TYPE} ({SOIL_TYPE})."

    final_relay_state = manual_relay_override if manual_relay_override is not None else ai_decision

    entry = Telemetry(
        temperature=temp, humidity=humidity, soil_moisture=soil_moisture,
        rainfall=weather['rainfall'], rain_probability=weather['rain_probability'],
        forecast_temperature=weather['forecast_temperature'], forecast_humidity=weather['forecast_humidity'],
        relay_status=final_relay_state, ai_suggestion=suggestion_text
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({"relay": final_relay_state}), 200

@app.route('/api/dashboard/latest', methods=['GET'])
def get_dashboard_data():
    latest = Telemetry.query.order_by(Telemetry.timestamp.desc()).first()
    if not latest:
        return jsonify({"message": "No data recorded yet"}), 404

    return jsonify({
        "timestamp": latest.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": latest.temperature,
        "humidity": latest.humidity,
        "soil_moisture": latest.soil_moisture,
        "rainfall": latest.rainfall,
        "rain_probability": latest.rain_probability,
        "forecast_temperature": latest.forecast_temperature,
        "forecast_humidity": latest.forecast_humidity,
        "relay_status": latest.relay_status,
        "manual_override_active": manual_relay_override is not None,
        "override_state": manual_relay_override,
        "ai_suggestion": latest.ai_suggestion,
        "crop_type": CROP_TYPE,
        "soil_type": SOIL_TYPE
    }), 200

@app.route('/api/dashboard/override', methods=['POST'])
def dashboard_manual_override():
    global manual_relay_override
    data = request.get_json() or {}
    action = data.get("action")
    
    manual_relay_override = True if action == "ON" else (False if action == "OFF" else None)
    
    if manual_relay_override is not None:
        state_str = "FORCED ON" if manual_relay_override else "FORCED OFF"
        send_push_notification("Manual Override Activated", f"Pump state set to {state_str} from dashboard.", priority="high", tags="warning,droplet")
    else:
        send_push_notification("Control Mode Reset", "System returned to Automatic ML control.", priority="default", tags="gear")

    return jsonify({"status": "Success", "manual_override": manual_relay_override}), 200

# Prevent duplicate scheduler execution in Werkzeug debug mode
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_weekly_field_report, trigger="interval", days=7)
    scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
