import logging
import tkinter as tk
from src.database.library_borrowing_manage import library_borrowings as dtb
from .HomePage import HomePage
from datetime import date

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
  
		search_button = tk.Button(self, text="Αναζήτηση", width=10, command=lambda: self.showBorrowings(self.entry_field1.get()))
		search_button.grid(row=5, column=0, pady=10, padx=10,sticky="w")

		self.borrow_button = tk.Button(self, text="Δανεισμός", width=10, command=lambda: self.newBorrowingPopup())
		self.borrow_button.grid(row=0, column=2, pady=(10,0), padx=10, sticky="ew")
		
		self.return_button = tk.Button(self, text="Επιστροφή", state="disabled", width=10, command=lambda:self.returnBookPopup())
		self.return_button.grid(row=1, column=2, padx=10, sticky="w")
  
		self.delete_button = tk.Button(self, text="Διαγραφή", state="disabled", width=10, command=lambda: self.deleteBorrowingPopup())
		self.delete_button.grid(row=2, column=2, padx=10, sticky="w")  

		home_button = tk.Button(self, text="Αρχική σελίδα", width=10, command=lambda:self.handleHomePage(controller))
		home_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="w")

		listbox_frame = tk.Frame(self)
		listbox_frame.grid(row=6, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

		self.result_listbox = tk.Listbox(listbox_frame)
		self.result_listbox.grid(row=0, column=0, sticky="nsew")

		scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.result_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.result_listbox.config(yscrollcommand=scrollbar.set)

		self.db = dtb("src/database/members_sqlite.db")

		self.result_listbox.bind("<Double-Button-1>", lambda event: self.on_double_click(event))

		self.rowconfigure(6, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	
	### Borrowings Functions
	def deleteFields(self):
		self.entry_field1.delete(0, tk.END)
		self.entry_field2.delete(0, tk.END)
		self.entry_field3.delete(0, tk.END)
		self.entry_field4.delete(0, tk.END)

	def switchButtonState(self, value):
		if (value == 0):
			self.return_button['state'] = tk.DISABLED
			self.delete_button['state'] = tk.DISABLED
		elif (value == 1):
			self.return_button['state'] = tk.NORMAL
			self.delete_button['state'] = tk.NORMAL

	def showBorrowings(self, borrowingID):
		self.deleteFields()
		borrowings = self.db.search_borrowing(borrowingID)
		self.borrowingShownData = borrowings
		self.result_listbox.delete(0, tk.END) 

		for borrowing in borrowings:
			user = self.db.search_id_member(borrowing[2])
			book = self.db.search_id_book(borrowing[1])
			returnStatus = "Ναι" if borrowing[4] == 1 else "Όχι"

			self.result_listbox.insert(tk.END, f" {user[0][1]} (id: {borrowing[2]}) - {book[0][1]} (id: {borrowing[1]}) - 'Εχει επιστραφεί: {returnStatus} - Βαθμολογία: {borrowing[5]}") 
		self.switchButtonState(0)

	def deleteBorrowing(self, borrowingId):
		""" Διαγραφή δανεισμού με χρήση borrowingId """
		self.db.delete_borrowing(borrowingId)

	def on_double_click(self, event):
		selection = self.result_listbox.curselection()
		if selection:
			index = selection[0]
			borrowing_list = list(self.borrowingShownData)  # Convert the set to a list
			value = borrowing_list[index]
			self.deleteFields()
			self.entry_field1.insert(0, value[2])
			self.entry_field2.insert(0, value[1])
			self.entry_field3.insert(0, value[3])
			self.entry_field4.insert(0, value[5])
			self.borrowingID = value[0]
			self.borrowingIDLabel.configure(text=f"{value[0]}")
			self.switchButtonState(1)

			self.selectedBorrowing = {
            	'member_id': value[2],
            	'book_id': value[1],
            	'date': value[3],
            	'rating': value[5],
            	'borrow_id': value[0]
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

	def handleHomePage(self, controller):
		self.deleteFields()
		self.result_listbox.delete(0, tk.END) 
		controller.show_frame(HomePage)
		
	###############################################################
	# Pop-up code
	def newBorrowingPopup(self):
		popup = tk.Toplevel()
		popup.title("Εισαγωγή νέου δανεισμού")
	
		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		currentDate = date.today().strftime("%Y-%m-%d")

		tk.Label(popup, text="ID μέλους:").grid(row=0, column=0, sticky="w", pady=(20,0), padx=10)  
		entry_field1 = tk.Entry(popup)
		entry_field1.grid(row=0, column=1, sticky="ew", pady=(20,0), padx=10)

		tk.Label(popup, text="ID βιβλίου:").grid(row=1, column=0, sticky="w", padx=10)
		entry_field2 = tk.Entry(popup)
		entry_field2.grid(row=1, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Ημερομηνία:").grid(row=2, column=0, sticky="w", padx=10)
		entry_field3 = tk.Entry(popup)
		entry_field3.insert(0, currentDate)
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
	
				self.db.borrow_book(member_id, book_id, date)
				self.showBorrowings("") 
				self.borrowingIDLabel.configure(text=f"-")
				popup.destroy()
			else:
				error_label = tk.Label(popup, text="Πρέπει να συμπληρώσετε όλα τα πεδία", fg="red")
				error_label.place(x=10, y=1)

	def deleteBorrowingPopup(self):
		popup = tk.Toplevel()

		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		tk.Label(popup, text="Επιθυμείτε να διαγράψετε την επιλεγμένη καταχώρηση δανεισμού;").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

		insert_button = tk.Button(popup, text="Ναι, διαγραφή", command= lambda: deleteAndClose())
		insert_button.grid(row=1, column=0, pady=10, padx=20,sticky="w")
		
		close_button = tk.Button(popup, text="Ακύρωση", command=popup.destroy)
		close_button.grid(row=1, column=1, pady=10, padx=20, sticky="e")

		def deleteAndClose():
			self.deleteBorrowing(self.selectedBorrowing["borrow_id"])
			self.showBorrowings("")
			self.borrowingIDLabel.configure(text=f"-")
			popup.destroy()

	def returnBookPopup(self):
		popup = tk.Toplevel()
		popup.title("Επιστροφή βιβλίου")
	
		XYPoints = self.centerizePopup(popup)
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
				self.db.return_book(member_id, book_id, rating_value)
				self.showBorrowings("")
				self.borrowingIDLabel.configure(text=f"-")
				popup.destroy()
			else:
				error_label = tk.Label(popup, text="Πρέπει να εισάγετε αξιολόγηση", fg="red")
				error_label.place(x=10, y=1)
	
	