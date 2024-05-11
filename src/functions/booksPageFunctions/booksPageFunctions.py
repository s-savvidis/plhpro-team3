import tkinter as tk
from src.database.db import Database as dtb

def deleteFields(self):
    self.entry_field1.delete(0, tk.END)
    self.entry_field2.delete(0, tk.END) 
    self.entry_field3.delete(0, tk.END) 
    self.entry_field4.delete(0, tk.END)

def switchButtonState(self, value):
    if (value == 0):
        self.save_button['state'] = tk.DISABLED
        self.delete_button['state'] = tk.DISABLED
    elif (value == 1):
        self.save_button['state'] = tk.NORMAL
        self.delete_button['state'] = tk.NORMAL

def showBooks(self, db, bookTitle):
    deleteFields(self)
    books = dtb.search_title(db, bookTitle)
    self.bookShownData = books
    self.result_listbox.delete(0, tk.END) 
    
    for book in books:
        self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
    switchButtonState(self, 0)

def deleteBook(self, db, bookId):
    dtb.delete_book(db, bookId)

def on_double_click(self, event):
    selection = self.result_listbox.curselection()
    if selection:
        index = selection[0]
        value = self.bookShownData[index]
        deleteFields(self)
        self.entry_field1.insert(0, value[1])
        self.entry_field2.insert(0, value[3])
        self.entry_field3.insert(0, value[2])
        self.entry_field4.insert(0, value[4])
        self.bookID = value[0]
        self.bookIDLabel.configure(text=f"{value[0]}")
        switchButtonState(self, 1)

        self.selectedBook = {
            'title': value[1],
            'category': value[3],
            'author': value[2],
            'isbn': value[4],
            'total_stock': value[5],
            'current_stock': value[6],
            'book_id': value[0]
        }


        

