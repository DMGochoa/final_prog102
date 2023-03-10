import sqlite3
import os
## quitar / añadir backend.
from db_schemas.user_schema import UserSchema
from utils.loggin_backend import logger_backend


class TransactionDB:

    @classmethod
    def create(cls, transaction):
        logger_backend.debug(f"Creating Transaction {transaction}")
        columns = ", ".join(transaction.keys())
        values = ", ".join("'{}'".format(value) for value in transaction.values())
        _execute("INSERT INTO Transactions ({}) VALUES({})".format(columns, values))
        logger_backend.debug("Transaction created!")
        return transaction

    @classmethod
    def get_done_transactions(cls, id):
        transactions = _execute("SELECT * FROM Transactions WHERE origin_account = '{}".format(id), return_entity=True)
        return transactions

    @classmethod
    def get_recived_transaction(cls, id):
        transactions = _execute("SELECT * FROM Transactions WHERE final_account = '{}".format(id), return_entity=True)
        return transactions

    @classmethod
    def report(cls, year, month, cbu):
        month_query = f"0{month}" if month < 10 else f"{month}"
        period = f"{year}-{month_query}"
        query_report = f"SELECT * FROM Transactions WHERE strftime('%Y-%m', date) = '{period}' and (origin_account = {cbu} or final_account = {cbu}) "
        transactions = _execute(query_report,return_entity=True)
        return transactions, period


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
