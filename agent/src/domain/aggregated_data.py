from dataclasses import dataclass

from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.temperature import Temperature
from domain.humidity import Humidity
from domain.vibration import Vibration
from domain.light import Light
from domain.air_quality import AirQuality
from domain.parking import Parking


@dataclass
class AggregatedData:
    accelerometer: Accelerometer
    gps: Gps
    timestamp: datetime
    parking: Parking
    temperature: Temperature
    humidity: Humidity
    vibration: Vibration
    light: Light
    air_quality: AirQuality
    user_id: int
