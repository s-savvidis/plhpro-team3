#!/usr/bin/env python3

import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

logging.basicConfig(level=logging.DEBUG)


class library_db_init():
    def __init__(self, conn):
        self.conn = conn
    
    def csv_to_dict(self, csv_file):
        '''Read CSV and convert to Dictionary using Pandas'''
        try:
            csvData = pd.read_csv(csv_file)
            csvDict = csvData.to_dict(orient='records')
            return csvDict
        except Exception as e:
            logging.error("Error import csv_file: {} Error: {}".format(csv_file, e))
            return False

    def insert_members_rec(self, membersDict):
        '''
        Insert Members into DB.
        '''
        sql = ''' INSERT INTO members (name, age, occupation, tel, email, gender) VALUES (?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        dbConn = self.conn
        for i in membersDict:
            cur.execute(sql, (i['full_name'],i['age'],i['occupation'],i['telephone_number'],i['email'],i['gender']))
            logging.info("Importing member {}".format(i['full_name']))
        dbConn.commit()
    
    def insert_books_rec(self, booksDict):
        '''
        Insert Books into DB.
        '''
        dbConn = self.conn
        sql = ''' INSERT INTO books (title, category, author, isbn, total_stock, current_stock) VALUES (?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        for i in booksDict:
            cur.execute(sql, (i['book_title'],i['book_category'],i['book_author'],i['book_isbn'],i['total_stock'],i['current_stock']))
            logging.info("Importing book {}".format(i['book_title']))
        dbConn.commit()    

    def insert_borrowings_rec(self, borrowingsDict):
        '''
        Insert Borrowings into DB.
        '''
        dbConn = self.conn
        sql = ''' INSERT INTO borrowings (book_id, member_id, date, return_status, rating) VALUES (?,?,?,?,?) '''
        cur = self.conn.cursor()
        for i in borrowingsDict:
            cur.execute(sql, (i['book_id'],i['member_id'],i['borrow_date'],i['return_status'],i['rating']))
            logging.info("Importing borrowing for date {}".format(i['borrow_date']))
        dbConn.commit()    


    def import_members(self, csv_file):
        '''Import Members records into DB'''
        membersDict = self.csv_to_dict(csv_file)
        self.insert_members_rec(membersDict)

    def import_books(self, csv_file):
        '''Import Book records into DB'''
        booksDict = self.csv_to_dict(csv_file)
        self.insert_books_rec(booksDict)

    def import_borrowings(self, csv_file):
        '''Import Borrowing records into DB'''
        borrowingsDict = self.csv_to_dict(csv_file)
        self.insert_borrowings_rec(borrowingsDict)

    
    def create_db_tables(self):
        '''Create DB tables if they do not exist'''
        sql_create_members_table = """CREATE TABLE IF NOT EXISTS members (
                                        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name      TEXT,
                                        age       INTEGER,
                                        occupation TEXT,
                                        tel       TEXT,
                                        email     TEXT UNIQUE,
                                        gender    TEXT
                                    );
                                    """
        sql_create_books_table = """CREATE TABLE IF NOT EXISTS books (
                                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        title     TEXT,
                                        category  TEXT,
                                        author    TEXT,
                                        isbn      INT NOT NULL UNIQUE,
                                        total_stock INT NOT NULL,
                                        current_stock INT NOT NULL
                                    );
                                    """
        
        sql_create_borrowing_table = """CREATE TABLE IF NOT EXISTS borrowings (
                                        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        book_id   INTEGER NOT NULL,
                                        member_id INTEGER NOT NULL,
                                        date      TEXT NOT NULL,
                                        return_status INTEGER,
                                        rating    INTEGER,
                                        FOREIGN KEY(member_id) REFERENCES members(member_id),
                                        FOREIGN KEY(book_id) REFERENCES books(book_id)
                                    );
                                    """
        try:
          cur=self.conn.cursor()                  # Current DB record. Get the cursor.
          cur.execute(sql_create_members_table)   # Execute the SQL Statement from Above
                                                  # and create the Members table
          cur.execute(sql_create_books_table)     # Create the Books table.
          cur.execute(sql_create_borrowing_table) # Create the Book borrowing table.
        except Error as e:
          logging.error("Error creating tables. Error: {}".format(e))
        return None

    def db_count_rec(self):
        '''DB Record count.'''
        cur = self.conn.cursor()
        
        cur.execute('SELECT * FROM members')
        rows = cur.fetchall()
        memberCount = len(rows)
    
        cur.execute('SELECT * FROM books')
        rows = cur.fetchall()
        bookCount = len(rows)
        
        return memberCount, bookCount

def help_info():
    print("Library DB Init module.")
    print("Usage: ")
    print("library-db-init.py: ")
    print("  -d, --db : Library Database filename and path.")
    print("  -m, --members : Αρχείο csv με στοιχεία μελών.")
    print("  -b, --books  : Αρχείο csv με στοιχεία βιβλίων.")
    print("  -o, --borrowings : Αρχείο CSV με στοιχεία δανεισμών.")
    print("-*"*25)
    print("Παράδειγμα:")
    print("library-db-init.py -d=../../../members_sqlite.db -m=members.csv -b=books.csv -o=borrowings.csv")
    print("library-db-init.py --db=../../../members_sqlite.db --members=members.csv --books=books.csv --borrowings=borrowings.csv")
    

#######################################
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', help='SQLite3 DB filename. e.g. -d ../../../members_sqlite.db', default="../../../members_sqlite.db")
    parser.add_argument('-m', '--members', help='Members init CSV file. e.g. -m=members.csv')
    parser.add_argument('-b', '--books', help='Books init CSV file. e.g. -b=books.csv')
    parser.add_argument('-o', '--borrowings', help='Borrowings init CSV file. e.g. -o=borrowings.csv')
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.db)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.db, e))
        sys.exit(1)
    
    sqlDb = library_db_init(conn)
    logging.info("Initialising DB")
    
    sqlDb.create_db_tables()
    
    logging.info("Importing Members")
    if args.members:
        sqlDb.import_members(args.members)

    logging.info("Importing Books")
    if args.books:
        sqlDb.import_books(args.books)

    logging.info("Importing Borrowings")
    if args.borrowings:
        sqlDb.import_borrowings(args.borrowings)
    