from marshmallow import Schema, fields, EXCLUDE


class UserSchema(Schema):
    first_name = fields.Str(allow_none=False, required=True)
    last_name = fields.Str(allow_none=False, required=True)
    type = fields.Str(allow_none=False, required=True)
    birthday = fields.Date(allow_none=False, required=True)
    document_id = fields.Integer(allow_none=False, required=True)
    country = fields.Str(allow_none=False, required=True)
    city = fields.Str(allow_none=False, required=True)
    address = fields.Str(allow_none=True, required=True)
    email = fields.Str(allow_none=False, required=True)
    password = fields.Str(allow_none=False)
    phone_number = fields.Int(allow_none=True, required=True)
    username = fields.Str(allow_none=False)
    code = fields.Integer(allow_none=False)
    id = fields.Int(allow_none=False)

    class Meta:
        unknown = EXCLUDE


