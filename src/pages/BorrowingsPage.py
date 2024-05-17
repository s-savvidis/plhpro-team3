import tkinter as tk
from src.database.db import Database as dtb
from .HomePage import HomePage
from src.functions.borrowingsPageFunctions.borrowingsPageFunctions import *
from src.pages.popups.newBorrowingPopup import newBorrowingPopup
from src.pages.popups.returnBookPopup import returnBookPopup
from src.pages.popups.deleteBorrowingPopup import deleteBorrowingPopup
		
class BorrowingsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.borrowingShownData = []
		self.selectedBorrowing = {
				'borrow_id',
    			'book_id',
                'member_id',
                'date',
                'return_Status',
                'rating'
		}

		tk.Label(self, text="ID μέλους:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		self.entry_field1 = tk.Entry(self, width=60)
		self.entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=(0,200))

		tk.Label(self, text="ID βιβλίου:").grid(row=1, column=0, sticky="w", padx=10)
		self.entry_field2 = tk.Entry(self, width=60)
		self.entry_field2.grid(row=1, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="Ημερομηνία:").grid(row=2, column=0, sticky="w", padx=10)
		self.entry_field3 = tk.Entry(self, width=60)
		self.entry_field3.grid(row=2, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text=f"Αξιολόγηση:").grid(row=4, column=0, sticky="w", padx=10)
		self.entry_field4 = tk.Entry(self, width=60)
		self.entry_field4.grid(row=4, column=1, sticky="w", padx=(0,200))

		tk.Label(self, text=f"Borrowing ID:").grid(row=5, column=0, sticky="w", padx=10)
		self.borrowingIDLabel = tk.Label(self, text=f"-")
		self.borrowingIDLabel.grid(row=5, column=1, sticky="w", padx=(0,200))
  
		search_button = tk.Button(self, text="Αναζήτηση", width=10, command=lambda: showBorrowings(self, self.db, self.entry_field1.get()))
		search_button.grid(row=5, column=0, pady=10, padx=10,sticky="w")

		self.add_button = tk.Button(self, text="Δανεισμοός", width=10, command=lambda: newBorrowingPopup(self))
		self.add_button.grid(row=0, column=2, pady=(10,0), padx=10, sticky="ew")
		
		self.save_button = tk.Button(self, text="Επιστροφή", state="disabled", width=10, command=lambda:returnBookPopup(self))
		self.save_button.grid(row=1, column=2, padx=10, sticky="w")
  
		self.delete_button = tk.Button(self, text="Διαγραφή", state="disabled", width=10, command=lambda: deleteBorrowingPopup(self))
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

		self.result_listbox.bind("<Double-Button-1>", lambda event: on_double_click(self, event))

		self.rowconfigure(6, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)