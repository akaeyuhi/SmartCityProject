from marshmallow import Schema, fields


class AirQualitySchema(Schema):
    pm2_5 = fields.Float(required=True)
    pm10 = fields.Float(required=True)
    aqi = fields.Int(required=False)