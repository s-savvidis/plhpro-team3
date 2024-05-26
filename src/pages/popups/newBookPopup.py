import tkinter as tk
from src.database.db import Database as dtb
from src.functions.booksPageFunctions.booksPageFunctions import *


def newBookPopup(self):
	popup = tk.Toplevel()
	popup.title("Εισαγωγή νέου βιβλίου")
	
	XYPoints = centerizePopup(self, popup)
	popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

	defaultCategory = tk.StringVar()
	defaultCategory.set(self.categoryOptions["-"])

	tk.Label(popup, text="Τίτλος*:").grid(row=0, column=0, sticky="w", pady=(20,0), padx=10)  
	entry_field1 = tk.Entry(popup)
	entry_field1.grid(row=0, column=1, sticky="ew", pady=(20,0), padx=10)

	tk.Label(popup, text="Συγγραφέας*:").grid(row=1, column=0, sticky="w", padx=10)
	entry_field2 = tk.Entry(popup)
	entry_field2.grid(row=1, column=1, sticky="ew", padx=10)

	tk.Label(popup, text="Κατηγορία:").grid(row=2, column=0, sticky="w", padx=10)
	entry_field3 = tk.OptionMenu(popup, defaultCategory, *self.categoryOptions)
	entry_field3.grid(row=2, column=1, sticky="ew", padx=10)

	tk.Label(popup, text="ISBN*:").grid(row=3, column=0, sticky="w", padx=10)
	entry_field4 = tk.Entry(popup)
	entry_field4.grid(row=3, column=1, sticky="ew", padx=10)

	tk.Label(popup, text="Γενικό απόθεμα:").grid(row=4, column=0, sticky="w", padx=10)
	tStock=tk.IntVar(value=0)
	entry_field5 = tk.Spinbox(popup, from_= 0, to = 50, increment=1,
	textvariable=tStock)
	entry_field5.grid(row=4, column=1, sticky="ew", padx=10)

	tk.Label(popup, text="Τωρινό απόθεμα:").grid(row=5, column=0, sticky="w", padx=10)
	cStock=tk.IntVar(value=0)
	entry_field6 = tk.Spinbox(popup, from_= 0, to = 50, width=4, increment=1,
	textvariable=cStock)
	entry_field6.grid(row=5, column=1, sticky="ew", padx=10)

	insert_button = tk.Button(popup, text="Εισαγωγή", command= lambda: addBook())
	insert_button.grid(row=6, column=0, pady=10, padx=10,sticky="w")
	
	close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
	close_button.grid(row=6, column=1, pady=10, sticky="w")

	def addBook():
		bookDetails = {
			'title': entry_field1.get(),
			'category': defaultCategory.get(),
			'author': entry_field2.get(),
			'isbn': entry_field4.get(),
			'total_stock': entry_field5.get(),
			'current_stock': entry_field6.get()
		}
		if (
		entry_field1.get()
		and entry_field2.get()
		and entry_field4.get()
		):
			dtb.insert_book(self.db, bookDetails)
			showBooks(self, self.db, "")
			self.bookIDLabel.configure(text=f"-")
			popup.destroy()
		else:
			error_label = tk.Label(popup, text="Συμπληρώστε όλα τα απαραίτητα πεδία με *", fg="red")
			error_label.place(x=40, y=1)

