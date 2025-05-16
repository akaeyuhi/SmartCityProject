from dataclasses import dataclass


@dataclass
class AirQuality:
    pm2_5: float
    pm10: float
    aqi: int = None

    def categorize(self) -> str:
        if self.aqi is None:
            return "Unknown"
        if self.aqi <= 50:
            return "Good"
        if self.aqi <= 100:
            return "Moderate"
        if self.aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        if self.aqi <= 200:
            return "Unhealthy"
        if self.aqi <= 300:
            return "Very Unhealthy"
        return "Hazardous"
