from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accel_file = None
        self.gps_file = None
        self.accel_reader = None
        self.gps_reader = None

    def startReading(self):
        self.accel_file = open(self.accelerometer_filename, "r")
        self.gps_file = open(self.gps_filename, "r")

        self.accel_reader = reader(self.accel_file)
        self.gps_reader = reader(self.gps_file)

        next(self.accel_reader, None)
        next(self.gps_reader, None)

    def read(self) -> AggregatedData:
        try:
            accel_data = next(self.accel_reader)
            gps_data = next(self.gps_reader)

            accelerometer = Accelerometer(
                x=int(accel_data[0]),
                y=int(accel_data[1]),
                z=int(accel_data[2]),
            )
            gps = Gps(
                longitude=float(gps_data[0]),
                latitude=float(gps_data[1]),
            )

            return AggregatedData(
                accelerometer=accelerometer,
                gps=gps,
                time=datetime.now(),
                user_id=config.USER_ID,
            )
        except StopIteration:
            return None

    def stopReading(self):
        if self.accel_file:
            self.accel_file.close()
        if self.gps_file:
            self.gps_file.close()
