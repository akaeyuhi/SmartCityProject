from marshmallow import Schema, fields


class TemperatureSchema(Schema):
    value = fields.Float(required=True)
    unit = fields.Str(missing="C")