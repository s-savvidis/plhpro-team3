#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)

#Εισαγωγή βιβλιοθηκών
import tkinter as tk

#Εισαγωγή Σελίδων
from src.pages.HomePage import HomePage
from src.pages.BooksPage import BooksPage
from src.pages.UsersPage import UsersPage
from src.pages.BorrowingsPage import BorrowingsPage
from src.pages.MainStatsPage import StatsPage

#Ορισμός κλάσης βασικού παραθύρου
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Διαχείριση Δανειστικής Βιβλιοθήκης") #Τίτλος παραθύρου
        self.geometry("1000x800") #Τίτλος παραθύρου

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, BooksPage, UsersPage, StatsPage, BorrowingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
    
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

app = MainWindow()
app.mainloop()

       