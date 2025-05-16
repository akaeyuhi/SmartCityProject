from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationInfo

class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class TemperatureData(BaseModel):
    value: float
    unit: str


class HumidityData(BaseModel):
    value: float
    unit: str


class VibrationData(AccelerometerData):
    magnitude: float = None

    @field_validator('magnitude', mode='after')
    def compute_magnitude(cls, v, info: ValidationInfo):
        x = info.data.get('x', 0)
        y = info.data.get('y', 0)
        z = info.data.get('z', 0)
        return (x**2 + y**2 + z**2) ** 0.5

class LightData(BaseModel):
    illumination: float


class AirQualityData(BaseModel):
    pm2_5: float
    pm10: float
    aqi: int = None


class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    temperature: TemperatureData
    humidity: HumidityData
    vibration: VibrationData
    light: LightData
    air_quality: AirQualityData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )
