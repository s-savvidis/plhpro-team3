import tkinter as tk
from src.database.db import Database as dtb

def deleteFields(self):
    self.entry_field1.delete(0, tk.END)
    self.entry_field2.delete(0, tk.END) 
    self.defaultCategory.set(self.categoryOptions["-"]) 
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
        self.defaultCategory.set(self.categoryOptions[value[2]])
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

def centerizePopup(self, popup):	
    # Get the width and height of the popup window
    popup_width = popup.winfo_reqwidth()
    popup_height = popup.winfo_reqheight()

    # Get the width and height of the parent window
    parent_x = self.winfo_rootx()  # Get the x-coordinate of the parent window
    parent_y = self.winfo_rooty()  # Get the y-coordinate of the parent window
    parent_width = self.winfo_width()  # Get the width of the parent window
    parent_height = self.winfo_height()  # Get the height of the parent window
    x = parent_x + (parent_width - popup_width) // 2
    y = parent_y + (parent_height - popup_height) // 2
    return {"x":x,"y":y}


        

