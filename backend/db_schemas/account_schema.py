from marshmallow import Schema, fields, EXCLUDE


class AccountSchema(Schema):
    user_id = fields.Integer(allow_none=False)
    cbu = fields.Integer(allow_none=False)
    balance = fields.Float(allow_none=False)
    id = fields.Int(allow_none=False)

    class Meta:
        unknown = EXCLUDE
