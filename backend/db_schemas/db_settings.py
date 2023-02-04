import mysql
from user_schema import UserSchema


def init_db():
    _execute(
        ("CREATE TABLE IF NOT EXISTS User ("
         "  first_name VARCHAR NOT NULL,"
         "  last_name VARCHAR NOT NULL,"
         "  type VARCHAR NOT NULL,"
         "  birthday DATE NOT NULL,"
         "  document_id INTEGER NOT NULL,"
         "  country VARCHAR NOT NULL,"
         "  city VARCHAR NOT NULL,"
         "  address VARCHAR,"
         "  email VARCHAR NOT NULL,"
         "  password VARCHAR NOT NULL,"
         "  phone_number INTEGER,"
         "  username VARCHAR NOTNULL,"
         "  id INT PRIMARY KEY AUTO_INCREMENT)"))



def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return UserSchema().load(list_of_dicts, many=True)


def _execute(query, return_entity=None):
    connection = mydb = mysql.connector.connect(
      host="localhost",
      port=3303,
      user="root",
      password="root")
    cursor = connection.cursor()
    cursor.execute(query)

    query_result = None
    if cursor.rowcount == -1:
        query_result = _build_list_of_dicts(cursor)

    if query_result is not None and return_entity:
        query_result = _convert_to_schema(query_result)

    cursor.close()
    connection.close()
    return query_result
