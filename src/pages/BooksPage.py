import logging
import tkinter as tk
#from src.database.db import Database as dtb
from src.database.library_books_manage import library_books as dtb
from .HomePage import HomePage
#from src.functions.booksPageFunctions.booksPageFunctions import *
from src.pages.popups.newBookPopup import newBookPopup
from src.pages.popups.updateBookPopup import updateBookPopup
from src.pages.popups.deleteBookPopup import deleteBookPopup

class BooksPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.bookShownData = []
		self.selectedBook = {
				'title',
                'category',
                'author',
                'isbn',
                'total_stock',
                'current_stock',
				'book_id'
		}

		self.categoryOptions = {
			"-":"-",
			"Βίπερ":"Βίπερ",
			"Κόμικ":"Κόμικ",
			"Επική ποίηση":"Επική ποίηση",
			"Άρλεκιν":"Άρλεκιν",
			"Νουβέλα":"Νουβέλα",
			"Σχολικά":"Σχολικά",
			"Αγγλική Λογοτεχνία":"Αγγλική Λογοτεχνία",
			"Ιστορικό":"Ιστορικό",
			"Φαντασία":"Φαντασία",
			"Ελληνική Λογοτεχνία":"Ελληνική Λογοτεχνία",
			"Ιστορικό μυθιστόρημα":"Ιστορικό μυθιστόρημα",
			"Κυβερνοπάνκ":"Κυβερνοπάνκ",
			"Μυθιστόρημα":"Μυθιστόρημα",
			"Πληροφορική":"Πληροφορική",
			"Επιστημονική Φαντασία":"Επιστημονική Φαντασία",
		}
		
		# showBooks(self, self.db)

		self.defaultCategory = tk.StringVar()
		self.defaultCategory.set(self.categoryOptions["-"])

		tk.Label(self, text="Τίτλος:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		self.entry_field1 = tk.Entry(self, width=60)
		self.entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=(0,200))

		tk.Label(self, text="Συγγραφέας:").grid(row=1, column=0, sticky="w", padx=10)
		self.entry_field2 = tk.Entry(self, width=60)
		self.entry_field2.grid(row=1, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="Κατηγορία:").grid(row=2, column=0, sticky="w", padx=10)
		self.entry_field3 = tk.OptionMenu(self, self.defaultCategory, *self.categoryOptions)
		self.entry_field3.grid(row=2, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="ISBN:").grid(row=3, column=0, sticky="w", padx=10)
		self.entry_field4 = tk.Entry(self, width=60)
		self.entry_field4.grid(row=3, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text=f"Book ID:").grid(row=4, column=0, sticky="w", padx=10)
		self.bookIDLabel = tk.Label(self, text=f"-")
		self.bookIDLabel.grid(row=4, column=1, sticky="w", padx=(0,200))

		search_button = tk.Button(self, text="Αναζήτηση", width=10, command=lambda: self.search_books())
		search_button.grid(row=5, column=0, pady=10, padx=10,sticky="w")

		self.add_button = tk.Button(self, text="Nέο βιβλίο", width=10, command=lambda: newBookPopup(self))
		self.add_button.grid(row=0, column=2, pady=(10,0), padx=10, sticky="ew")
		
		self.save_button = tk.Button(self, text="Ενημέρωση", state="disabled", width=10, command=lambda:self.updateBookPopup(self.selectedBook))
		self.save_button.grid(row=1, column=2, padx=10, sticky="w")

		self.delete_button = tk.Button(self, text="Διαγραφή", state="disabled", width=10, command=lambda:self.deleteBookPopup())
		self.delete_button.grid(row=2, column=2, padx=10, sticky="w")

		home_button = tk.Button(self, text="Αρχική σελίδα", width=10, command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="w")

		listbox_frame = tk.Frame(self)
		listbox_frame.grid(row=6, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

		self.result_listbox = tk.Listbox(listbox_frame)
		self.result_listbox.grid(row=0, column=0, sticky="nsew")

		scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.result_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.result_listbox.config(yscrollcommand=scrollbar.set)

		self.db = dtb("src/database/members_sqlite.db")

		#self.showBooks(self, self.db, "")
		self.showBooks("")

		self.result_listbox.bind("<Double-Button-1>", lambda event: self.on_double_click(event))

		self.rowconfigure(6, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	### Books Functions
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

	def showBooks(self, title):
		self.deleteFields()
		books = self.db.search_title(title)
		self.bookShownData = books
		self.result_listbox.delete(0, tk.END) 

		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
		self.switchButtonState(0)

	def initialShowBooks(self):
		self.deleteFields()
		books = self.db.search_title("")
		self.bookShownData = books
		self.result_listbox.delete(0, tk.END) 

		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
		self.switchButtonState(0)

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

	def search_books(self):
		title = self.entry_field1.get()
		category = self.defaultCategory.get()
		author = self.entry_field2.get()
		isbn = self.entry_field4.get()

		result_sets = []

		# Debugging print
		logging.info("Search Criteria - Title:{} Category:{} Author:{} ISBN:{}".format(title, category, author, isbn))

		if title:
			#title_results = set(self.db.search_title(title))
			title_results = self.db.search_title(title)
			#result_sets = self.db.search_title(title)
			result_sets.append(title_results)
			print("Title Results:", title_results)  # Debug print statement
		if category:
			print(*self.db.search_category(category))
			category_results = self.db.search_category(category)
			result_sets.append(category_results)
			print("Category Results:", category_results)  # Debug print statement
		if author:
			author_results = set(self.db.search_author(author))
			result_sets.append(author_results)
			print("Author Results:", author_results)  # Debug print statement
		if isbn:
			isbn_results = set(self.db.search_isbn(isbn))
			result_sets.append(isbn_results)
			print("ISBN Results:", isbn_results)  # Debug print statement

		if result_sets:
			#final_results = set.intersection(*result_sets)
			final_results = result_sets
			print("Final Results:", final_results)  # Debug print statement
			self.bookShownData = final_results
			self.result_listbox.delete(0, tk.END)

			for book in final_results:
				# Ensure the book data has the expected structure
				try:
					self.result_listbox.insert(tk.END, f"{book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")
					print(f"Inserted into Listbox: {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")  # Debug print
				except IndexError as e:
					print("Error with book data structure:", book, e)  # Debug print for errors in data structure

			self.switchButtonState(0)
		else:
			self.result_listbox.delete(0, tk.END)
			self.result_listbox.insert(tk.END, "No results found.")


	def deleteBook(self, db, bookId):
	    self.db.delete_book(db, bookId)

	def on_double_click(self, event):
		selection = self.result_listbox.curselection()
		if selection:
			index = selection[0]
			book_list = list(self.bookShownData)  # Convert the set to a list
			value = book_list[index]
			self.deleteFields()
			self.entry_field1.insert(0, value[1])
			self.entry_field2.insert(0, value[3])
			self.defaultCategory.set(self.categoryOptions[value[2]])
			self.entry_field4.insert(0, value[4])
			self.bookID = value[0]
			self.bookIDLabel.configure(text=f"{value[0]}")
			self.switchButtonState(1)

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
