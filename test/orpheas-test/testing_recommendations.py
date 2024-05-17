import sys
import logging
import sqlite3
from sqlite3 import Error
import os

path_to_directory = 'C:/Users/orphe/OneDrive/Έγγραφα/GitHub/plhpro-team3'
sys.path.append(path_to_directory)
from library_borrowing_manage import library_borrowings

logging.basicConfig(level=logging.DEBUG)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logging.error(e)
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='SQLite3 DB filename', default="borrowing_sqlite.db")
    args = parser.parse_args()

    try:
        conn = create_connection(args.database)
    except Exception as e:
        logging.error("Error Establishing connection to db {}. Error: {}".format(args.database, e))
        sys.exit(1)

    manager = library_borrowings(conn)

    member_id = 1 
    recommendations = manager.recommendations(member_id)
    print("Recommendations for member {}: {}".format(member_id, recommendations))