import tkinter as tk
from src.database.db import Database as dtb
from src.functions.borrowingsPageFunctions.borrowingsPageFunctions import *

def returnBookPopup(self):
	popup = tk.Toplevel()
	popup.title("Επιστροφή βιβλίου")
	
	XYPoints = centerizePopup(self, popup)
	popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")
 
	tk.Label(popup, text="Αξιολόγηση:").grid(row=0, column=0, sticky="w", padx=10)
	rating = tk.IntVar()
	entry_field4 = tk.Spinbox(popup, from_=1, to=3, increment=1, textvariable=rating)
	entry_field4.grid(row=0, column=1, sticky="ew", padx=10)

	insert_button = tk.Button(popup, text="Επιστροφή", command=lambda: returnBook())
	insert_button.grid(row=2, column=0, pady=10, padx=10, sticky="w")
		
	close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
	close_button.grid(row=2, column=1, pady=10, sticky="w")

	def returnBook():
		member_id = self.entry_field1.get()
		book_id = self.entry_field2.get()
		rating_value = rating.get()

		if rating_value:
			dtb.return_book(self.db, member_id, book_id, rating_value)
			showBorrowings(self, self.db, "")
			self.borrowingIDLabel.configure(text=f"-")
			popup.destroy()
		else:
			error_label = tk.Label(popup, text="Πρέπει να εισάγετε αξιολόγηση", fg="red")
			error_label.place(x=10, y=1)
