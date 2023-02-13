import sqlite3
import os


class SetupDatabase:
    db_name = 'bank_db.sqlite'
    absolute_path = os.path.dirname(__file__)
    actual_path = os.path.join(absolute_path, db_name)
    create_user_table_query = ("""CREATE TABLE IF NOT EXISTS User (
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
                CONSTRAINT valid_length CHECK(length(password)>=4 AND
                                            length(code)==8))""")
    create_account_table_query = ("""CREATE TABLE IF NOT EXISTS Account (
                user_id integer NOT NULL,
                cbu integer NOT NULL,
                balance float NOT NULL DEFAULT '0,0',
                currency string NOT NULL,
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT
                CONSTRAINT not_null_values CHECK(user_id is not NULL AND
                                                cbu is not NULL)
                CONSTRAINT valid_balance CHECK (balance >=0))""")
    create_transaction_table_query = ("""CREATE TABLE IF NOT EXISTS Transactio(
                origin_account integer NOT NULL,
                final_account integer NOT NULL,
                type string NOT NULL,
                amount float NOT NULL,
                status boolean NOT NULL DEFAULT 'TRUE',
                description string NOT NULL,
                date date NOT NULL)""")

    @classmethod
    def create_db(self):
        if not os.path.exists(self.actual_path):
            conn = sqlite3.connect(self.actual_path)
            conn.close()

    @classmethod
    def create_user_table(self): 
        conn = sqlite3.connect(self.actual_path)
        cursor = conn.cursor()
        cursor.execute(self.create_user_table_query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create_account_table(self):
        conn = sqlite3.connect(self.actual_path)
        cursor = conn.cursor()
        cursor.execute(self.create_account_table_query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def create_transaction_table(self):
        conn = sqlite3.connect(self.actual_path)
        cursor = conn.cursor()
        cursor.execute(self.create_transaction_table_query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def setup(self):
        self.create_db()
        self.create_user_table()
        self.create_account_table()
        self.create_transaction_table_query()
