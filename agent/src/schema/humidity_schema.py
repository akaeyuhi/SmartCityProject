from marshmallow import Schema, fields


class HumiditySchema(Schema):
    value = fields.Float(required=True)
    unit = fields.Str(missing="%")