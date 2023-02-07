from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError

from backend.db_schemas import user_db
from backend.db_schemas import user_schema as UserSchema

app = Flask(__name__)
api = Api(app)


# def initialize_database():
#     user_db.init_db()


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


api.add_resource(User, "/users", "/user/<int:id>")

if __name__ == "__main__":
    app.run(host="127.0.0.1")
