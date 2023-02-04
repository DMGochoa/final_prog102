from backend.db_schemas import user_db

user = {
    "first_name": 'Laura',
    "last_name": "Meneses",
    "type": "Client",
    "birthday": '16/03/1998',
    "document_id": "1234567890",
    "country": "bolivia",
    "city": "cochabamba",
    "address": "fakea ddress...",
    "email": "jdbjhf@mail.com",
    "password": "32435643",
    "phone_number": 34546543,
    "username": "lmeneses"
}

user_db.create(user)
users = user_db.get_all()
print(users)
