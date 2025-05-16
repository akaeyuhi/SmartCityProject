from marshmallow import Schema, fields


class VibrationSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)
    magnitude = fields.Method("get_magnitude")

    def get_magnitude(self, obj):
        return (obj.x ** 2 + obj.y ** 2 + obj.z ** 2) ** 0.5