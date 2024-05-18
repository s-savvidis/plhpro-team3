import tkinter as tk
from src.database.db import Database as dtb
from src.functions.borrowingsPageFunctions.borrowingsPageFunctions import *


def newBorrowingPopup(self):
	popup = tk.Toplevel()
	popup.title("Εισαγωγή νέου δανεισμού")
	
	XYPoints = centerizePopup(self, popup)
	popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

	tk.Label(popup, text="ID μέλους:").grid(row=0, column=0, sticky="w", pady=(20,0), padx=10)  
	entry_field1 = tk.Entry(popup)
	entry_field1.grid(row=0, column=1, sticky="ew", pady=(20,0), padx=10)

	tk.Label(popup, text="ID βιβλίου:").grid(row=1, column=0, sticky="w", padx=10)
	entry_field2 = tk.Entry(popup)
	entry_field2.grid(row=1, column=1, sticky="ew", padx=10)

	tk.Label(popup, text="Ημερομηνία:").grid(row=2, column=0, sticky="w", padx=10)
	entry_field3 = tk.Entry(popup)
	entry_field3.grid(row=2, column=1, sticky="ew", padx=10)

	insert_button = tk.Button(popup, text="Εισαγωγή", command= lambda: newBorrowing())
	insert_button.grid(row=6, column=0, pady=10, padx=10,sticky="w")
	
	close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
	close_button.grid(row=6, column=1, pady=10, sticky="w")

	def newBorrowing():        
		member_id = entry_field1.get()
		book_id = entry_field2.get()
		date = entry_field3.get()
		if entry_field1.get() and entry_field2.get() and entry_field3.get():
	
			dtb.borrow_book(self.db, member_id, book_id, date)
			showBorrowings(self, self.db, "") 
			self.borrowingIDLabel.configure(text=f"-")
			popup.destroy()
		else:
			error_label = tk.Label(popup, text="Πρέπει να συμπληρώσετε όλα τα πεδία", fg="red")
			error_label.place(x=10, y=1)
