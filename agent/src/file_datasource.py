from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
from domain.temperature import Temperature
from domain.humidity import Humidity
from domain.vibration import Vibration
from domain.light import Light
from domain.air_quality import AirQuality
import config
import random

class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accel_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

        with open(self.gps_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.gps_lines = lines

        with open(self.accel_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.accel_lines = lines

        with open(self.parking_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.parking_lines = lines

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        data = AggregatedData(
            accelerometer=Accelerometer(1, 2, 3),
            gps=Gps(4, 5),
            parking=Parking(25, Gps(4, 5)),
            temperature=Temperature(-376, "C"),
            humidity=Humidity(0, "%"),
            vibration=Vibration(1, 2, 3),
            light=Light(900000),
            air_quality=AirQuality(-5, -5),
            timestamp=datetime.now(),
            user_id=config.USER_ID,
        )

        if self.reading == True:
            if self.gps_line > len(self.gps_lines) - 1:
                self.gps_line = 0

            if self.accel_line > len(self.accel_lines) - 1:
                self.accel_line = 0

            if self.parking_line > len(self.parking_lines) - 1:
                self.parking_line = 0

            split_gps = self.gps_lines[self.gps_line].split(',')
            split_accel = self.accel_lines[self.accel_line].split(',')
            split_parking = self.parking_lines[self.parking_line].split(',')

            lat, long = split_gps
            data.gps = Gps(long, lat)

            x, y, z = split_accel
            data.accelerometer = Accelerometer(x, y, z)

            long, lat, empty_count = split_parking
            data.parking = Parking(empty_count, Gps(long, lat))

            self.gps_line += 1
            self.accel_line += 1
            self.parking_line += 1

        data.temperature = self._generate_temperature()
        data.humidity = self._generate_humidity()
        data.vibration = self._generate_vibration()
        data.light = self._generate_light()
        data.air_quality = self._generate_air_quality()

        return data

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.reading = True
        self.accel_line = 0
        self.gps_line = 0
        self.parking_line = 0

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.reading = False

    # Генератори випадкових даних
    def _generate_temperature(self) -> Temperature:
        value = round(random.uniform(-10.0, 40.0), 2)
        return Temperature(value=value, unit="C")

    def _generate_humidity(self) -> Humidity:
        value = round(random.uniform(0.0, 100.0), 2)
        return Humidity(value=value, unit="%")

    def _generate_vibration(self) -> Vibration:
        x = round(random.uniform(-5.0, 5.0), 3)
        y = round(random.uniform(-5.0, 5.0), 3)
        z = round(random.uniform(-5.0, 5.0), 3)
        return Vibration(x=x, y=y, z=z)

    def _generate_light(self) -> Light:
        illum = round(random.uniform(0.0, 2000.0), 1)
        return Light(illumination=illum)

    def _generate_air_quality(self) -> AirQuality:
        pm2_5 = round(random.uniform(0.0, 500.0), 1)
        pm10 = round(random.uniform(0.0, 600.0), 1)
        aqi = random.randint(0, 300)
        return AirQuality(pm2_5=pm2_5, pm10=pm10, aqi=aqi)