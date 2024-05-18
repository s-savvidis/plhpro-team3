import tkinter as tk
from src.functions.booksPageFunctions.booksPageFunctions import *

def deleteBookPopup(self):
		popup = tk.Toplevel()

		XYPoints = centerizePopup(self, popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		tk.Label(popup, text="Επιθυμείτε να διαγράψετε την επιλεγμένη καταχώρηση βιβλίου;").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

		insert_button = tk.Button(popup, text="Ναι, διαγραφή", command= lambda: deleteAndClose())
		insert_button.grid(row=1, column=0, pady=10, padx=20,sticky="w")
		
		close_button = tk.Button(popup, text="Ακύρωση", command=popup.destroy)
		close_button.grid(row=1, column=1, pady=10, padx=20, sticky="e")

		def deleteAndClose():
			deleteBook(self, self.db, self.selectedBook["book_id"])
			showBooks(self, self.db, "")
			self.bookIDLabel.configure(text=f"-")
			popup.destroy()