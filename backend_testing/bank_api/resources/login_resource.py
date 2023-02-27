import logging

from flask import request, jsonify, make_response
from flask_restful import Resource, abort
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from bank_api.database import db
from bank_api.models.user import User
from bank_api.schemas.user_schema import UserSchema

LOGIN_ENDPOINT = "/login"
logger = logging.getLogger(__name__)

class LoginResource(Resource):

    def post(self):
        user_stmt = select(User).where(User.username == request.get_json()["username"])
        user = db.session.execute(user_stmt).scalar_one()

        if not user:
            return {"msg": "Username doesn't exist"}, 400

        logger.debug(f"{user.username} try to login")

        if request.get_json()["password"] != user.password or request.get_json()["code"] != int(user.code):
            return {"msg": "Bad password or code"}, 400

        logger.debug(f"{user.username} login token generated ")
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=f"Bearer {access_token}")
