import sqlite3
import os
import random
import string
## quitar / añadir backend.
from db_schemas.user_schema import UserSchema
from utils.loggin_backend import logger_backend


class UserDb:

    @classmethod
    def create(cls, user):
        logger_backend.debug(f"Creating user {user}")
        user['username'] = generate_username(user)
        user['password'] = generate_first_password(user)
        user['code'] = generate_code()

        columns = ", ".join(user.keys())
        values = ", ".join("'{}'".format(value) for value in user.values())
        _execute("INSERT INTO User ({}) VALUES({})".format(columns, values))
        logger_backend.debug("User created!")
        return user

    @classmethod
    def get_user_by_username(cls, name):
        user = _execute("Select * FROM User WHERE username = '{}'".format(name), return_entity=True)
        return user

    @classmethod
    def get_id_by_username(cls, username):
        id = _execute("SELECT id FROM User WHERE username = '{}'".format(username), return_entity=True)
        return id[0]

    @classmethod
    def get_cbu(cls, id):
        cbu = _execute("SELECT cbu FROM Transaction WHERE id = '{}'".format(id), return_entity=False)
        return cbu[0]['cbu']

    @classmethod
    def get_all(cls):
        return _execute("SELECT * FROM User", return_entity=False)

    @classmethod
    def get_user(cls, id):
        user = _execute("Select * FROM User WHERE id = {}".format(id), return_entity=True)
        return user

    @classmethod
    def update(cls, user, id):
        query = "SELECT count(*) AS count FROM User WHERE id = '{}'".format(id)
        count = _execute(query, return_entity=False)

        if count[0]["count"] == 0:
            return

        values = ["'{}'".format(value) for value in user.values()]
        update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(user.keys(), values))
        _execute("UPDATE User SET {} WHERE id = '{}'".format(update_values, id))
        return {}

    @classmethod
    def delete(cls, id):
        count = _execute("SELECT count(*) AS count FROM User WHERE id = '{}'".format(id),
                         return_entity=False)
        if count[0]["count"] == 0:
            return
        _execute("DELETE FROM User WHERE id = '{}'".format(id))
        return {}


def generate_username(user):
    username = user.get('first_name')[0]+user.get('last_name')

    query = r"SELECT count(*) AS count FROM User WHERE username like '{0}%'".format(username)
    count = _execute(query, return_entity=False)
    if count[0]["count"] > 0:
        username = f'{username}{count[0]["count"]+1}'
    
    return username


def generate_first_password(user):
    password = user.get('first_name')[:2]+''.join(random.choices(population=string.digits, k=4))
    return password


def generate_code():
    code = random.randint(10000000, 99999999)
    return code


def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return UserSchema().load(list_of_dicts, many=True)


def _execute(query, return_entity=None):

    db_name = 'bank_db.sqlite'
    absolute_path = os.path.dirname(__file__)
    db_path = os.path.join(absolute_path, '..', db_name)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

    query_result = None
    if cursor.rowcount == -1:
        query_result = _build_list_of_dicts(cursor)

    if query_result is None and return_entity:
        query_result = _convert_to_schema(query_result)

    cursor.close()
    connection.close()
    return query_result
