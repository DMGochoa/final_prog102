import sqlite3
# from user_schema import UserSchema
import random
import string
import os
from backend.db_schemas.user_schema import UserSchema


def generate_username(user):
    username = user.get('first_name')[0]+user.get('last_name')

    query = r"SELECT count(*) AS count FROM User WHERE username like '{0}%'".format(username)
    count = _execute(query, return_entity=False)
    if count[0]["count"] > 0:
        username = f'{username}{count[0]["count"]+1}'
    
    return username


def generate_first_password(user):
    password = user.get('first_name')[:2]+''.join(random.choices(population=string.digits,k=4))
    return password


def generate_code(user):
    code = random.randint(10000000, 99999999)
    return code


def init_db():
    _execute(
        ("""CREATE TABLE IF NOT EXISTS User (
            first_name text NOT NULL,
            last_name text NOT NULL,
            type text NOT NULL,
            birthday DATE NOT NULL,
            document_id integer NOT NULL,
            country text NOT NULL,
            city text NOT NULL,
            address text,
            email text NOT NULL,
            password text NOT NULL,
            phone_number INTEGER,
            username text NOT NULL,
            code integer NOT NULL,
            id integer PRIMARY KEY AUTOINCREMENT
            CONSTRAINT not_null_values CHECK(first_name is not NULL AND
                                            last_name is not NULL AND
                                            type is not NULL AND
                                            birthday is not NULL AND
                                            document_id is not NULL AND
                                            country is not NULL AND
                                            city is not NULL AND
                                            email is not NULL AND
                                            password is not NULL AND
                                            username is not NULL AND
                                            code is not NULL)
            CONSTRAINT valid_length CHECK(length(password)==8 AND
                                        length(code)==8))"""))


def get_all():
    return _execute("SELECT * FROM User", return_entity=False)


def get_user(id):
    user = _execute("Select * FROM User WHERE id = {}".format(id), return_entity=True)
    return user


def create(user):

    user['username']=generate_username(user)
    user['password']=generate_first_password(user)
    user['code']=generate_code(user)

    columns = ", ".join(user.keys())
    values = ", ".join("'{}'".format(value) for value in user.values())
    _execute("INSERT INTO User ({}) VALUES({})".format(columns, values))

    return user


def update(user, id):
    query = "SELECT count(*) AS count FROM User WHERE id = '{}'".format(id)
    count = _execute(query, return_entity=False)

    if count[0]["count"] == 0:
        return

    values = ["'{}'".format(value) for value in user.values()]
    update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(user.keys(), values))
    _execute("UPDATE User SET {} WHERE id = '{}'".format(update_values, id))
    return {}


def delete(id):
    count = _execute("SELECT count(*) AS count FROM User WHERE id = '{}'".format(id),
                     return_entity=False)
    if count[0]["count"] == 0:
        return
    _execute("DELETE FROM User WHERE id = '{}'".format(id))
    return {}


def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return UserSchema().load(list_of_dicts, many=True)


def _execute(query, return_entity=None):
    absolute_path = os.path.dirname(__file__)
    connection = sqlite3.connect(os.path.join(absolute_path, "testdb.sqlite"))
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


