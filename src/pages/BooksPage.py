import tkinter as tk
from src.database.db import Database as dtb
from .HomePage import HomePage

class BooksPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.bookShownData = []

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

		tk.Label(self, text=f"Book ID:").grid(row=4, column=0, sticky="w", padx=10)
		self.bookID = tk.Label(self, text=f"-")
		self.bookID.grid(row=4, column=1, sticky="ew", padx=(0,200))

		search_button = tk.Button(self, text="Αναζήτηση", command= lambda: self.showBooks(self.db, self.entry_field1.get()))
		search_button.grid(row=5, column=0, pady=10, padx=10,sticky="w")
		
		self.save_button = tk.Button(self, text="Αποθήκευση", state="disabled", command=lambda:print("save"))
		self.save_button.grid(row=5, column=1, pady=10, sticky="w")

		self.delete_button = tk.Button(self, text="Διαγραφή", state="disabled", command=lambda:print("delete"))
		self.delete_button.grid(row=5, column=2, pady=10, padx=10, sticky="w")

		self.add_button = tk.Button(self, text="Nέο βιβλίο", command=lambda:print("add"))
		self.add_button.grid(row=0, column=2, pady=(10,0), padx=10, sticky="ew")

		home_button = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=7, column=0, pady=10, padx=10, sticky="w")

		listbox_frame = tk.Frame(self)
		listbox_frame.grid(row=6, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

		self.result_listbox = tk.Listbox(listbox_frame)
		self.result_listbox.grid(row=0, column=0, sticky="nsew")

		scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.result_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.result_listbox.config(yscrollcommand=scrollbar.set)

		self.db = dtb("src/database/members_sqlite.db")

		self.result_listbox.bind("<Double-Button-1>", self.on_double_click)

		self.rowconfigure(6, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	def deleteFilds(self):
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
		self.deleteFilds()
		books = dtb.search_title(db, bookTitle)
		self.bookShownData = books
		self.result_listbox.delete(0, tk.END) 
		
		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]}") 
		self.switchButtonState(0)
	
	def on_double_click(self, event):
		selection = self.result_listbox.curselection()
		if selection:
			index = selection[0]
			value = self.bookShownData[index]
			self.deleteFilds()
			self.entry_field1.insert(0, value[1])
			self.entry_field2.insert(0, value[3])
			self.entry_field3.insert(0, value[2])
			self.entry_field4.insert(0, value[4])
			self.bookID.configure(text=f"Book ID: {value[4]}")
			self.switchButtonState(1)
			




		