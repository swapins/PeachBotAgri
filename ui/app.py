import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Ensure project root is on sys.path so imports like `from main import ...` work
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import PeachBotEngine
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

# Initialize engine (loads crop module)
engine = PeachBotEngine("coffee")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run-demo", methods=["POST"])
def run_demo():
    payload = request.get_json() or {}

    # Sensors (fall back to defaults)
    sensors = payload.get("sensors", {"moisture": 45, "temp": 28, "humidity": 55})
    vision = payload.get("vision")  # single label or list
    lat = payload.get("lat")
    lon = payload.get("lon")

    # Fetch weather if available
    weather_data = None
    if lat is not None and lon is not None and getattr(engine, "weather", None):
        try:
            weather_data = engine.weather.get_agri_metrics(lat, lon)
        except Exception:
            weather_data = None

    # Run crop analysis
    report = None
    remedies = []
    try:
        report = engine.crop.analyze_health(sensors, weather_data)
    except Exception as e:
        report = f"Error: {e}"

    if vision:
        labels = vision if isinstance(vision, list) else [vision]
        for lab in labels:
            try:
                remedies.append({"label": lab, "remedy": engine.crop.get_pest_remedy(lab)})
            except Exception:
                remedies.append({"label": lab, "remedy": "unknown"})

    result = {
        "report": report,
        "weather_data": weather_data,
        "remedies": remedies,
    }

    return jsonify(result)


if __name__ == "__main__":
    # Use 0.0.0.0 so a kiosk/touch device can access
    app.run(host="0.0.0.0", port=8080, debug=False)
