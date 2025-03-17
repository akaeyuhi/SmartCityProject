from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accel_file = None
        self.gps_file = None
        self.parking_file = None
        self.accel_reader = None
        self.gps_reader = None
        self.parking_reader = None

    def startReading(self):
        self.accel_file = open(self.accelerometer_filename, "r")
        self.gps_file = open(self.gps_filename, "r")
        self.parking_file = open(self.parking_filename, "r")

        self.accel_reader = reader(self.accel_file)
        self.gps_reader = reader(self.gps_file)
        self.parking_reader = reader(self.parking_file)

        next(self.accel_reader, None)
        next(self.gps_reader, None)
        next(self.parking_reader, None)

    def read(self):
        try:
            accel_data = next(self.accel_reader)
            gps_data = next(self.gps_reader)
            parking_data = next(self.parking_reader)

            accelerometer = Accelerometer(
                x=int(accel_data[0]),
                y=int(accel_data[1]),
                z=int(accel_data[2]),
            )
            gps = Gps(
                longitude=float(gps_data[0]),
                latitude=float(gps_data[1]),
            )
            parking = Parking(
                empty_count=int(parking_data[0]),
                gps=gps
            )

            return {
                "aggregated_data": AggregatedData(
                    accelerometer=accelerometer,
                    gps=gps,
                    time=datetime.now(),
                    user_id=config.USER_ID,
                ),
                "parking_data": parking
            }

        except StopIteration:
            return None

    def stopReading(self):
        if self.accel_file:
            self.accel_file.close()
        if self.gps_file:
            self.gps_file.close()
        if self.parking_file:
            self.parking_file.close()
