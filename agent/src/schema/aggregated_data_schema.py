from marshmallow import Schema, fields
from schema.accelerometer_schema import AccelerometerSchema
from schema.gps_schema import GpsSchema
from schema.parking_schema import ParkingSchema
from schema.temperature_schema import TemperatureSchema
from schema.humidity_schema import HumiditySchema
from schema.vibration_schema import VibrationSchema
from schema.light_schema import LightSchema
from schema.air_quality_schema import AirQualitySchema


class AggregatedDataSchema(Schema):
    accelerometer = fields.Nested(AccelerometerSchema)
    gps = fields.Nested(GpsSchema)
    parking = fields.Nested(ParkingSchema)
    temperature = fields.Nested(TemperatureSchema)
    humidity = fields.Nested(HumiditySchema)
    vibration = fields.Nested(VibrationSchema)
    light = fields.Nested(LightSchema)
    air_quality = fields.Nested(AirQualitySchema)
    timestamp = fields.DateTime("iso")
    user_id = fields.Int()
