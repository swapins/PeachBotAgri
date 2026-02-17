import importlib
from typing import Any, Optional

from services.weather_service import WeatherService


class PeachBotEngine:
    def __init__(self, crop_type: str):
        # Dynamically load the crop module
        try:
            module = importlib.import_module(f"crops.{crop_type}")
            # Automatically find the class (e.g., CoffeeModule)
            class_name = f"{crop_type.capitalize()}Module"
            self.crop = getattr(module, class_name)()
            print(f"--- PeachBot Agri: {self.crop.name} Engine Loaded ---")
        except Exception as e:
            print(f"Error loading crop '{crop_type}': {e}")
            self.crop = None

        # Weather service (optional); will return None if API key missing
        try:
            self.weather = WeatherService()
        except Exception:
            self.weather = None

    def process_field_data(self, sensors: dict, vision_result: Any = None, lat: Optional[float] = None, lon: Optional[float] = None):
        if not self.crop:
            return

        # 1. Environment Analysis
        # Fetch weather metrics if coordinates provided and service available
        weather_data = None
        if lat is not None and lon is not None and getattr(self, "weather", None):
            try:
                weather_data = self.weather.get_agri_metrics(lat, lon)
            except Exception as e:
                print(f"Warning: failed to fetch weather data: {e}")

        try:
            # Pass weather_data (may be None) to crop analyzer
            report = self.crop.analyze_health(sensors, weather_data)
            print(f"Analysis: {report}")
        except Exception as e:
            print(f"Error running analyze_health: {e}")

        # 2. Vision Analysis (Pest/Disease)
        if vision_result:
            # Accept either a single label or a list of labels
            if isinstance(vision_result, (list, tuple)):
                detections = vision_result
            else:
                detections = [vision_result]

            for det in detections:
                try:
                    remedy = self.crop.get_pest_remedy(det)
                    print(f"Detection: [{det}] -> Action: {remedy}")
                except Exception as e:
                    print(f"Error resolving remedy for '{det}': {e}")


# --- LOCAL TEST ---
if __name__ == "__main__":
    # Simulate data coming from an Edge device/IoT sensor
    iot_payload = {"temp": 28, "humidity": 55, "soil_ph": 6.2, "moisture": 45}
    ai_vision_tag = "Leaf Rust"

    # Example coordinates (Coorg, India) — used to fetch last-7-day metrics
    demo_lat = 12.3375
    demo_lon = 75.8069

    # Initialize for Coffee
    bot = PeachBotEngine("coffee")
    bot.process_field_data(iot_payload, ai_vision_tag, lat=demo_lat, lon=demo_lon)
