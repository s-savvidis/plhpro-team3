#!/usr/bin/env python3
import sys
import logging
from random import randrange
import sqlite3
from sqlite3 import Error
from datetime import timedelta, datetime

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

def random_users(conn, number):
    '''Αναζήτηση μέλους με τμήμα του ονόματος'''
    memberIdList=[]

    cur = conn.cursor()
    sqlQry = ''' SELECT * FROM members'''
    cur.execute(sqlQry)
    memberRows = cur.fetchall()
    for i in range(0, number):
        while True:
            rndNum = randrange(30)
            if not memberRows[rndNum][0] in memberIdList:
                memberIdList.append(memberRows[rndNum][0])
                break
    return memberIdList

def random_books(conn, categoryName):
    '''Αναζήτηση βιβλίου με κατηγορία'''
    cur = conn.cursor()
    sqlQry = ''' SELECT book_id FROM books WHERE category=?'''
    cur.execute(sqlQry, (categoryName,))
    bookRows = cur.fetchall()
    return bookRows

def random_borrowings(bookIdList, maxBorrowings):
    ''' Δημιουργία λίστας τυχαία επιλογής βιβλίων απο κατηγορία '''
    rndBookId = 0
    borrowList=[]
    for i in range(0, maxBorrowings):
        while True:
            rndNum = randrange(len(bookIdList))
            if not bookIdList[rndNum] in borrowList:
                borrowList.append(bookIdList[rndNum])
                break
    return borrowList

def borrow_random_dates(startDate, endDate, numOfBooks):
    randomBookDates = []
    date_range = endDate - startDate
    for _ in range(numOfBooks):
        rndDays = randrange(date_range.days)
        rndDate = startDate + timedelta(days=rndDays)
        randomBookDates.append(rndDate)
    return randomBookDates

#######################################
'''

memberList : Τυχαία λίστα με member_id μελών.
bookPref   : Πίνακας με κατηγορίες βιβλίων που θα προτιμήσει κάθε μέλος απο τη memberList.
             Με αυτό τον τρόπο μπορούμε να δημιουργήσουμε ένα Bias για συγκεκριμένες κατηγορίες βιβλίων.
bookIds    : Θα έχει όλα τα book_id για κάθε κατηγορία. 
             Θα βοηθήσει στο να διαλέξουμε τυχαία βιβλία απο την προκαθορισμένη κατηγορία , για κάθε μέλος.
bookIdList : Πίνακας 2 διαστάσεων. Θέση 0 θα έχει το όνομα κάθε κατηγορίας. Θέση 1 θα έχει nested tupple απο  book_id (βλ. bookIds).
             bookIdList[0]: ['Βίπερ', 'Κόμικ', Επική ποίηση' ...]
             bookIdList[1]: [(1,2,3), (5,6), (7,8,9,10,11)]
             Με αυτό τον τρόπο βρίσκουμε τη θέση των βιβλίων που χρειαζόμαστε αναζητοντας το index της θέσης 0 βάση ονόματος.
             π.χ.
             bookIdList[0].index('Κόμικ') = 1
             άρα η λίστα με τα book_ids που είναι διαθέσημα για αυτή την κατηγορία είναι:
             bookIdList[1][1] = (5,6)
             Έτσι μπορούμε να πάρουμε ένα τυχαίο βιβλίο με random μεταξύ 0 και 1. 0=bookId5 1=bookId=6

memberBorrow = {} : Μέλη μα κάθε κατηγορία βιβλίου και nested λίστα βιβλίων.

memberBorrow = {'member_id': 0,
                'book_lst: []
                }

                




'''
if __name__ == '__main__':
    conn = create_connection("../../../members_sqlite.db")
    
    bookPref = []
    memberList = []
    bookIds = []
    bookIdList = []
    bookIdList.append([])
    bookIdList.append([])
    bookCategory=['Βίπερ',
                  'Κόμικ',
                  'Επική ποίηση',
                  'Άρλεκιν',
                  'Νουβέλα',
                  'Σχολικά',
                  'Αγγλική Λογοτεχνία',
                  'Ιστορικό',
                  'Φαντασία',
                  'Ελληνική Λογοτεχνία',
                  'Ιστορικό μυθιστόρημα',
                  'Κυβερνοπάνκ',
                  'Μυθιστόρημα',
                  'Πληροφορική',
                  'Επιστημονική Φαντασία'
                  ]
    memberBorrow={}
    bookIdBorrow=[]
    memberBookBorrow=[]
    borrowingList=[]
    
    memberList = random_users(conn, 16)
    for i in (range(len(bookCategory))):
        bookIds = random_books(conn, bookCategory[i])
        #print(bookIds)
        bookIdList[0].append(bookCategory[i])
        bookIdList[1].append(bookIds)
    
    for i in (range(len(bookCategory))):
        print(bookIdList[0][i])
        print(bookIdList[1][i])
    
    print(bookIdList[0].index('Άρλεκιν'))
    
    bookPref.append(["Ιστορικό μυθιστόρημα","Μυθιστόρημα","Ιστορικό","Ελληνική Λογοτεχνία"])
    bookPref.append(["Μυθιστόρημα","Επική ποίηση","Επιστημονική Φαντασία"])
    bookPref.append(["Πληροφορική","Βίπερ","Σχολικά"])
    bookPref.append(["Κυβερνοπάνκ","Πληροφορική","Επιστημονική Φαντασία","Επική ποίηση","Κόμικ"])
    bookPref.append(["Βίπερ","Ελληνική Λογοτεχνία","Ιστορικό"])
    bookPref.append(["Μυθιστόρημα"])
    bookPref.append(["Μυθιστόρημα","Ιστορικό μυθιστόρημα","Ιστορικό","Σχολικά"])
    bookPref.append(["Σχολικά", "Ελληνική Λογοτεχνία","Ιστορικό μυθιστόρημα"])
    bookPref.append(["Πληροφορική"])
    bookPref.append(["Επιστημονική Φαντασία","Επική ποίηση","Βίπερ","Κυβερνοπάνκ"])
    bookPref.append(["Βίπερ","Σχολικά","Νουβέλα"])
    bookPref.append(["Ιστορικό","Αγγλική Λογοτεχνία","Μυθιστόρημα","Μυθιστόρημα", "Άρλεκιν","Ελληνική Λογοτεχνία"])
    bookPref.append(["Ελληνική Λογοτεχνία","Σχολικά","Ιστορικό μυθιστόρημα","Κόμικ"])
    bookPref.append(["Κόμικ","Πληροφορική","Αγγλική Λογοτεχνία"])
    bookPref.append(["Μυθιστόρημα","Βίπερ","Αγγλική Λογοτεχνία"])
    bookPref.append(["Μυθιστόρημα","Ιστορικό","Βίπερ"])
    
    
    # Εμφάνιση Α/Α , κατ. βιβλίου και πλήθος βιβλίων.
    for i in range(0, len(bookPref)):
        print("************ {}".format(i))
        for j in range(0, len(bookPref[i])):
            bookIndex = bookIdList[0].index(bookPref[i][j])
            print("Κατηγορία: {} - Αριθμός βιβλίων: {}".format(
                bookCategory[bookIndex],
                len(bookIdList[1][bookIndex])
            ))
            print(bookIdList[1][bookIndex])
    
    # Δημιουργία τυχαίων δανεισμών.
    for i in range(0, len(memberList)):
        # Βρόγχος για διαπέραση λίστας μελών.
        
        print("Μέλος {}".format(memberList[i]))
        
        # Διαπέραση προτίμησης κατηγορίας κάθε μέλους.
        for bookCat in bookPref[i]:
            
            catIndex = bookIdList[0].index(bookCat) # categoryIndex απο το όνομα της προτίμησης.
            bookNum = len(bookIdList[1][catIndex])
            rndBorrowings = randrange(bookNum)      # Πόσα βιβλία θα διαλέξει το μέλος απο τη συγκεκριμένη κατηγορία.
            
            catBorrowing = random_borrowings(bookIdList[1][catIndex], rndBorrowings)
            for bookIdBorrow in catBorrowing:
                memberBookBorrow.append(bookIdBorrow)
                
        
        memberBorrow = {'member_id': memberList[i],
                     'book_list': memberBookBorrow
                     }
        borrowingList.append(memberBorrow) # Αποθήκευση προτιμήσεων μέλους
        memberBookBorrow=[]                # Καθαρισμός πίνακα πριν την επανάληψη
    
    
    bookingDates=[]
    
    bookingStartDate = datetime(2023, 1, 1)
    bookingEndDate = datetime(2023, 12, 31)
    
    for memberBorrowings in borrowingList:
        
        # Φτιάξε τυχαίες ημερομηνίες.
        bookingDates = borrow_random_dates(bookingStartDate, bookingEndDate, len(memberBorrowings['book_list']))
        
        for i in range(0, len(memberBorrowings['book_list'])):
            # Εμφάνιση member_id, book_id, ημερομηνία, rating, επιστροφή
            bookRating=randrange(1,10)
            if bookRating in range(1,2):
                memberRating = 1  # Δεν μου άρεσε.
            elif bookRating in range(3,8):
                memberRating = 2  # Μου άρεσε.
            else:
                memberRating = 3  # Το λάτρεψα.
                
            print("{}, {}, {}, 0, {}".format(memberBorrowings['member_id'],
                                            *memberBorrowings['book_list'][i],
                                            bookingDates[i].strftime('%Y-%m-%d'),
                                            memberRating
                                            )
                  )
            
            
            
            
        
        
        
        
                
                
            
            