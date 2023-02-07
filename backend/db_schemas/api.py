from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError

from user_schema import UserSchema
import user_db

app = Flask(__name__)
api = Api(app)


def initialize_database():
    user_db.init_db()


class User(Resource):

    def get(self, id=None):
        if id is None:
            return user_db.get_all()

        user = user_db.get_user(id)
        if not user:
            abort(404, errors={"errors": {"message": "User with Id {} does not exist".format(id)}})
        return user

    def put(self, id):
        try:
            user = UserSchema().load(request.json)
            if user_db.update(user, id):
                abort(404, errors={"errors": {"message": "User with Id {} does not exist".format(id)}})
        except ValidationError as e:
            abort(405, errors=e.messages)
    
    def post(self):
        try:
            user = UserSchema().load(request.json)
            user = user_db.create(user)
            return {
                "username": user['username'],
                "password": user['password'],
                "code": user['code']
            }, 201
                
        except ValidationError as e:
            abort(405, errors=e.messages)

api.add_resource(User, "/users", "/user/<int:id>")

if __name__ == "__main__":
    app.run(host="127.0.0.1")
