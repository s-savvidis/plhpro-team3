import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def execute_query(self, query, parameters=()):
        self.cur.execute(query, parameters)
        return self.cur.fetchall()

    def execute_statement(self, statement, parameters=()):
        self.cur.execute(statement, parameters)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
