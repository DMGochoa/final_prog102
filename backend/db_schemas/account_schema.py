from marshmallow import Schema, fields, EXCLUDE


class AccountSchema(Schema):
    user_id = fields.Integer(allow_none=False, required=True)
    cbu = fields.Integer(allow_none=False, required=True)
    balance = fields.Float(allow_none=False, required=True)
    id = fields.Int(allow_none=False, required=True)

    class Meta:
        unknown = EXCLUDE
