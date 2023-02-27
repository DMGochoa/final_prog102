from bank_api.resources.login_resource import LOGIN_ENDPOINT
from bank_api.resources.users_resource import USERS_ENDPOINT
from flask import jsonify

def test_login(client):
    user_json = {
            "first_name": "jhon",
            "last_name": "doe",
            "type": "user",
            "document_id": "12345678",
            "birthday": "1997-01-01",
            "country": "peru",
            "city": "lima",
            "address": "av siempreviva",
            "email": "ca@texample.com",
            "phone_number": "999555999"
    }
    user_response = client.post(f"{USERS_ENDPOINT}",json=user_json)
    login_json = {
        "username": user_response.json["username"],
        "password": user_response.json["password"],
        "code": int(user_response.json["code"])
    }
    response = client.post(f"{LOGIN_ENDPOINT}",json=login_json)
    assert response.status_code == 200
