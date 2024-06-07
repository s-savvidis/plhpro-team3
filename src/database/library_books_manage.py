#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

logging.basicConfig(level=logging.DEBUG)



class library_books():
    '''Κλάση διαχείρισης βιβλίων.'''
    def __init__(self, database):
        #self.conn = conn
        try:
            self.conn = sqlite3.connect(database)
        except Exception as e:
            logging.error("Error Establishing connection to db {}. Error: {}".format(database, e))
            sys.exit(1)
    
    def search_title(self, bookTitle):
        '''Αναζήτηση βιβλίου με τμήμα του τίτλου'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM books WHERE title LIKE ? '''
        cur.execute(sqlQry, ('%' + bookTitle + '%',))
        bookRows = cur.fetchall()
        print(bookRows)
        return bookRows
    
    def search_author(self, bookAuthor):
        '''Αναζήτηση βιβλίων βάση συγγραφέα'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM books WHERE author LIKE ? '''
        cur.execute(sqlQry, ('%' + bookAuthor + '%',))
        bookRows = cur.fetchall()

        return bookRows
    
    def search_category(self, bookCategory):
        '''Αναζήτηση βιβλίων βάση κατηγορίας'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM books WHERE category LIKE ? '''
        cur.execute(sqlQry, ('%' + bookCategory + '%',))
        bookRows = cur.fetchall()

        return bookRows


    def search_isbn(self, bookISBN):
        '''Αναζήτηση βιβλίου βάση ISBN'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM books WHERE isbn=? '''
        cur.execute(sqlQry, (bookISBN,))
        bookRows = cur.fetchall()

        return bookRows
    
    def delete_book(self, bookId):
        '''Διαγραφή βιβλίου βάση bookId'''
        cur = self.conn.cursor()
        sqlQry = ''' DELETE FROM books WHERE book_id=? '''
        cur.execute(sqlQry, (bookId,))
        self.conn.commit()

    def insert_book(self, bookDetails):
        '''Εισαγωγή βιβλίου στη βάση'''

        sql = ''' INSERT INTO books (title, category, author, isbn, total_stock, current_stock) VALUES (?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        dbConn = self.conn
        try:
            cur.execute(sql, (bookDetails['title'],
                              bookDetails['category'],
                              bookDetails['author'],
                              bookDetails['isbn'],
                              bookDetails['total_stock'],
                              bookDetails['current_stock']
                              )
                        )
            logging.info("Εισαγωγή νέου βιβλίου στη βάση. {}".format(bookDetails['title']))
            dbConn.commit()
            
            bookId = self.search_(bookDetails['isbn'])

            return bookId
        except Exception as e:
            logging.error("Πρόβλημα εισαγωγής βιβλίου {} στη βάση. Πρόβλημα: {}".format(bookDetails['title'], e))
            return False
        
    def update_book(self, bookDetails):
        '''Επικαιροποίηση στοιχείων βιβλίου'''
        sql = ''' UPDATE books SET title=?, category=?, author=?, isbn=?, total_stock=?, current_stock=? WHERE book_id=? '''
        cur = self.conn.cursor()
        dbConn = self.conn
        try:
            cur.execute(sql, (bookDetails['title'],
                            bookDetails['category'],
                            bookDetails['author'],
                            bookDetails['isbn'],
                            bookDetails['total_stock'],
                            bookDetails['current_stock'],
                            bookDetails['book_id']
                            )
                        )
            logging.info("Επικαιροποίηση στοιχείων βιβλίου με κωδικό {} και τίτλο {}".format(bookDetails['book_id'],bookDetails['title']))
            dbConn.commit()
            return True
        except Exception as e:
            logging.error("Πρόβλημα επικεροποίησης στοιχείων βιβλίου {} στη βάση. Πρόβλημα: {}".format(bookDetails['title'], e))
            return False   

#######################################
if __name__ == '__main__':
    import argparse
    
    newBook={}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="books_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)
        
    libBooks = library_books(conn)
    
    
    ###### Εισαγωγή βιβλίου
    print()
    print("Εισαγωγή νέου βιβλίου:###########")
    newBook['title'] = input("Τίτλος βιβλίου: ")
    newBook['category'] = input("Κατηγορία: ")
    newBook['author'] = input("Συγγραφέας: ")
    newBook['isbn'] = input("ISBN: ")
    newBook['total_stock'] = input("Συνολικό απόθεμα: ")
    newBook['current_stock'] = input("Απόθεμα: ")
    
    insertResult = libBooks.insert_book(newBook)
    if not insertResult:
        print("Αποτυχία εισαγωγής νέου βιβλίου.")
        sys.exit(1)
    else:
        print("Κωδικός νέου βιβλίου {}".format(insertResult))
    

    print("Αναζήτηση βιβλίου.")    
    bookTitle = input("Τίτλος βιβλίου: ")
    
    bookSearch = libBooks.search_title(bookTitle)
    if bookSearch == []:
        print("Tο βιβλίο δε βρέθηκε.")
        sys.exit(0)
    else:
        for i in bookSearch:
            print(i)
    
    bookID = input("Επιλέξτε κωδικό βιβλίου: ")
    bookSearch = libBooks.search_id(bookID)
    print("Πληροφορίες βιβλίου")
    print("Κωδικός βιβλίου: {}".format(bookSearch[0][0]))
    
    sys.exit(0)
