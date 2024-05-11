import sys
import logging
import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)
    
    def search_title(self, bookTitle):
        '''Αναζήτηση βιβλίου με τμήμα του τίτλου'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM books WHERE title LIKE ? '''
        cur.execute(sqlQry, ('%' + bookTitle + '%',))
        bookRows = cur.fetchall()

        return bookRows
    
    def search_author(self, bookAuthor):
        '''Αναζήτηση βιβλίων βάση συγγραφέα'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT book_id FROM books WHERE author LIKE ? '''
        cur.execute(sqlQry, ('%' + bookAuthor + '%',))
        bookRows = cur.fetchall()

        return bookRows
    
    def search_category(self, bookCategory):
        '''Αναζήτηση βιβλίων βάση κατηγορίας'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT book_id FROM books WHERE category LIKE ? '''
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
            
            bookId = bookDetails['isbn']

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
        
    def delete_book(self, bookId):
        '''Διαγραφή βιβλίου βάση bookId'''
        dbConn = self.conn
        sqlQry = ''' DELETE FROM books WHERE book_id=? '''
        try:
            cur = self.conn.cursor()
            sqlQry = ''' DELETE FROM books WHERE book_id=? '''
            cur.execute(sqlQry, (bookId,))
            dbConn.commit()
            return True
        except Exception as e:
            logging.error("Αποτυχία διαγραφής βιβλίου με κωδικό {}. Λάθος: {}".format(bookId, e))
            return False
        
    def close_connection(self):
        self.conn.close()


