from marshmallow import Schema, fields


class LightSchema(Schema):
    illumination = fields.Float(required=True)
