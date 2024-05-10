import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd
import os

class LibraryDBInit:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_tables(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS members (
                                        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name      TEXT,
                                        age       INTEGER,
                                        occupation TEXT,
                                        tel       TEXT,
                                        email     TEXT UNIQUE,
                                        gender    TEXT
                                    );
                                    """)

        c.execute("""CREATE TABLE IF NOT EXISTS books (
                                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        title     TEXT,
                                        category  TEXT,
                                        author    TEXT,
                                        isbn      INT NOT NULL UNIQUE,
                                        total_stock INT NOT NULL,
                                        current_stock INT NOT NULL
                                    );
                                    """)

        c.execute("""CREATE TABLE IF NOT EXISTS borrowings (
                                        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        book_id   INTEGER NOT NULL,
                                        member_id INTEGER NOT NULL,
                                        date      TEXT NOT NULL,
                                        return_status INTEGER,
                                        rating    INTEGER,
                                        FOREIGN KEY(member_id) REFERENCES members(member_id),
                                        FOREIGN KEY(book_id) REFERENCES books(book_id)
                                    );
                                    """)

        conn.commit()
        conn.close()

    def import_csv(self, table, csv_file):
        conn = sqlite3.connect(self.db_file)
        df = pd.read_csv(csv_file)
        df.to_sql(table, conn, if_exists='append', index=False)
        conn.close()

#if __name__ == "__main__":

    #db_init = LibraryDBInit("library.db")
    #db_init.create_tables()
    #db_init.import_csv("books", "C:\\Users\\orphe\\Desktop\\test\\books.csv")
    #db_init.import_csv("members", "C:\\Users\\orphe\\Desktop\\test\\members.csv")
    #db_init.import_csv("borrowings", "C:\\Users\\orphe\\Desktop\\test\\borrowings.csv")

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
            cur.execute('''UPDATE borrowing SET return_status = 1, rating=? WHERE borrowing_id=?''', (book_rating, borrowing_id,))
            dbConn = self.conn
            dbConn.commit()
            logging.info("Επιτυχία επιστροφής βιβλίου κωδικό και κωδικό δανεισμού: {}".format(book_id, borrowing_id))
            return True
        except Exception as e:
            logging.error("Αποτυχία επιστροφής βιβλίου {} με κωδικό δανεισμού {}".format(book_id, borrowing_id))
            return False
    
    def stats_books_member(self, start_date=None, end_date=None):
        ''' Πλήθος βιβλίων ανα μέλος σε χρονική περίοδο που επιλέγουμε (Έτος-Μήνας-Ημέρα)'''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(members.member_id), members.member_id, members.name FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    WHERE borrowings.date >= ? 
                    AND borrowings.date <= ? 
                    GROUP BY members.member_id ORDER BY members.name;''', (start_date, end_date))
        book_member_stats = cur.fetchall()
        return book_member_stats 

    def stats_borrowing_member(self, member_id, start_date=None, end_date=None):
        ''' Κατανομή προτιμήσεων δανεισμού ανά μέλος σε χρονική περίοδο που επιλέγουμε (Έτος-Μήνας-Ημέρα)'''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(books.category), books.category FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    WHERE borrowings.date >= ? 
                    AND borrowings.date <= ? 
                    AND borrowings.member_id = ?
                    GROUP BY books.category
                    ORDER BY COUNT(books.category) DESC;''', (start_date, end_date, member_id))
        borrowing_member_stats = cur.fetchall()
        return borrowing_member_stats

    def stats_pref_members(self, start_date=None, end_date=None):
        ''' Κατανομή προτιμήσεων όλων των μελών ξεχωριστά ανά κατηγορία για χρονική περίοδο που επιλέγουμε (Έτος-Μήνας-Ημέρα)'''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.member_id, members.name, COUNT(books.category), books.category FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    WHERE borrowings.date >= ? 
                    AND borrowings.date <= ? 
                    GROUP BY members.name, books.category 
                    ORDER BY members.member_id, COUNT(books.category) DESC;''', (start_date, end_date))
        pref_members_stats = cur.fetchall()
        return pref_members_stats
    
    def stats_pref(self, start_date=None, end_date=None):
        ''' Κατανομή προτιμήσεων όλων των μελών συνολικά ανά κατηγορία για χρονική περίοδο που επιλέγουμε (Έτος-Μήνας-Ημέρα)'''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(books.category), books.category FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    WHERE borrowings.date >= ? 
                    AND borrowings.date <= ? 
                    GROUP BY books.category 
                    ORDER BY COUNT(books.category) DESC;''', (start_date, end_date))
        pref_stats = cur.fetchall()
        return pref_stats


    def stats_member_history(self, member_id):
        ''' Ιστορικό δανεισμού ανά μέλος '''
        cur = self.conn.cursor()
        cur.execute('''SELECT books.category, books.title, borrowings.date FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    WHERE borrowings.member_id = ? 
                    ORDER BY borrowings.date DESC;''', (member_id,))
        member_history_stats = cur.fetchall()
        return member_history_stats

    def stats_author(self):
        ''' Πλήθος δανεισμών ανά συγγραφέα '''
        cur = self.conn.cursor()
        cur.execute('''SELECT COUNT(books.author), books.author FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    GROUP BY books.author 
                    ORDER BY COUNT(books.author) DESC;''')
        author_stats = cur.fetchall()
        return author_stats

    def stats_age(self):
        ''' Πλήθος δανεισμών ανά ηλικιακή ομάδα '''
        cur = self.conn.cursor()
        cur.execute('''SELECT CASE 
        WHEN members.age BETWEEN 0 AND 20 THEN '0-20'
        WHEN members.age BETWEEN 21 AND 30 THEN '21-30'
        WHEN members.age BETWEEN 31 AND 40 THEN '31-40'
        WHEN members.age BETWEEN 41 AND 50 THEN '41-50'
        WHEN members.age BETWEEN 51 AND 60 THEN '51-60'
        ELSE '60+'
        END AS age_group,
        COUNT(borrowings.borrow_id) FROM borrowings 
        INNER JOIN members ON borrowings.member_id=members.member_id 
        INNER JOIN books ON borrowings.book_id=books.book_id 
        GROUP BY age_group
        ORDER BY members.age;''')
        age_stats = cur.fetchall()
        return age_stats
    
    def stats_gender(self):
        ''' Πλήθος δανεισμών ανά φύλο '''
        cur = self.conn.cursor()
        cur.execute('''SELECT members.gender, COUNT(borrowings.borrow_id) FROM borrowings 
                    INNER JOIN members ON borrowings.member_id=members.member_id 
                    INNER JOIN books ON borrowings.book_id=books.book_id 
                    GROUP BY members.gender 
                    ORDER BY COUNT(borrowings.borrow_id) DESC;''')
        gender_stats = cur.fetchall()
        return gender_stats
    
    def recommendations(self, member_id):
        ''' Πρόταση δανεισμού μέσω Ratings '''
        cur = self.conn.cursor()
    
        # Βρίσκουμε το ιστορικό δανεισμών του μέλους στο οποίο θέλουμε να προτείνουμε βιβλία
        cur.execute('''SELECT book_id FROM borrowings WHERE member_id = ?''', (member_id,))
        borrowing_history = cur.fetchall()
    
        #Αν δεν έχει δανειστεί βιβλία τότε λόγο μη επαρκούς ιστορικού του προτείνουμε τα βιβλία με τις καλύτερες 
        # συνολικές κριτικές από πέντε διαφορετικές κατηγορίες
        if len(borrowing_history) == 0:
            cur.execute('''SELECT books.book_id, books.title
                    FROM books 
                    LEFT JOIN borrowings ON books.book_id = borrowings.book_id 
                    WHERE books.category IN (SELECT DISTINCT category FROM books) 
                    GROUP BY books.book_id 
                    ORDER BY AVG(borrowings.rating) DESC 
                    LIMIT 5''')
            suggestions = cur.fetchall()
        else:
            #Αν έχει δανειστεί τουλάχιστον ένα βιβλία, βρίσκουμε τα βιβλία που του άρεσαν περισσότερο (μέχρι 10 για να αποφύγουμε χαμηλές βαθμολογίες)
            cur.execute('''SELECT book_id FROM borrowings 
                        WHERE member_id = ? 
                        ORDER BY rating DESC 
                        LIMIT 10''', (member_id,))
            top_rated = cur.fetchall()
        
        
        # Βρίσκουμε το καλύερο βιβλίο που δεν έχει δανειστεί, βάση της μέσης βαθμολογίας του, για κάθε ξεχωριστή κατηγορία βιβλίου που υπάρχει στο ιστορικό του.
            suggested_categories = []
            suggestions = []
            for book_id, in top_rated:
                cur.execute('''SELECT category FROM books WHERE book_id = ?''', (book_id,))
                category = cur.fetchone()[0]
                if category not in suggested_categories:
                    suggested_categories.append(category)
                    cur.execute('''SELECT books.book_id, books.title 
                               FROM books 
                               LEFT JOIN borrowings ON books.book_id = borrowings.book_id AND borrowings.member_id = ?
                               WHERE books.category = ?
                               AND borrowings.member_id IS NULL
                               GROUP BY books.book_id, books.title 
                               ORDER BY AVG(borrowings.rating) DESC
                               LIMIT 1''', (member_id, category))
                    suggested_book = cur.fetchone()
                    if suggested_book:
                        suggestions.append(suggested_book)

            # Αν υπάρχουν λιγότερες από 5 προτάσεις, συμπληρώνουμε με τα καλύτερα βάση βαθμολογίας χρηστών βιβλία, από άλλες κατηγορίες
            while len(suggestions) < 5:
                cur.execute('''SELECT books.book_id, books.title
                           FROM books 
                           LEFT JOIN borrowings ON books.book_id = borrowings.book_id 
                           WHERE books.category NOT IN ({})
                           GROUP BY books.book_id 
                           ORDER BY AVG(borrowings.rating) DESC 
                           LIMIT {}'''.format(','.join(['?']*len(suggested_categories)), (5 - len(suggestions))), list(suggested_categories))
                remaining_suggestions = cur.fetchall()
                suggestions.extend(remaining_suggestions)
                
    
        return suggestions   
    
        
def get_recommendations(member_id):
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    recommendations = library_manager.recommendations(member_id)
    conn.close()

    print("Προτάσεις δανεισμού για το μέλος με ID:", member_id)
    for idx, (book_id, title) in enumerate(recommendations, start=1):
        print(f"{idx}. {title}")
        
def get_stats_books_member(start_date=None, end_date=None):
    start_date = input('Από (έτος-μήνας-ημέρα)')
    end_date = input ('Έως (έτος-μήνας-ημέρα)')
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_book_member = library_manager.stats_books_member(start_date, end_date)
    conn.close()
    print('Στατιστικά μελών για την περίοδο από', start_date, 'έως', end_date, ':')
    for (count, member_id, member_name) in (stats_book_member):
        print('To μέλος', member_id, member_name, 'δανείστηκε', count, 'βιβλίο/α')
        
def get_stats_borrowing_member(member_id, start_date=None, end_date=None):
    start_date = input('Από (έτος-μήνας-ημέρα)')
    end_date = input ('Έως (έτος-μήνας-ημέρα)')
    conn = sqlite3.connect("Library.db")
    library_manager = library_borrowings(conn)
    stats_borrowing_member = library_manager.stats_borrowing_member(member_id, start_date, end_date)
    conn.close()
    print('Στατιστικά προτιμήσεων του μέλους με ID:', member_id, 'για την περίοδο από', start_date, 'έως', end_date)
    for (count, bookCategory) in stats_borrowing_member:
        print(bookCategory, count)
                
        
def get_stats_pref_members(start_date=None, end_date=None):
    start_date = input('Από (έτος-μήνας-ημέρα)')
    end_date = input ('Έως (έτος-μήνας-ημέρα)')
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_pref_members = library_manager.stats_pref_members(start_date, end_date)
    conn.close()
    print('Στατιστικά μελών βάση κατηγορίας για την περίοδο από', start_date, 'έως', end_date, ':')
    for (member_id, member_name, count, bookCategory) in (stats_pref_members):
        print('To μέλος', member_id, member_name, 'δανείστηκε', count, 'βιβλίο/α από την κατηγορία', bookCategory)
                
def get_stats_pref(start_date=None, end_date=None):
    print('Στατιστικά δανεισμών βάση κατηγορίας για την περίοδο από', start_date, 'έως', end_date, ':')
    start_date = input('Από (έτος-μήνας-ημέρα)')
    end_date = input ('Έως (έτος-μήνας-ημέρα)')
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_pref = library_manager.stats_pref(start_date, end_date)
    conn.close()
    
    for (count, bookCategory) in (stats_pref):
        print('Tα μέλη δανείστηκαν', count, 'βιβλίο/α από την κατηγορία', bookCategory)
        
def get_stats_member_history(member_id):
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_member_history = library_manager.stats_member_history(member_id)
    conn.close()
    print('Ιστορικό δανεισμού για το μέλος με ID:', member_id)
    for (bookCategory, book_title, borrowing_date) in stats_member_history:
        print(book_title, '(' + bookCategory + ')', borrowing_date)

def get_stats_author():
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_author = library_manager.stats_author()
    conn.close()
    print('Στατιστικά πλήθους δανεισμών ανά συγγραφέα')
    for (count, book_author) in stats_author:
        print(book_author, count)
        
def get_stats_age():
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_age = library_manager.stats_age()
    conn.close()
    print('Στατιστικά πλήθους δανεισμών ανά ηλικιακή ομάδα')
    for (members_age, count) in stats_age:
        print(members_age, count)        
        
def get_stats_gender():
    conn = sqlite3.connect("library.db")
    library_manager = library_borrowings(conn)
    stats_gender = library_manager.stats_gender()
    conn.close()
    print('Στατιστικά πλήθους δανεισμών ανά φύλο')
    for (members_gender, count) in stats_gender:
        print(members_gender, count)
                                      

if __name__ == "__main__":
    member_id = 1
    #get_recommendations(member_id)
    #get_stats_books_member()
    #get_stats_borrowing_member(member_id)
    #get_stats_pref_members()
    #get_stats_pref()
    #get_stats_member_history(member_id)
    #get_stats_author()
    #get_stats_age()
    #get_stats_gender()



#if __name__ == '__main__':
    #import argparse
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="borrowing_sqlite.db")
    #args = parser.parse_args()

    #try:
        #conn = create_connection(args.database)
    #except Exception as e:
        #logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        #sys.exit(1)

