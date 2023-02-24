from bank_api.resources.users_resource import USERS_ENDPOINT

def test_user_create(client):
    user_json = {
            "first_name": "jhon",
            "last_name": "doe",
            "type": "client-person",
            "document_id": "12345678",
            "birthday": "1997-01-01",
            "country": "peru",
            "city": "lima",
            "address": "av siempreviva",
            "email": "ca@texample.com",
            "phone_number": "999555999"
    }
    response = client.post(f"{USERS_ENDPOINT}",json=user_json)
    assert response.status_code == 201
    assert response.json["username"] == "jdoe"


def test_user_create_with_empty_field(client):
    # no country 
    user_json = {
            "first_name": "jhon",
            "last_name": "doe",
            "type": "client-person",
            "document_id": "12345678",
            "birthday": "1997-01-01",
            "city": "lima",
            "address": "av siempreviva",
            "email": "ca@texample.com",
            "phone_number": "999555999"
    }
    response = client.post(f"{USERS_ENDPOINT}",json=user_json)
    assert response.status_code == 405
    assert response.json["errors"]["country"][0] == "Missing data for required field."