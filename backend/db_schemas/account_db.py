import sqlite3
import os
import random
import string
from backend.db_schemas.account_schema import AccountSchema


class AccountDb:

    @classmethod
    def create(cls, user_id):
        account = AccountSchema().load({"user_id": user_id})
        account['cbu'] = generate_cbu(user_id)
        account['balance'] = 0.0
        account['currency'] = "local"
        columns = ", ".join(account.keys())
        values = ", ".join("'{}'".format(value) for value in account.values())
        _execute("INSERT INTO Account ({}) VALUES({})".format(columns, values))
        return account

    @classmethod
    def get_accounts_by_userid(cls, user_id):
        query = r"SELECT * FROM Account WHERE user_id  = {0}".format(user_id)
        return _execute(query, return_entity=False)

    @classmethod
    def add_money_to_account(cls,cbu,amount):
        query = r"SELECT balance from Account WHERE cbu = '{}'".format(cbu)
        balance = _execute(query, return_entity=False)[0]['balance']
        new_balance = balance+amount
        update_balance_query = r"UPDATE Account SET balance = {} WHERE cbu = {}".format(new_balance,cbu)
        update_balance = _execute(update_balance_query)
        return new_balance

    @classmethod
    def get_user(cls, id):
        account = _execute("SELECT * FROM Account WHERE id = {}".format(id), return_entity=True)
        return account

    @classmethod
    def get_balance(cls, id):
        balance = "SELECT balance FROM Account WHERE id = {}".format(id, return_entity=True)
        return balance

    @classmethod
    def update(cls, account, id):
        query = "SELECT count(*) AS count FROM Account WHERE id = '{}'".format(id)
        count = _execute(query, return_entity=False)

        if count[0]["count"] == 0:
            return

        values = ["'{}'".format(value) for value in account.values()]
        update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(account.keys(), values))
        _execute("UPDATE Account SET {} WHERE id = '{}'".format(update_values, id))
        return {}

    @classmethod
    def delete(cls, id):
        count = _execute("SELECT count(*) AS count FROM Account WHERE id = '{}'".format(id),
                         return_entity=False)
        if count[0]["count"] == 0:
            return
        _execute("DELETE FROM Account WHERE id = '{}'".format(id))
        return {}


def generate_cbu(user_id):
    query = r"SELECT count(*) AS count FROM Account WHERE user_id  = {0}".format(user_id)
    count = _execute(query, return_entity=False)
    cbu = 10200000000 + user_id*10000 + count[0]["count"]+1
    return cbu


def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return AccountSchema().load(list_of_dicts, many=True)


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
