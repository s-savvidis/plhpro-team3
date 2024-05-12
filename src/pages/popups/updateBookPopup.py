import tkinter as tk
from src.database.db import Database as dtb
from src.functions.booksPageFunctions.booksPageFunctions import *

def updateBookPopup(self, bookDetails):
		popup = tk.Toplevel()
		popup.title("Ενημέρωση βιβλίου")

		XYPoints = centerizePopup(self, popup)
		popup.geometry(f"+{XYPoints["x"]}+{XYPoints["y"]}")

		tk.Label(popup, text="Γενικό απόθεμα:").grid(row=0, column=0, sticky="w", padx=10)
		tStock=tk.IntVar(value=bookDetails["total_stock"])
		entry_field5 = tk.Spinbox(popup, from_= 0, to = 50, increment=1,
    	textvariable=tStock)
		entry_field5.grid(row=0, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Τωρινό απόθεμα:").grid(row=1, column=0, sticky="w", padx=10)
		cStock=tk.IntVar(value=bookDetails["current_stock"])
		entry_field6 = tk.Spinbox(popup, from_= 0, to = 50, width=4, increment=1,
    	textvariable=cStock)
		entry_field6.grid(row=1, column=1, sticky="ew", padx=10)

		insert_button = tk.Button(popup, text="Ενημέρωση", command= lambda: updateBook(entry_field5.get(), entry_field6.get()))
		insert_button.grid(row=2, column=0, pady=10, padx=10,sticky="w")
		
		close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
		close_button.grid(row=2, column=1, pady=10, sticky="w")

		def updateBook(tStock, cStock):
			bookDetails = {
				'title': self.entry_field1.get(),
                'category': self.defaultCategory.get(),
                'author': self.entry_field2.get(),
                'isbn': self.entry_field4.get(),
                'total_stock': tStock,
                'current_stock': cStock,
				'book_id': self.selectedBook["book_id"]
			}
			dtb.update_book(self.db, bookDetails)
			showBooks(self, self.db, "")
			self.bookIDLabel.configure(text=f"-")
			popup.destroy()