import tkinter as tk
from src.functions.borrowingsPageFunctions.borrowingsPageFunctions import *

def deleteBorrowingPopup(self):
		popup = tk.Toplevel()

		XYPoints = centerizePopup(self, popup)
		popup.geometry(f"+{XYPoints["x"]}+{XYPoints["y"]}")

		tk.Label(popup, text="Επιθυμείτε να διαγράψετε την επιλεγμένη καταχώρηση δανεισμού;").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

		insert_button = tk.Button(popup, text="Ναι, διαγραφή", command= lambda: deleteAndClose())
		insert_button.grid(row=1, column=0, pady=10, padx=20,sticky="w")
		
		close_button = tk.Button(popup, text="Ακύρωση", command=popup.destroy)
		close_button.grid(row=1, column=1, pady=10, padx=20, sticky="e")

		def deleteAndClose():
			deleteBorrowing(self, self.db, self.selectedBorrowing["borrow_id"])
			showBorrowings(self, self.db, "")
			self.borrowingIDLabel.configure(text=f"-")
			popup.destroy()