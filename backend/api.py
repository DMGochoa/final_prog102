from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from db_schemas.user_schema import UserSchema
from marshmallow import ValidationError
from db_schemas.user_db import UserDb
from setup_db import SetupDatabase

app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "prog102"
jwt = JWTManager(app)

class User(Resource):

    def post(self):
        try:
            user = UserSchema().load(request.json)
            user_db = UserDb.create(user)
            return {
                       "username": user_db['username'],
                       "password": user_db['password'],
                       "code": user_db['code']
                   }, 201

        except ValidationError as e:
            abort(405, errors=e.messages)

    def get(self, id=None):
        if id is None:
            return UserDb.get_all()

        user = UserDb.get_user(id)
        if not user:
            abort(404, errors={"errors": {"message": "User with Id {} does not exist".format(id)}})
        return user

    def put(self, id):
        try:
            user = UserSchema().load(request.json)
            if UserDb.update(user, id):
                abort(404, errors={"errors": {"message": "User with Id {} does not exist".format(id)}})
        except ValidationError as e:
            abort(405, errors=e.messages)


api.add_resource(User, "/users", "/user/<int:id>")


class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        code = request.json.get("code", None)

        user_db = UserDb.get_user_by_username(username)

        if not user_db:
            return {"msg": "Username doesn't exist"}, 400

        if password != user_db[0]['password'] or code != user_db[0]['code']:
            print(code)
            print(user_db[0]['code'])
            return {"msg": "Bad password or code"}, 400

        access_token = create_access_token(identity=username)
        return jsonify(access_token=f"Bearer {access_token}")


api.add_resource(Login, "/login")


class Homepage(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user_db = UserDb.get_user_by_username(username)

        return jsonify(user=user_db)


api.add_resource(Homepage, "/home")


if __name__ == "__main__":
    SetupDatabase.setup()
    app.run(host="127.0.0.1",port=9000)
