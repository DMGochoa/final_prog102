from flask import Flask, request
from flask_restful import Resource, Api, abort
from marshmallow import ValidationError

from db_schemas.user_db import UserDb
from db_schemas.user_schema import UserSchema

from setup_db import SetupDatabase

app = Flask(__name__)
api = Api(app)

class User(Resource):

    def post(self):
        try:
            user = UserSchema().load(request.json)
            userdb = UserDb.create(user)
            return {
                "username": userdb['username'],
                "password": userdb['password'],
                "code": userdb['code']
            }, 201
                
        except ValidationError as e:
             abort(405, errors=e.messages)

    # def get(self, id=None):
    #     if id is None:
    #         return user_db.get_all()

    #     user = user_db.get_user(id)
    #     if not user:
    #         abort(404, errors={"errors": {"message": "User with Id {} does not exist".format(id)}})
    #     return user

#     def put(self, id):
#         try:
#             user = UserSchema().load(request.json)
#             if user_db.update(user, id):
#                 abort(404, errors={"errors": {"message": "User with Id {} does not exist".format(id)}})
#         except ValidationError as e:
#             abort(405, errors=e.messages)
    


api.add_resource(User, "/users", "/user/<int:id>")

if __name__ == "__main__":
    SetupDatabase.setup()
    app.run(host="127.0.0.1", port=9000, debug=True)
