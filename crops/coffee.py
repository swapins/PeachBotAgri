from .base_crop import CropModule
from typing import Optional


class CoffeeModule(CropModule):
    def __init__(self):
        self.name = "Coffee (Arabica)"

    def analyze_health(self, sensor_data: dict, weather_data: Optional[dict] = None) -> str:
        report = []

        # 1. Physical Sensor Logic (Local)
        soil_moisture = sensor_data.get("moisture") or sensor_data.get("soil_moisture")
        if soil_moisture is None:
            soil_moisture = 70

        if soil_moisture < 50:
            report.append("💧 LOCAL: Soil moisture low. Irrigation recommended.")

        # 2. Historical Weather Logic (GPS-based)
        if weather_data:
            if (weather_data.get("total_rain_week") or 0) > 50:
                report.append("🌧️ HISTORICAL: High weekly rainfall. Risk of Coffee Leaf Rust (Fungal).")

            if (weather_data.get("avg_temp_week") or 0) > 25:
                report.append("🔥 TREND: Sustained high temps. Monitor for Coffee Berry Borer.")

        return "\n".join(report) if report else "✅ Status: Optimal growing conditions."

    def get_pest_remedy(self, detection: str) -> str:
        if not detection:
            return "General organic pesticide recommended."

        # Accept labels that may vary; do case-insensitive substring matching
        remedies = {
            "leaf rust": "Apply copper-based fungicide.",
            "rust": "Apply copper-based fungicide.",
            "berry borer": "Install pheromone traps.",
            "borer": "Install pheromone traps.",
        }

        det_lower = str(detection).lower()
        for key, rem in remedies.items():
            if key in det_lower or det_lower in key:
                return rem

        return "General organic pesticide recommended."
