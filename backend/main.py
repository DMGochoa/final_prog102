from db_schemas import user_db

user = {
    "first_name": "kristian",
    "last_name": "ev",
    "type": "client-person",
    "birthday": '16/03/1998',
    "document_id": "1234567890",
    "country": "bolivia",
    "city": "cochabamba",
    "address": "fake address...",
    "email": "kev@mail.com",
    "password": "32435643",
    "phone_number": "34546543",
    "username": "kev"
}

# user_db.init_db()
# user_db.create(user)
user = user_db.get_user_by_username('jmendoza')
# users = user_db.get_all()
print(user)
