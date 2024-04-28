#!/usr/bin/env python3
import sys
import logging
import sqlite3
from sqlite3 import Error
import pandas as pd

class library_borrowings():
    '''Κλάση διαχείρισης δανεισμών.'''
    def __init__(self, conn):
        self.conn = conn
        
    def bulk_import(self, borrowinList):
        pass
