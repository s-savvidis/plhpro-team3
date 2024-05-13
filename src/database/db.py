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
    
    def search_name(self, memberName):
        '''Αναζήτηση μέλους με τμήμα του ονόματος'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE name LIKE ? '''
        cur.execute(sqlQry, ('%' + memberName + '%',))
        memberRows = cur.fetchall()

        return memberRows
    
    def search_email(self, memEmail):
        '''Αναζήτηση μέλους βάση email'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT member_id FROM members WHERE email LIKE ? '''
        cur.execute(sqlQry, ('%' + memEmail + '%',))
        memberRows = cur.fetchall()

        return memberRows


    def search_id(self, member_id):
        '''Αναζήτηση μέλους βάση κωδικού μέλους'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE member_id=? '''
        cur.execute(sqlQry, (member_id,))
        memberRows = cur.fetchall()

        return memberRows

    def insert_member(self, memberDetails):
        '''Εισαγωγή μέλους στη βάση'''

        sql = ''' INSERT INTO members (name, age, occupation, tel, email, gender) VALUES (?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        dbConn = self.conn
        try:
            cur.execute(sql, (memberDetails['full_name'],
                              memberDetails['age'],
                              memberDetails['occupation'],
                              memberDetails['telephone_number'],
                              memberDetails['email'],
                              memberDetails['gender']
                              )
                        )
            logging.info("Εισαγωγή νέου μέλους στη βάση. {}".format(memberDetails['full_name']))
            dbConn.commit()
            
            memberId = self.search_email(memberDetails['email'])

            return memberId
        except Exception as e:
            logging.error("Πρόβλημα εισαγωγής μέλους {} στη βάση. Πρόβλημα: {}".format(memberDetails['full_name'], e))
            return False
    def update_member(self, memberDetails):
        '''Επικαιροποίηση στοιχείων μέλους'''
        sql = ''' UPDATE members SET (name, age, occupation, tel, email, gender) VALUES (?,?,?,?,?,?) WHERE member_id=? '''
        cur = self.conn.cursor()
        dbConn = self.conn
        try:
            cur.execute(sql, (memberDetails['full_name'],
                              memberDetails['age'],
                              memberDetails['occupation'],
                              memberDetails['telephone_number'],
                              memberDetails['email'],
                              memberDetails['member_id'],
                              memberDetails['gender']
                              )
                        )
            logging.info("Επικαιροποίηση στοιχείων μέλους με κωδικό {} και όνομα {}".format(memberDetails['member_id'],memberDetails['full_name']))
            dbConn.commit()
            return True
        except Exception as e:
            logging.error("Πρόβλημα επικεροποίησης στοιχείων μέλους {} στη βάση. Πρόβλημα: {}".format(memberDetails['full_name'], e))
            return False
    
    def delete_member(self, memberId):
        '''Διαγραφή μέλους βάση memberId'''
        dbConn = self.conn
        sqlQry = ''' DELETE FROM members WHERE member_id=? '''
        try:
            cur = self.conn.cursor()
            sqlQry = ''' DELETE FROM members WHERE member_id=? '''
            cur.execute(sqlQry, (memberId,))
            dbConn.commit()
            return True
        except Exception as e:
            logging.error("Αποτυχία διαγραφής μέλους με κωδικό {}. Λάθος: {}".format(memberId, e))
            return False
        
    def close_connection(self):
        self.conn.close()


