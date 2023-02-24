from marshmallow import Schema, fields, post_load
from bank_api.models.user import User


class UserSchema(Schema):
    """
    User Marshmallow Schema
    """
    id = fields.Int(allow_none=False)
    first_name = fields.Str(allow_none=False, required=True)
    last_name = fields.Str(allow_none=False, required=True)
    type = fields.Str(allow_none=False, required=True)
    birthday = fields.Date(allow_none=False, required=True)
    document_id = fields.Str(allow_none=False, required=True)
    country = fields.Str(allow_none=False, required=True)
    city = fields.Str(allow_none=False, required=True)
    address = fields.Str(allow_none=True, required=True)
    email = fields.Str(allow_none=False, required=True)
    password = fields.Str(allow_none=False)
    phone_number = fields.Str(allow_none=False, required=True)
    username = fields.Str(allow_none=False)
    code = fields.Str(allow_none=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
