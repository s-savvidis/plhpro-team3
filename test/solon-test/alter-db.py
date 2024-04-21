#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error

logging.basicConfig(level=logging.DEBUG)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logging.error(e)
        sys.exit(1)

#######################################
def alter_sql_tables(conn):
    
    alterStatements=[]
    
    alterStatements.append("ALTER TABLE books ADD COLUMN total_stock INT NOT NULL DEFAULT 0;")
    alterStatements.append("ALTER TABLE books ADD COLUMN current_stock INT NOT NULL;")
    alterStatements.append("ALTER TABLE borrowings ADD COLUMN return_status INTEGER;")

    cur=conn.cursor()                       # Current DB record. Get the cursor.
      
    for sqlAlter in alterStatements:
        logging.info("Altering Books - {}".format(sqlAlter))
        try:
            cur.execute(sqlAlter)
        except Error as e:
            print(e)
    return None

#######################################
if __name__ == '__main__':

    conn=create_connection("./members_sqlite.db")
    alter_sql_tables(conn)
    sys.exit(0)
