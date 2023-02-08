import sqlite3
import os

class SetupDatabase():
    db_name='bank_db.sqlite'
    absolute_path = os.path.dirname(__file__)
    actualpath=os.path.join(absolute_path,db_name)

    create_user_table_query = """
            CREATE TABLE IF NOT EXISTS User (
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
            id integer PRIMARY KEY AUTOINCREMENT)"""

    @classmethod
    def create_db(self):
        if not os.path.exists(self.actualpath):
            conn=sqlite3.connect(self.actualpath)
            conn.close()

    @classmethod
    def create_user_table(self):
        conn=sqlite3.connect(self.actualpath)
        cursor = conn.cursor()
        cursor.execute(self.create_user_table_query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def setup(self):
        self.create_db()
        self.create_user_table()
