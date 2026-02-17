import requests
import os
from dotenv import load_dotenv

load_dotenv()


class WeatherService:
    """Fetch agricultural weather metrics using Visual Crossing timeline API.

    Returns a dict with safe defaults or None on failure.
    """

    def __init__(self):
        self.api_key = os.getenv("VISUAL_CROSSING_KEY")
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    def get_agri_metrics(self, lat, lon):
        if not self.api_key:
            # API key not configured
            return None

        url = f"{self.base_url}/{lat},{lon}/last7days?unitGroup=metric&key={self.api_key}&include=days"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            days = data.get("days", [])
            if not days:
                return None

            # Safely aggregate fields with fallbacks
            temps = [d.get("temp") for d in days if d.get("temp") is not None]
            precip = [d.get("precip") for d in days if d.get("precip") is not None]

            avg_temp = sum(temps) / len(temps) if temps else None
            total_precip = sum(precip) if precip else 0.0
            current_humidity = days[-1].get("humidity")

            return {
                "avg_temp_week": avg_temp,
                "total_rain_week": total_precip,
                "current_humidity": current_humidity,
            }

        except Exception:
            return None
