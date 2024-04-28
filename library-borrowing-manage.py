#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        #sqVer = sqlite3.version
        #logging.info(sqVer)
        return conn
    except Error as e:
        logging.error(e)
        sys.exit(1)

class library_borrowings():
    '''Κλάση διαχείρισης δανεισμών.'''
    def __init__(self, conn):
        self.conn = conn
    
    def borrow_book(self, member_id, book_id):
        cur = self.conn.cursor()

        # Αναζήτηση διαθεσιμότητας βιβλίου
        cur.execute('''SELECT current_stock FROM books WHERE id = ?''', (book_id,))
        stock = cur.fetchone()[0]
        if stock == 0:
            return False

        else:
            # Ανανεώνουμε το απόθεμα
            cur.execute('''UPDATE books SET current_stock = current_stock - 1 WHERE id = ?''', (book_id,))

            # Εισάγουμε τον δανεισμό στην βάση δεδομένων
            cur.execute('''INSERT INTO borrowing (member_id, book_id, date, return_status) VALUES (?, ?, CURRENT_DATE, 0)''', (member_id, book_id))

            return True  
    
    def return_book(self, member_id, book_id):
        cur = self.conn.cursor()
        
        # Ανανεώνουμε το απόθεμα
        cur.execute('''UPDATE books SET current_stock = current_stock + 1 WHERE id = ?''', (book_id,))

        # Ανανεώνουμε την βάση δεδομένων κατά την επιστροφή του βιβλίου
        cur.execute('''UPDATE borrowing SET return_status = 1 WHERE member_id = ? AND book_id = ? AND return_status = 0''', (member_id, book_id))
        
        # Εισαγωγή rating (?????)    
        
if __name__ == '__main__':
    import argparse
    
    newBook={}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="borrowing_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)        
        
        
        