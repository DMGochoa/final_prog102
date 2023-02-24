from bank_api.database import db
from sqlalchemy import text
import random
import string

def set_username(context):
    first_name =  context.get_current_parameters()['first_name']
    last_name =  context.get_current_parameters()['last_name']
    username = f"{first_name[0]}{last_name}"
  
    # look in db for similar usernames
    username_count_query = text(f"SELECT count(*) AS count FROM Users WHERE username like '{username}%'")
    # count = db.session.execute(username_count_query).scalars().first()
    count = db.session.scalars(username_count_query).first()
    
    if count > 0:
        username = f'{username}{count+1}' 

    return username

def set_first_password(context):
    first_name =  context.get_current_parameters()['first_name']
    return first_name[:2]+''.join(random.choices(population=string.digits, k=4))

def generate_code():
    return random.randint(10000000, 99999999)

class User(db.Model):
    """
    User Flask-SQLAlchemy Model
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    type = db.Column(db.String())
    birthday = db.Column(db.Date())
    document_id = db.Column(db.String())
    country = db.Column(db.String())
    city = db.Column(db.String())
    address = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String(), default = set_first_password)
    phone_number = db.Column(db.String())
    username = db.Column(db.String(), default = set_username)
    code = db.Column(db.String(),default=generate_code)

    # def __repr__(self):
    #     return (
    #         f"**User** "
    #         f"user_id: {self.id} "
    #         f"name: {self.first_name} {self.last_name} "
    #         f"username:  {self.username}"
    #     )

