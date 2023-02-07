from marshmallow import Schema, fields, EXCLUDE


class UserSchema(Schema):
    first_name = fields.Str(allow_none=False)
    last_name = fields.Str(allow_none=False)
    type = fields.Str(allow_none=False)
    birthday = fields.Date(allow_none=False)
    document_id = fields.Integer(allow_none=False)
    country = fields.Str(allow_none=False)
    city = fields.Str(allow_none=False)
    address = fields.Str(allow_none=True)
    email = fields.Str(allow_none=False)
    password = fields.Str(allow_none=False)
    phone_number = fields.Int(allow_none=True)
    username = fields.Str(allow_none=False)
    code = fields.Integer(allow_none=False)
    id = fields.Int(allow_none=False)

    class Meta:
        unknown = EXCLUDE


