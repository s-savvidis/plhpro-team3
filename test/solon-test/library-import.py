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


def create_sql_table(conn):
    sql_create_members_table = """CREATE TABLE IF NOT EXISTS members (
                                    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name      TEXT,
                                    age       INTEGER,
                                    occupation TEXT,
                                    tel       TEXT,
                                    email     TEXT UNIQUE
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
                                    FOREIGN KEY(member_id) REFERENCES members(member_id),
                                    FOREIGN KEY(book_id) REFERENCES books(book_id)
                                );
                                """
    try:
      cur=conn.cursor()                       # Current DB record. Get the cursor.
      cur.execute(sql_create_members_table)   # Execute the SQL Statement from Above
                                              # and create the Members table
      
      #cur=conn.cursor()
      cur.execute(sql_create_books_table)     # Create the Books table.
      
      cur.execute(sql_create_borrowing_table) # Create the Book borrowing table.
    except Error as e:
      print(e)
    return None

def sql_select_count_rec(conn):
    '''
    SQL Record count.
    '''
    cur = conn.cursor()
    #sql = ''' SELECT * FROM jira_issues '''
    
    cur.execute('SELECT * FROM members')
    rows = cur.fetchall()
    print("DB Members count: {}".format(len(rows)))

    cur.execute('SELECT * FROM books')
    rows = cur.fetchall()
    print("DB Books count: {}".format(len(rows)))


def insert_members_rec(conn, membersDict):
    '''
    Insert Members into DB.
    '''
    sql = ''' INSERT INTO members (name, age, occupation, tel, email) VALUES (?,?,?,?,?) '''
    cur = conn.cursor()
    for i in membersDict:
        cur.execute(sql, (i['full_name'],i['age'],i['occupation'],i['telephone_number'],i['email']))
    conn.commit()

def insert_books_rec(conn, booksDict):
    '''
    Insert Books into DB.
    '''
    sql = ''' INSERT INTO books (title, category, author, isbn, total_stock, current_stock) VALUES (?,?,?,?,?,?) '''
    cur = conn.cursor()
    for i in booksDict:
        cur.execute(sql, (i['book_title'],i['book_category'],i['book_author'],i['book_isbn'],i['total_stock'],i['current_stock']))
    conn.commit()

def csv_to_dict(csv_file):
    csvData = pd.read_csv(csv_file)
    csvDict = csvData.to_dict(orient='records')
    #for i in csvDict:
    #    print(i)
    return csvDict


def sql_select_count_rec(conn):
    '''
    SQL Record count.
    '''
    cur = conn.cursor()
    #sql = ''' SELECT * FROM jira_issues '''
    
    cur.execute('SELECT * FROM members')
    rows = cur.fetchall()
    print("DB Members count: {}".format(len(rows)))

    cur.execute('SELECT * FROM books')
    rows = cur.fetchall()
    print("DB Books count: {}".format(len(rows)))

class library_members():
    '''Κλάση διαχείρισης μελών.'''
    def __init__(self, member_id=0, name="", age=0, occupation="", tel="", email=""):
        self.member_id = member_id
        self.name = name
        self.age = age
        self.occupation = occupation
        self.tel = tel
        self.email = email
    
    def search_name(self, conn, memberName):
        cur = conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE name LIKE ? '''
        cur.execute(sqlQry, ('%' + memberName + '%',))
        memberRows = cur.fetchall()
        #cur.execute('SELECT * FROM members')
        
        return memberRows

    def search_id(self, conn, member_id):
        cur = conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE member_id=? '''
        cur.execute(sqlQry, (member_id,))
        memberRows = cur.fetchall()

        return memberRows

    def search_o(self, conn, member_id):
        cur = conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE member_id=? '''
        cur.execute(sqlQry, (member_id,))
        memberRows = cur.fetchall()

        return memberRows


#######################################
if __name__ == '__main__':

    conn=create_connection("./members_sqlite.db")
    
    
    '''
    libMembers = library_members()
    
    memberName = input("Όνομα μέλους: ")
    
    memberSearch = libMembers.search_name(conn, memberName)
    for i in memberSearch:
        print(i)
    
    memberID = input("Κωδικός μέλους: ")
    memberSearch = libMembers.search_id(conn, memberID)
    print(memberSearch)
    sys.exit(0)
    '''
    
    create_sql_table(conn)
    
    logging.info("Table created.")
    
    membersDict = csv_to_dict('members.csv')
    booksDict = csv_to_dict('books.csv')
    
    #for i in membersDict:
    #    print(i['full_name'],i['age'],i['occupation'],i['telephone_number'],i['email'])
    
    print("Inserting members.")
    insert_members_rec(conn, membersDict)
    
    print("Inserting Books.")
    insert_books_rec(conn, booksDict)

    sql_select_count_rec(conn)
