from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, abort
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from backend.db_schemas import transaction_db
from db_schemas.user_schema import UserSchema
from db_schemas.user_db import UserDb
from db_schemas.account_schema import AccountSchema
from backend.db_schemas.account_db import AccountDb
from utils.loggin_backend import logger_backend
from setup_db import SetupDatabase

app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "prog102"
jwt = JWTManager(app)


class User(Resource):

    def post(self):
        try:
            logger_backend.debug(f"POST '/users' {request.json} ")
            user = UserSchema().load(request.json)
            user_db = UserDb.create(user)
            user_id = UserDb.get_user_by_username(user_db['username'])[0]['id']
            account = AccountDb.create(user_id=user_id)
            logger_backend.debug(f"Create account {account['cbu']}")
            return {
                       "username": user_db['username'],
                       "password": user_db['password'],
                       "code": user_db['code'],
                       "account_cbu": account['cbu']
                   }, 201

        except ValidationError as e:
            logger_backend.debug(f"Validation error:  {e.messages} ")
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
        logger_backend.debug(f"{user_db[0]['username']} try to login")
        if not user_db:
            return {"msg": "Username doesn't exist"}, 400

        if password != user_db[0]['password'] or code != user_db[0]['code']:
            return {"msg": "Bad password or code"}, 400

        logger_backend.debug(f"{user_db[0]['username']} login token generated ")
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


class Account(Resource):
    # create new account

    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        user_id = UserDb.get_user_by_username(username)[0]['id']
        account = AccountDb.create(user_id=user_id)
        logger_backend.debug(f"Create new account by {username}, cbu : {account['cbu']} ")
        return jsonify(account=account)
    # get all accounts by current user

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        logger_backend.debug(f"{username} client try to see theirs accounts")
        user_id = UserDb.get_user_by_username(username)[0]['id']
        accounts = AccountDb.get_accounts_by_userid(user_id)
        return jsonify(accounts=accounts)


api.add_resource(Account, "/accounts")


class Transaction(Resource):

    def post(self):
        transaction_type = request.json.get("transaction_type", None)
        cbu_origin = request.json.get("cbu_origin", None)
        cbu_destiny = request.json.get("cbu_destiny", None)
        amount = request.json.get("amount", None)
        description = request.json.get("description", None)
        # username = get_jwt_identity()
        # user_id = UserDb.get_user_by_username(username)[0]['id']
        try:
            origin = AccountDb.transaction(cbu_origin, cbu_destiny, amount, transaction_type, description)
            logger_backend.debug(f"{cbu_origin} added  $ {amount} to cbu : {cbu_destiny} ")
            return jsonify(cbu_origin=cbu_origin, origin_new_balance=origin, cbu_destiny=cbu_destiny, amount=amount,
                           description=description)
        except:
            return make_response(jsonify(msg="Error with account destiny or ammount"), 400)


api.add_resource(Transaction,  "/transaction")


if __name__ == "__main__":
    SetupDatabase.setup()
    app.run(host="127.0.0.1", port=9000, debug=True)
