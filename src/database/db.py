import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def execute_query(self, query, parameters=()):
        self.cur.execute(query, parameters)
        return self.cur.fetchall()

    def execute_statement(self, statement, parameters=()):
        self.cur.execute(statement, parameters)
        self.conn.commit()

    def search_title(self, bookTitle):
        '''Αναζήτηση βιβλίου με τμήμα του τίτλου'''
        
        sqlQry = ''' SELECT * FROM books WHERE title LIKE ? '''
        self.cur.execute(sqlQry, ('%' + bookTitle + '%',))
        bookRows = self.cur.fetchall()

        return bookRows

    def close_connection(self):
        self.conn.close()
