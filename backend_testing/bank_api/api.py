import logging
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from flask import Flask
from flask_restful import Api

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

from bank_api.constants import PROJECT_ROOT, BANK_DATABASE
from bank_api.database import db
from bank_api.resources.users_resource import UserResource, USERS_ENDPOINT
from bank_api.resources.login_resource import LoginResource, LOGIN_ENDPOINT

def create_app(db_location):
    """
    Function that creates our Flask application.
    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection

    :param db_location: Connection string to the database
    :return: Initialized Flask app
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("bank_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location
    db.init_app(app)
    app.config["JWT_SECRET_KEY"] = "prog102"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    api = Api(app)
    api.add_resource(UserResource, USERS_ENDPOINT)
    api.add_resource(LoginResource, LOGIN_ENDPOINT)

    with app.app_context():
        db.create_all()
        
    return app


if __name__ == "__main__":
    app = create_app(f"sqlite:///{PROJECT_ROOT}/{BANK_DATABASE}")
    app.run(host="127.0.0.1", port=9000, debug=True)