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

class library_members():
    '''Κλάση διαχείρισης μελών.'''
    def __init__(self, conn):
        self.conn = conn
    
    def search_name(self, memberName):
        '''Αναζήτηση μέλους με τμήμα του ονόματος'''
        cur = self.conn.cursor()
        sqlQry = ''' SELECT * FROM members WHERE name LIKE ? '''
        cur.execute(sqlQry, ('%' + memberName + '%',))
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

        sql = ''' INSERT INTO members (name, age, occupation, tel, email) VALUES (?,?,?,?,?) '''
        cur = self.conn.cursor()
        dbConn = self.conn
        try:
            cur.execute(sql, (memberDetails['full_name'],
                              memberDetails['age'],
                              memberDetails['occupation'],
                              memberDetails['telephone_number'],
                              memberDetails['email']
                              )
                        )
            logging.info("Εισαγωγή νέου μέλους στη βάση. {}".format(memberDetails['full_name']))
            dbConn.commit()
            return True
        except Exception as e:
            loggin.error("Πρόβλημα εισαγωγής μέλους {} στη βάση. Πρόβλημα: {}".format(memberDetails['full_name'], e))
            return False

#######################################
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="members_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)

    libMembers = library_members(conn)

    printf("Αναζήτηση μέλους.")    
    memberName = input("Όνομα μέλους: ")
    
    memberSearch = libMembers.search_name(memberName)
    for i in memberSearch:
        print(i)
    
    memberID = input("Επιλέξτε κωδικό μέλους: ")
    memberSearch = libMembers.search_id(memberID)
    print("Πληροφορίες μέλους")
    print(memberSearch)
    
    
    sys.exit(0)
