import sqlite3
from backend.db_schemas.user_schema import UserSchema


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
            id integer PRIMARY KEY)"""))


def get_all():
    return _execute("SELECT * FROM User", return_entity=False)


def get_user(id):
    user = _execute("Select * FROM User WHERE id = {}".format(id), return_entity=True)
    return user


def create(user):
    username = user.get("username")
    query = r"SELECT count(*) AS count FROM User WHERE username = '{0}'".format(username)
    count = _execute(query, return_entity=False)

    if count[0]["count"] > 0:
        return

    columns = ", ".join(user.keys())
    values = ", ".join("'{}'".format(value) for value in user.values())
    _execute("INSERT INTO User ({}) VALUES({})".format(columns, values))

    return {}


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
    connection = sqlite3.connect('bank_db')
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


