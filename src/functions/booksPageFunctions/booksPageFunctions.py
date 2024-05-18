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

def showBooks(self, db, title):
    deleteFields(self)
    books = dtb.search_title(db, title)
    self.bookShownData = books
    self.result_listbox.delete(0, tk.END) 
    
    for book in books:
        self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
    switchButtonState(self, 0)

def initialShowBooks(self, db):
    deleteFields(self)
    books = dtb.search_title(db, "")
    self.bookShownData = books
    self.result_listbox.delete(0, tk.END) 
    
    for book in books:
        self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
    switchButtonState(self, 0)

# def search_books(self, db):
#     title = self.entry_field1.get()
#     category = self.defaultCategory.get()
#     author = self.entry_field2.get()
#     isbn = self.entry_field4.get()

#     result_sets = []
    
#     if title:
#         result_sets.append(set(dtb.search_title(db, title)))
#         print(*set(dtb.search_title(db, title)))
#     if category:
#         result_sets.append(set(dtb.search_category(db, category)))
#         print(*set(dtb.search_category(db, title)))
#     if author:
#         result_sets.append(set(dtb.search_author(db, author)))
#         print(*set(dtb.search_author(db, title)))
#     if isbn:
#         result_sets.append(set(dtb.search_isbn(db, isbn)))
    
#     if result_sets:
#         final_results = set.intersection(*result_sets)
#         self.bookShownData = final_results
#         self.result_listbox.delete(0, tk.END) 
#         for book in final_results:
#             self.result_listbox.insert(tk.END, f"{  book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
#         switchButtonState(self, 0)
#     else:
#         final_results = set()

def search_books(self, db):
    title = self.entry_field1.get()
    category = self.defaultCategory.get()
    author = self.entry_field2.get()
    isbn = self.entry_field4.get()

    result_sets = []
    
    # Debugging print
    print("Search Criteria - Title:", title, "Category:", category, "Author:", author, "ISBN:", isbn)
    
    if title:
        title_results = set(dtb.search_title(db, title))
        result_sets.append(title_results)
        print("Title Results:", title_results)  # Debug print statement
    # if category:
    #     print(*dtb.search_category(db, category))
    #     category_results = set(dtb.search_category(db, category))
    #     result_sets.append(category_results)
    #     print("Category Results:", category_results)  # Debug print statement
    if author:
        author_results = set(dtb.search_author(db, author))
        result_sets.append(author_results)
        print("Author Results:", author_results)  # Debug print statement
    if isbn:
        isbn_results = set(dtb.search_isbn(db, isbn))
        result_sets.append(isbn_results)
        print("ISBN Results:", isbn_results)  # Debug print statement

    if result_sets:
        final_results = set.intersection(*result_sets)
        print("Final Results:", final_results)  # Debug print statement
        self.bookShownData = final_results
        self.result_listbox.delete(0, tk.END)
        
        for book in final_results:
            # Ensure the book data has the expected structure
            try:
                self.result_listbox.insert(tk.END, f"{book[0]} - {book[2]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")
                print(f"Inserted into Listbox: {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")  # Debug print
            except IndexError as e:
                print("Error with book data structure:", book, e)  # Debug print for errors in data structure
        
        switchButtonState(self, 0)
    else:
        self.result_listbox.delete(0, tk.END)
        self.result_listbox.insert(tk.END, "No results found.")


def deleteBook(self, db, bookId):
    dtb.delete_book(db, bookId)

def on_double_click(self, event):
    selection = self.result_listbox.curselection()
    if selection:
        index = selection[0]
        book_list = list(self.bookShownData)  # Convert the set to a list
        value = book_list[index]
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


        