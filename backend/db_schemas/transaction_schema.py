from marshmallow import Schema, fields, EXCLUDE


class TransactionSchema(Schema):
    origin_account = fields.Integer(allow_none=False, required=True),
    final_account = fields.Integer(allow_none=False, required=True),
    type = fields.String(allow_none=False, required=True),
    amount = fields.Float(allow_none=False, required=True),
    status = fields.Boolean(allow_none=False),
    description = fields.String(allow_none=True),
    date = fields.Date(allow_none=False, required=True)

    class Meta:
        unknown = EXCLUDE
