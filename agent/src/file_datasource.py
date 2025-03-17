from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config
import random

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.batch_size = 7
        self.files = {"accel": None, "gps": None, "parking": None}
        self.readers = {"accel": None, "gps": None, "parking": None}

    def startReading(self):
        self.files["accel"] = open(self.accelerometer_filename, "r")
        self.files["gps"] = open(self.gps_filename, "r")
        self.files["parking"] = open(self.parking_filename, "r")

        self.readers["accel"] = reader(self.files["accel"])
        self.readers["gps"] = reader(self.files["gps"])
        self.readers["parking"] = reader(self.files["parking"])

        next(self.readers["accel"], None)
        next(self.readers["gps"], None)
        next(self.readers["parking"], None)

    def _read_next(self, reader, file_key):
        try:
            return next(reader)
        except StopIteration:
            self.files[file_key].seek(0)
            next(reader, None)
            return next(reader)

    def read(self):
        data_list = []
        for _ in range(self.batch_size):
            accel_data = self._read_next(self.readers["accel"], "accel")
            gps_data = self._read_next(self.readers["gps"], "gps")
            parking_data = self._read_next(self.readers["parking"], "parking")

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

            data_list.append({
                "aggregated_data": AggregatedData(
                    accelerometer=accelerometer,
                    gps=gps,
                    time=datetime.now(),
                    user_id=config.USER_ID,
                ),
                "parking_data": parking
            })
        
        return data_list

    def stopReading(self):
        for key in self.files:
            if self.files[key]:
                self.files[key].close()
