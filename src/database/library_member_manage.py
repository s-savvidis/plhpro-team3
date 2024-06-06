#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

class library_members():
    '''Κλάση διαχείρισης μελών.'''
    def __init__(self, database):
        #self.conn = conn
        try:
            self.conn = sqlite3.connect(database)
        except Exception as e:
            logging.error("Error Establishing connection to db {}. Error: {}".format(database, e))
            sys.exit(1)
    
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
        
    def stats_borrowing_member(self, member_id, start_date=1900-11-11, end_date=3000-11-11):
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
        
#######################################
if __name__ == '__main__':
    import argparse
    
    newMembr={}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="../../../members_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)

    libMembers = library_members(conn)
    
    
    ###### Εισαγωγή μέλους
    print()
    print("Εισαγωγή νέου μέλους:###########")
    newMembr['full_name'] = input("Όνομα μέλους: ")
    newMembr['age'] = input("Ηλικία: ")
    newMembr['occupation'] = input("Επάγγελμα: ")
    newMembr['telephone_number'] = input("Τηλέφωνο: ")
    newMembr['email'] = input("Email: ")
    newMembr['gender'] = input("gender: ")
    
    insertResult = libMembers.insert_member(newMembr)
    if not insertResult:
        print("Αποτυχία εισαγωγής νέου μέλους.")
        sys.exit(1)
    else:
        print("Κωδικός νέου μέλους {}".format(insertResult))
    

    print("Αναζήτηση μέλους.")    
    memberName = input("Όνομα μέλους: ")
    
    memberSearch = libMembers.search_name(memberName)
    if memberSearch == []:
        print("Tο μέλος δε βρέθηκε.")
        sys.exit(0)
    else:
        for i in memberSearch:
            print(i)
    
    memberID = input("Επιλέξτε κωδικό μέλους: ")
    memberSearch = libMembers.search_id(memberID)
    print("Πληροφορίες μέλους")
    print("Κωδικός μελους: {}".format(memberSearch[0][0]))

    sys.exit(0)