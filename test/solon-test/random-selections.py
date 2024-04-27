#!/usr/bin/env python3
import sys
import logging
from random import randrange
import sqlite3
from sqlite3 import Error

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
'''
def random_orders(conn, memberList, bookIdList, bookPref):
    borrowList=[]
    
    for i in range(0, len(bookPref)):
        
    memberBorrow={}
    
    for i in 
    pass
'''
#######################################
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
    
    for i in range(0, len(bookPref)):
        print("************ {}".format(i))
        for j in range(0, len(bookPref[i])):
            bookIndex = bookIdList[0].index(bookPref[i][j])
            print(bookIdList[1][bookIndex])