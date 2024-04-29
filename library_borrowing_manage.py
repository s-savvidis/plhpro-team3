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
    
    def borrow_book(self, member_id, book_id, borrow_date):
        cur = self.conn.cursor()

        # Αναζήτηση διαθεσιμότητας βιβλίου
        cur.execute('''SELECT current_stock FROM books WHERE id = ?''', (book_id,))
        stock = cur.fetchone()[0]
        if stock == 0:
            return False

        else:
            # Ανανεώνουμε το απόθεμα
            cur.execute('''UPDATE books SET current_stock = current_stock - 1 WHERE book_id = ?''', (book_id,))

            # Εισάγουμε τον δανεισμό στην βάση δεδομένων
            cur.execute('''INSERT INTO borrowing (member_id, book_id, date, return_status, rating) VALUES (?, ?, ?, 0, ?)''', (member_id, book_id, borrow_date, 0))

            return True  
    
    def return_book(self, member_id, book_id, book_rating):
        borrowing_id=0
        
        cur = self.conn.cursor()
        
        try:
            cur.execute('''SELECT borrowing_id FROM borrowings WHERE member_id = ? AND book_id = ? AND return_status = 0''', (member_id,book_id,))
            borrowing_id = cur.fetchone()[0]
        except Exception as e:
            logging.error("Αποτυχία αναζήτησης Borrowing_ID απο member_id {} και book_id {}".format(member_id, book_id))
            return False
        
        # Ανανεώνουμε το απόθεμα
        try:
            cur.execute('''UPDATE books SET current_stock = current_stock + 1 WHERE id = ?''', (book_id,))
            logging.info("Επιτυχία αύξησης αποθέματος βιβλίου με κωδικό: {}".format(book_id))
        except Exception as e:
            logging.error("Αποτυχία ενημέρωσης stock βιβλίου book_id {}".format(book_id))
            return False

        # Ανανεώνουμε την βάση δεδομένων κατά την επιστροφή του βιβλίου
        try:
            cur.execute('''UPDATE borrowing SET return_status = 1, rating=? WHERE borrowing_id=?''', (borrowing_id,))
            dbConn.commit()
            logging.info("Επιτυχία επιστροφής βιβλίου κωδικό και κωδικό δανεισμού: {}".format(book_id, borrowing_id))
            return True
        except Exception as e:
            logging.error("Αποτυχία επιστροφής βιβλίου {} με κωδικό δανεισμού {}".format(book_id, borrowing_id))
            return False
    
    def stats_books_member(self):
        ''' Πλήθος βιβλίων ανα μέλος σε χρονική περίοδο '''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(members.member_id), members.member_id, members.name FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.date >= "2023-01-01" AND borrowings.date <= "2023-01-31" GROUP BY members.member_id ORDER BY members.name;''')
        book_member_stats = cur.fetchall()
        return book_member_stats

    def stats_borrowing_member(self):
        ''' Κατανομή προτιμήσεων δανεισμού ανά μέλος '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.member_id, members.name, COUNT(books.category), books.category FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.date >= "2023-02-01" AND borrowings.date <= "2023-02-31" AND borrowings.member_id=23 GROUP BY books.category ;''')
        borrowing_member_stats = cur.fetchall()
        return borrowing_member_stats

    def stats_pref_members(self):
        ''' Κατανομή προτιμήσεων όλων των μελών ανά κατηγορία για χρονική περίοδο '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.member_id, members.name, COUNT(books.category), books.category FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id WHERE borrowings.date >= "2023-02-01" AND borrowings.date <= "2023-02-31" GROUP BY members.name, books.category;''')
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
        cur.execute('''SELECT COUNT(books.author), books.author FROM borrowings INNER JOIN members ON borrowings.member_id=members.member_id INNER JOIN books ON borrowings.book_id=books.book_id GROUP BY books.author ORDER BY books.author;''')
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
    
    def recommendations(self, member_id):
        ''' Πρόταση δανεισμού μέσω Ratings '''
        cur = self.conn.cursor()
    
        # Βρίσκουμε το ιστορικό δανεισμών του μέλους στο οποίο θέλουμε να προτείνουμε βιβλία
        cur.execute('''SELECT book_id FROM borrowings WHERE member_id = ?''', (member_id,))
        borrowing_history = cur.fetchall()
    
        #Αν έχει δανειστεί μέχρι πέντε βιβλία τότε λόγο μη επαρκούς ιστορικού του προτείνουμε τα βιβλία με τις καλύτερες 
        # συνολικές κριτικές από πέντε διαφορετικές κατηγορίες
        if len(borrowing_history) <= 5:
            cur.execute('''SELECT books.book_id, books.title, AVG(borrowings.rating) 
                    FROM books 
                    LEFT JOIN borrowings ON books.book_id = borrowings.book_id 
                    WHERE books.category IN (SELECT DISTINCT category FROM books) 
                    GROUP BY books.book_id 
                    ORDER BY AVG(borrowings.rating) DESC 
                    LIMIT 5''')
            suggestions = cur.fetchall()
        else:
            # Βρίσκουμε τα πέντε βιβλία που του άρεσαν περισσότερο
            cur.execute('''SELECT book_id FROM borrowings 
                        WHERE member_id = ? 
                        ORDER BY rating DESC 
                        LIMIT 5''', (member_id,))
            top_rated = cur.fetchall()
        
        
        suggestions = []

        # Βρίσκουμε τις κατηγορίες στις οποίες ανήκουν τα αγαπημένα του βιβλία
        top_categ = []
        for book_id, in top_rated:
            cur.execute('''SELECT category FROM books WHERE book_id = ?''', (book_id,))
            category = cur.fetchone()[0]
            if category not in top_categ:
                top_categ.append(category)
                if len(top_categ)>= 5:
                    break

        # Βρίσκουμε βιβλία τα οποία ο χρήστης δεν έχει δανειστεί 
        for category in top_categ:
            cur.execute('''SELECT book_id, title, AVG(borrowings.rating) 
                   FROM books 
                   LEFT JOIN borrowings ON books.book_id = borrowings.book_id AND borrowings.member_id = ?
                   WHERE books.category LIKE ? AND borrowings.member_id IS NULL
                   GROUP BY books.book_id, books.title 
                   ORDER BY AVG(borrowings.rating) DESC''', (member_id, '%' + category + '%'))
            top_in_cat = cur.fetchall()
            for book_id, title in top_in_cat:
                if book_id not in [book_id for book_id, in borrowing_history]:
                    suggestions.append((book_id, title))
                    if len(suggestions) >= 5:  
                        break
            if len(suggestions) >= 5:
                break

            return suggestions
        
######################################
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="borrowing_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)        


