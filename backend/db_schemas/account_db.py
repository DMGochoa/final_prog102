import sqlite3
import os
import datetime
## quitar / añadir backend.
from backend.db_schemas.account_schema import AccountSchema
from backend.db_schemas.transaction_db import TransactionDB


class AccountDb:

    @classmethod
    def create(cls, user_id):
        account = AccountSchema().load({"user_id": user_id})
        account['cbu'] = generate_cbu(user_id)
        account['balance'] = 0.0
        account['currency'] = "local"
        account['creation_date'] = datetime.date.today()
        columns = ", ".join(account.keys())
        values = ", ".join("'{}'".format(value) for value in account.values())
        _execute("INSERT INTO Account ({}) VALUES({})".format(columns, values))
        return account

    @classmethod
    def get_accounts_by_userid(cls, user_id):
        query = r"SELECT * FROM Account WHERE user_id  = {0}".format(user_id)
        return _execute(query, return_entity=False)

    @classmethod
    def get_account_by_cbu(cls, cbu):
        query = r"SELECT * FROM Account WHERE cbu  = {}".format(cbu)
        return _execute(query, return_entity=False)

    @classmethod
    def transaction(cls, cbu_origin, cbu_destiny, amount, transaction_type, description):
        destiny_query = r"SELECT balance from Account WHERE cbu = '{}'".format(cbu_destiny)
        destiny_balance = _execute(destiny_query, return_entity=False)[0]['balance']

        if cls.get_account_by_cbu(cbu_origin):
            transaction_type = "transaction"
            query = r"SELECT balance from Account WHERE cbu = '{}'".format(cbu_origin)
            balance = _execute(query, return_entity=False)[0]['balance']
            if balance < amount:
                raise Exception("The amount to withdraw is bigger than current balance")
            new_origin_balance = balance - amount
            update_balance_query_origin = r"UPDATE Account SET balance = {} WHERE cbu = {}".format(new_origin_balance,
                                                                                                   cbu_origin)
            _execute(update_balance_query_origin)
            new_destiny_balance = destiny_balance + amount
        if transaction_type == "deposit":
            new_destiny_balance = destiny_balance + amount
            new_origin_balance = new_destiny_balance
        if transaction_type == "withdraw":
            if destiny_balance < amount:
                raise Exception("The amount to withdraw is bigger than current balance")
            new_destiny_balance = destiny_balance - amount
            new_origin_balance = new_destiny_balance

        update_balance_query_destiny = r"UPDATE Account SET balance = {} WHERE cbu = {}".format(new_destiny_balance,
                                                                                                cbu_destiny)
        _execute(update_balance_query_destiny)
        transaction = {
            "origin_account": cbu_origin,
            "final_account": cbu_destiny,
            "type": transaction_type,
            "amount": amount,
            "status": True,
            "description": description,
            "date": datetime.date.today()
        }
        TransactionDB.create(transaction)
        return new_origin_balance

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
    cbu = 10200000000 + user_id * 10000 + count[0]["count"] + 1
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
