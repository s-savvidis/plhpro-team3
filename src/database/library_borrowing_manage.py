#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

class library_borrowings():
    '''Κλάση διαχείρισης δανεισμών.'''
    def __init__(self, database):
        try:
            self.conn = sqlite3.connect(database)
        except Exception as e:
            logging.error("Error Establishing connection to db {}. Error: {}".format(database, e))
            sys.exit(1)

    
    def search_borrowing(self, member_id=None):
        '''Αναζήτηση δανεισμών βάσξη member_id.'''
        cur = self.conn.cursor()
        
            #Αν δώσουμε member id εμφανίζει τους δανεισμούς του συγκεκριμένου μέλους        
        if member_id:
            sqlQry = '''SELECT * FROM borrowings WHERE member_id = ? ORDER BY date DESC'''
            cur.execute(sqlQry, (member_id,))
        else:
            # Όταν δεν έχουμε πληκτρολογήσει member id εμφανίζει όλους τους δανεισμούς
            sqlQry = '''SELECT * FROM borrowings ORDER BY date DESC'''
            cur.execute(sqlQry)
        borrowingRows = cur.fetchall()
        return borrowingRows
    
        
    def borrow_book(self, member_id, book_id, borrow_date):
        ''' Συνάρτηση δανεισμού '''
        cur = self.conn.cursor()

        # Αναζήτηση διαθεσιμότητας βιβλίου
        cur.execute('''SELECT current_stock FROM books WHERE book_id = ?''', (book_id,))
        stock = cur.fetchone()[0]
        if stock == 0:
            logging.info("Το βιβλίο με κωδικό {} δεν είναι διαθέσιμο".format(book_id,))
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
        ''' Συνάρτηση επιστροφής βιβλίου '''
        
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
    
    def search_id_member(self, member_id):
        '''Αναζήτηση μέλους βάση κωδικού μέλους'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE member_id=? '''
        cur.execute(sqlQry, (member_id,))
        member = cur.fetchall()

        return member
    
    def search_id_book(self, book_id):
        '''Αναζήτηση βιβλίου βάση κωδικού βιβλίου'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM books WHERE book_id=? '''
        cur.execute(sqlQry, (book_id,))
        book = cur.fetchall()

        return book
    
    def stats_books_member(self, periodApo, periodEos):
        ''' Πλήθος βιβλίων ανα μέλος σε χρονική περίοδο '''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(members.member_id), members.name FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.date >= ? AND borrowings.date <= ? GROUP BY members.member_id ORDER BY COUNT(members.member_id) DESC;''', (periodApo, periodEos,))
        book_member_stats = cur.fetchall()
        return book_member_stats

    def stats_borrowing_member(self):
        ''' Κατανομή προτιμήσεων δανεισμού ανά μέλος '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.member_id, members.name, COUNT(books.category), books.category FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.date >= "2023-02-01" AND borrowings.date <= "2023-02-31" AND borrowings.member_id=23 GROUP BY books.category ;''')
        borrowing_member_stats = cur.fetchall()
        return borrowing_member_stats

    def stats_pref_members(self, periodApo, periodEos):
        ''' Κατανομή προτιμήσεων όλων των μελών ανά κατηγορία για χρονική περίοδο '''
        cur = self.conn.cursor()
        cur.execute('''SELECT books.category, COUNT(books.category) FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.date >= ? AND borrowings.date <= ? GROUP BY books.category ORDER BY COUNT(books.category) DESC;''', (periodApo, periodEos,))
        pref_members_stats = cur.fetchall()
        return pref_members_stats

    def stats_member_history(self):
        ''' Ιστορικό δανεισμού ανά μέλος '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.member_id, members.name, books.category, books.title, borrowings.date FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.member_id=9 ORDER BY borrowings.date;''')
        member_history_stats = cur.fetchall()
        return member_history_stats

    def stats_author(self):
        ''' Πλήθος δανεισμών ανά συγγραφέα '''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(books.author), books.author FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id GROUP BY books.author ORDER BY COUNT(books.author) DESC;''')
        author_stats = cur.fetchall()
        return author_stats

    def stats_age(self):
        ''' Πλήθος δανεισμών ανά ηλικία '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.age, COUNT(borrowings.borrow_id) FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id GROUP BY members.age ORDER BY members.age;''')
        age_stats = cur.fetchall()
        return age_stats

    def stats_gender(self):
        ''' Πλήθος δανεισμών ανά φύλο '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.gender, COUNT(borrowings.borrow_id) FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id GROUP BY members.gender ORDER BY members.gender;''')
        gender_stats = cur.fetchall()
        return gender_stats

    def stats_member_history_all(self):
        ''' Ιστορικό δανεισμού όλων των μελών '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.member_id, members.name, books.category, books.title, borrowings.date FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id ORDER BY members.name, borrowings.date;''')
        member_history_stats = cur.fetchall()
        return member_history_stats
        
######################################
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="borrowing_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
        manager = library_borrowings(conn)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)        


