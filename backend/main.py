from db_schemas import user_db

user = {
    "first_name": "kev",
    "last_name": "garay",
    "type": "Client",
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
user_db.create(user)
users = user_db.get_all()
print(users)
