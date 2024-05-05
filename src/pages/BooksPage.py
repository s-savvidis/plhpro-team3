import tkinter as tk
from src.database.db import Database as dtb
from .HomePage import HomePage

class BooksPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		tk.Label(self, text="Τίτλος:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		self.entry_field1 = tk.Entry(self, width=60)
		self.entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=(0,200))

		tk.Label(self, text="Συγγραφέας:").grid(row=1, column=0, sticky="w", padx=10)
		self.entry_field2 = tk.Entry(self)
		self.entry_field2.grid(row=1, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="Κατηγορία:").grid(row=2, column=0, sticky="w", padx=10)
		self.entry_field3 = tk.Entry(self)
		self.entry_field3.grid(row=2, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="ISBN:").grid(row=3, column=0, sticky="w", padx=10)
		self.entry_field4 = tk.Entry(self)
		self.entry_field4.grid(row=3, column=1, sticky="ew", padx=(0,200))

		submit_button = tk.Button(self, text="Αναζήτηση", command=lambda: self.showBooks(self.db, self.entry_field1.get()))
		submit_button.grid(row=4, column=0, pady=10, padx=10,sticky="w")
		
		home_button = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=4, column=1, pady=10, sticky="w")

		listbox_frame = tk.Frame(self)
		listbox_frame.grid(row=5, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

		self.result_listbox = tk.Listbox(listbox_frame)
		self.result_listbox.grid(row=0, column=0, sticky="nsew")

		scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.result_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.result_listbox.config(yscrollcommand=scrollbar.set)

		self.db = dtb("src/database/members_sqlite.db")

		self.rowconfigure(5, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	def showBooks(self, db, bookTitle):
		books = dtb.search_title(db, bookTitle)
		self.result_listbox.delete(0, tk.END)  		
		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]}") 
		self.entry_field1.delete(0, tk.END) 

