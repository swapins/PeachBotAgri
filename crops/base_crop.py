from abc import ABC, abstractmethod
from typing import Optional


class CropModule(ABC):
    @abstractmethod
    def analyze_health(self, sensor_data: dict, weather_data: Optional[dict] = None) -> str:
        pass

    @abstractmethod
    def get_pest_remedy(self, detection: str) -> str:
        pass
