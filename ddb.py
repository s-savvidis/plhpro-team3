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
        # Ορισμός τίτλου παραθύρου
        self.title("Διαχείριση Δανειστικής Βιβλιοθήκης")
        # Ορισμός διάστασης παραθύρου
        self.geometry("1000x800") 

        # Δημιουργία ενός container (Frame) που θα περιέχει όλες τις σελίδες
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True) #τοποθετειται επάνω, και επεκτείνεται σε όλη τη διαθέσιμη σελίδα
        #το weight καθορίζει τη "σημαντικότητα" της επέκτασης. Ορίζεται 1 σε στήλη και γραμμή καθώς θέλουμε να επεκτείνονται και τα δύο όσο μεγαλώνει το παράθηρο
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Λεξικό για την αποθήκευση των διαφορετικών frames (σελίδων)
        self.frames = {}

        # Δημιουργία και αποθήκευση κάθε σελίδας στο λεξικό frames
        for F in (HomePage, BooksPage, UsersPage, StatsPage, BorrowingsPage):
            #δημιουργούμε τη μεταβλητή frame η οποία περιέχει μία σελίδα στην οποία περνάει ως όρισμα το container που δημιουργήσαμε και την κλαση του παραθύρου
            frame = F(container, self)
            #δημιουργούμε μια καταχώρηση στο λεξικό υπό τη μορφή {Σελίδα:frame}
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew") #nsew = επέκταση προς όλες τις κατευθύνσεις

        # Επιλογή της αρχικής σελίδας ως πρώτη σελίδα προς φόρτωση στον χρήστη
        self.show_frame(HomePage)
    
    # Μέθοδος για την εμφάνιση της επιλεγμένης από το χρήστη σελίδας κατά την πλοήγηση
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()#μέθοδος της tkinter για να φέρει στο προσκήνιο τη σελίδα επιλογής

# Δημιουργία του κύριου παραθύρου της εφαρμογής
app = MainWindow()
# Έναρξη του κύριου βρόχου της εφαρμογής
app.mainloop()

       