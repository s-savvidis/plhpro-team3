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
        sql = '''UPDATE members SET name=?, age=?, occupation=?, tel=?, email=?, gender=? WHERE member_id=?'''
        cur = self.conn.cursor()
        dbConn = self.conn
        
        try:
            cur.execute(sql, (memberDetails['full_name'],
                              memberDetails['age'],
                              memberDetails['occupation'],
                              memberDetails['telephone_number'],
                              memberDetails['email'],
                              memberDetails['gender'],  
                              memberDetails['member_id']
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
    
    
    def search_borrowing(self, member_id=None):
        '''Search borrowings based on the member_id.'''
        cur = self.conn.cursor()
        if member_id:
            # When member_id is provided, search only for that specific member
            sqlQry = '''SELECT * FROM borrowings WHERE member_id = ? ORDER BY date DESC'''
            cur.execute(sqlQry, (member_id,))
        else:
            # When member_id is not provided, retrieve all borrowings
            sqlQry = '''SELECT * FROM borrowings ORDER BY date DESC'''
            cur.execute(sqlQry)
        borrowingRows = cur.fetchall()
        return borrowingRows
    
        
    def borrow_book(self, member_id, book_id, borrow_date):
        cur = self.conn.cursor()

        # Αναζήτηση διαθεσιμότητας βιβλίου
        cur.execute('''SELECT current_stock FROM books WHERE book_id = ?''', (book_id,))
        stock = cur.fetchone()[0]
        if stock == 0:
            return False

        else:
            # Ανανεώνουμε το απόθεμα
            try:
                cur.execute('''UPDATE books SET current_stock = current_stock - 1 WHERE book_id = ?''', (book_id,))
                logging.info("Επιτυχία μείωσης αποθέματος βιβλίου με κωδικό: {}".format(book_id)) 
            except Exception as e:
                logging.error("Αποτυχία ενημέρωσης stock βιβλίου book_id {}".format(book_id))
                return False       
            
            # Εισάγουμε τον δανεισμό στην βάση δεδομένων
            try:
                cur.execute('''INSERT INTO borrowings (member_id, book_id, date, return_status, rating) VALUES (?, ?, ?, 0, ?)''', (member_id, book_id, borrow_date, 0))
                dbConn = self.conn
                dbConn.commit()
                logging.info("Επιτυχία δανεισμού βιβλίου με κωδικό: {}".format(book_id,))
                return True  
            except Exception as e:
                logging.error("Αποτυχία δανεισμού βιβλίου με κωδικό: {}".format(book_id,))
                return False
   
   
   
   
   
   
    def return_book(self, member_id, book_id, book_rating):
        
        cur = self.conn.cursor()
        
        try:
            cur.execute('''SELECT borrow_id FROM borrowings WHERE member_id = ? AND book_id = ? AND return_status = 0''', (member_id, book_id))
            borrowing_id = cur.fetchone()[0]
        except Exception as e:
            logging.error("Αποτυχία αναζήτησης Borrowing_ID απο member_id {} και book_id {}".format(member_id, book_id))
            return False
        
        # Ανανεώνουμε το απόθεμα
        try:
            cur.execute('''UPDATE books SET current_stock = current_stock + 1 WHERE book_id = ?''', (book_id,))
            logging.info("Επιτυχία αύξησης αποθέματος βιβλίου με κωδικό: {}".format(book_id))
        except Exception as e:
            logging.error("Αποτυχία ενημέρωσης stock βιβλίου book_id {}".format(book_id))
            return False

        # Ανανεώνουμε την βάση δεδομένων κατά την επιστροφή του βιβλίου
        try:
            cur.execute('''UPDATE borrowings SET return_status = 1, rating=? WHERE borrow_id=?''', (book_rating, borrowing_id))
            dbConn = self.conn
            dbConn.commit()
            logging.info("Επιτυχία επιστροφής βιβλίου κωδικό και κωδικό δανεισμού: {}".format(book_id, borrowing_id))
            return True
        except Exception as e:
            logging.error("Αποτυχία επιστροφής βιβλίου {} με κωδικό δανεισμού {}".format(book_id, borrowing_id))
            return False   

    def delete_borrowing(self, borrowingId):
        '''Διαγραφή δανεισμού βάση borrowing Id'''
        dbConn = self.conn
        sqlQry = ''' DELETE FROM borrowings WHERE borrow_id=? '''
        try:
            cur = self.conn.cursor()
            sqlQry = ''' DELETE FROM borrowings WHERE borrow_id=? '''
            cur.execute(sqlQry, (borrowingId,))
            dbConn.commit()
            return True
        except Exception as e:
            logging.error("Αποτυχία διαγραφής δανεισμού με κωδικό {}. Λάθος: {}".format(borrowingId, e))
            return False
        
    def close_connection(self):
        self.conn.close()
