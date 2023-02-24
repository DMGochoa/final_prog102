import logging

from flask import request, jsonify, make_response
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError


from bank_api.database import db
from bank_api.models.user import User
from bank_api.schemas.user_schema import UserSchema

USERS_ENDPOINT = "/users"
logger = logging.getLogger(__name__)

class UserResource(Resource):

    def post(self):
        """
        UserResource POST method. Adds a new User to the database.
        """
        try:
            user = UserSchema().load(request.get_json())
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(
                username = user.username,
                password = user.password,
                code = user.code),
                201)

        except ValidationError as e:
            logger.warning(f"Validation error:  {e.messages} ")
            abort(405, errors=e.messages)
