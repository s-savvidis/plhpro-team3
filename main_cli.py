#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

# Importing private modules
from library_member_manage import library_members
from library_books_manage import library_books
from library_borrowing_manage import library_borrowings



#######################################
if __name__ == '__main__':
    import argparse
    
    newMembr={}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="../../members_sqlite.db")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)

    libMembers = library_members(conn)