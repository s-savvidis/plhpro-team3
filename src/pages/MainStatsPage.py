import logging
import tkinter as tk
from src.database.library_borrowing_manage import library_borrowings as dtb
from .HomePage import HomePage

class StatsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.bookShownData = []
		self.selectedBook = {
				'title',
                'category',
                'author',
                'isbn',
                'total_stock',
                'current_stock',
				'book_id'
		}

		self.categoryOptions = {
			"-":"-",
			"Βίπερ":"Βίπερ",
			"Κόμικ":"Κόμικ",
			"Επική ποίηση":"Επική ποίηση",
			"Άρλεκιν":"Άρλεκιν",
			"Νουβέλα":"Νουβέλα",
			"Σχολικά":"Σχολικά",
			"Αγγλική Λογοτεχνία":"Αγγλική Λογοτεχνία",
			"Ιστορικό":"Ιστορικό",
			"Φαντασία":"Φαντασία",
			"Ελληνική Λογοτεχνία":"Ελληνική Λογοτεχνία",
			"Ιστορικό μυθιστόρημα":"Ιστορικό μυθιστόρημα",
			"Κυβερνοπάνκ":"Κυβερνοπάνκ",
			"Μυθιστόρημα":"Μυθιστόρημα",
			"Πληροφορική":"Πληροφορική",
			"Επιστημονική Φαντασία":"Επιστημονική Φαντασία",
		}

		search_button = tk.Button(self, text="Πλήθος βιβλίων ανα μέλος σε χρονική περίοδο", width=50, command=lambda: self.ui_stats_books_member())
		search_button.grid(row=0, column=0, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Κατανομή προτιμήσεων δανεισμού ανά μέλος", width=50, command=lambda: self.ui_stats_borrowing_member())
		search_button.grid(row=0, column=1, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Ιστορικό δανεισμού ανά μέλος", width=50, command=lambda: self.ui_stats_members())
		search_button.grid(row=1, column=1, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Πλήθος δανεισμών ανά συγγραφέα", width=50, command=lambda: self.ui_stats_writer())
		search_button.grid(row=1, column=0, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Πλήθος δανεισμών ανά ηλικία", width=50, command=lambda: self.ui_stats_age())
		search_button.grid(row=2, column=1, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Πλήθος δανεισμών ανά φύλο", width=50, command=lambda: self.ui_stats_gender())
		search_button.grid(row=2, column=0, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Κατανομή προτιμήσεων όλων των μελών ανά κατηγορία για χρονική περίοδο", width=50, command=lambda: self.ui_pref_members())
		search_button.grid(row=3, column=0, pady=10, padx=10,sticky="w")

		#
		# Απο και Έως πλαίσια κειμένου
		#
		frameApo = tk.Frame(self)
		frameApo.grid(row=4, column=0, columnspan=1, padx=5, pady=5)
		tk.Label(frameApo, text="Από:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
		self.entry_apo = tk.Entry(frameApo, width=10)
		self.entry_apo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
		self.entry_apo.insert(0, "2023-02-01")

		tk.Label(frameApo, text="Εώς:").grid(row=4, column=3, sticky="w", padx=5, pady=5)
		self.entry_eos = tk.Entry(frameApo, width=10)
		self.entry_eos.grid(row=4, column=4, sticky="ew", padx=5, pady=5)
		self.entry_eos.insert(0, "2023-02-28")


		#self.delete_button = tk.Button(self, text="Διαγραφή", state="disabled", width=10, command=lambda:self.deleteBookPopup())
		#self.delete_button.grid(row=2, column=2, padx=10, sticky="w")

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

		self.result_listbox.bind("<Double-Button-1>", lambda event: self.on_double_click(event))

		self.rowconfigure(6, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	### Statistics Functions
	def ui_stats_writer(self):
		myStats = self.db.stats_author()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END) 
		self.result_listbox.insert(tk.END, "| {:^8} | {:^30}".format("Βιβλία","Συγγραφέας"))

		for stat in myStats:
			#self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")
			self.result_listbox.insert(tk.END, "| {:^8} | {:<30}".format(stat[0],stat[1]))
		self.switchButtonState(0)

	def ui_stats_age(self):
		myStats = self.db.stats_age()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8} | {:^30}".format("Βιβλία","Ηλικία"))

		for stat in myStats:
			self.result_listbox.insert(tk.END, "| {:^8} | {:<30}".format(stat[1],stat[0]))
		self.switchButtonState(0)

	def ui_stats_members(self):
		myStats = self.db.stats_borrowing_member()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8} | {:^30}".format("Βιβλία","Ηλικία"))

		for stat in myStats:
			#self.result_listbox.insert(tk.END, "| {:^8} | {:<30}".format(stat[1],stat[0]))
			self.result_listbox.insert(tk.END, "{}".format(stat))
		self.switchButtonState(0)

	def ui_stats_gender(self):
		myStats = self.db.stats_gender()
		myGender = ""
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8} | {:^30}".format("Βιβλία","Ηλικία"))

		for stat in myStats:
			if stat[0] == "m":
				myGender = "Άρρεν"
			elif stat[0] == "f":
				myGender = "Θήλυ"
			else:
				myGender = "Άλλο"
			self.result_listbox.insert(tk.END, "| {:^8} | {:<30}".format(stat[1],myGender))
		self.switchButtonState(0)

	def ui_stats_borrowing_member(self):
		myStats = self.db.stats_borrowing_member()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8} | {:^30}".format("Βιβλία","Ηλικία"))

		print(myStats)
		for stat in myStats:
			self.result_listbox.insert(tk.END, "| {:^8} | {:<30}".format(stat[1],stat[0]))
		self.switchButtonState(0)
	

	def ui_pref_members(self):
		""" Κατανομή προτιμήσεων όλων των μελών κατα περίοδο """
		periodApo = self.entry_apo.get()
		periodDisect = periodApo.strip().split("-")
		if (len(periodDisect) != 3) or (int(periodDisect[0]) > 2024 ) or (int(periodDisect[0]) < 2023) or (int(periodDisect[1]) < 1) or (int(periodDisect[1]) > 12) or (int(periodDisect[2]) < 1) or (int(periodDisect[2]) > 31):
			logging.error("Wrong Apo date")
			self.wrongDatePopup()
			return False

		periodEos = self.entry_eos.get()
		periodDisect = periodEos.strip().split("-")
		if (len(periodDisect) != 3) or (int(periodDisect[0]) > 2024 ) or (int(periodDisect[0]) < 2023) or (int(periodDisect[1]) < 1) or (int(periodDisect[1]) > 12) or (int(periodDisect[2]) < 1) or (int(periodDisect[2]) > 31):
			logging.error("Wrong Eos date")
			self.wrongDatePopup()
			return False

		myStats = self.db.stats_pref_members(periodApo, periodEos)
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8} | {:^30}".format("Κατηγορία","Πλήθος προτίμησης βιβλίων"))
		print(myStats)
		for stat in myStats:
			self.result_listbox.insert(tk.END, "| {:^8} | {:<30}".format(stat[1],stat[0]))
		self.switchButtonState(0)

	def ui_stats_books_member(self):
		""" Πλήθος βιβλίων ανα μέλος σε χρονική περίοδο """
		periodApo = self.entry_apo.get()
		periodDisect = periodApo.strip().split("-")
		if (len(periodDisect) != 3) or (int(periodDisect[0]) > 2024 ) or (int(periodDisect[0]) < 2023) or (int(periodDisect[1]) < 1) or (int(periodDisect[1]) > 12) or (int(periodDisect[2]) < 1) or (int(periodDisect[2]) > 31):
			logging.error("Wrong Apo date")
			self.wrongDatePopup()
			return False

		periodEos = self.entry_eos.get()
		periodDisect = periodEos.strip().split("-")
		if (len(periodDisect) != 3) or (int(periodDisect[0]) > 2024 ) or (int(periodDisect[0]) < 2023) or (int(periodDisect[1]) < 1) or (int(periodDisect[1]) > 12) or (int(periodDisect[2]) < 1) or (int(periodDisect[2]) > 31):
			logging.error("Wrong Eos date")
			self.wrongDatePopup()
			return False

		myStats = self.db.stats_books_member(periodApo, periodEos)
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)

		line_format = "| {:^30} | {:<25} |"
		line = line_format.format("Όνομα μέλους", "Πλήθος προτίμησης βιβλίων")
		self.result_listbox.insert(tk.END, line)
		#print(myStats)

		for stat in myStats:
			line = line_format.format(stat[1], stat[0])
			self.result_listbox.insert(tk.END, line)
		self.switchButtonState(0)


	def deleteFields(self):
		self.entry_field1.delete(0, tk.END)
		self.entry_field2.delete(0, tk.END)
		self.defaultCategory.set(self.categoryOptions["-"])
		self.entry_field4.delete(0, tk.END)

	def switchButtonState(self, value):
		if (value == 0):
			self.save_button['state'] = tk.DISABLED
			self.delete_button['state'] = tk.DISABLED
		elif (value == 1):
			self.save_button['state'] = tk.NORMAL
			self.delete_button['state'] = tk.NORMAL

	def showBooks(self, title):
		self.deleteFields()
		books = self.db.search_title(title)
		self.bookShownData = books
		self.result_listbox.delete(0, tk.END)

		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
		self.switchButtonState(0)

	def initialShowBooks(self):
		self.deleteFields()
		books = self.db.search_title("")
		self.bookShownData = books
		self.result_listbox.delete(0, tk.END) 

		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
		self.switchButtonState(0)

	def search_books(self):
		title = self.entry_field1.get()
		category = self.defaultCategory.get()
		author = self.entry_field2.get()
		isbn = self.entry_field4.get()

		result_sets = []

		# Debugging print
		logging.info("Search Criteria - Title:{} Category:{} Author:{} ISBN:{}".format(title, category, author, isbn))

		if title:
			# Αναζήτηση βάση τίτλου. Μηδενισμός υπολοίπων.
			category = "-"
			author = ""
			isbn = ""
			result_sets = self.db.search_title(title)
			logging.debug("Title Results:{}".format(result_sets))  # Debug print statement
		if category != "-":
			# Αναζήτηση βάση κατηγορίας. Μηδενισμός υπολοίπων.
			author = ""
			isbn = ""
			result_sets = self.db.search_category(category)
			logging.debug("Category Results:{}".format(result_sets))  # Debug print statement
		if author:
			# Αναζήτηση βάση συγγραφέα. Μηδενισμός υπολοίπων.
			isbn = ""
			result_sets = self.db.search_author(author)
			logging.info("Author Results:{}".format(result_sets))  # Debug print statement
		if isbn:
			# Αναζήτηση βάση ISBN.
			result_sets = set(self.db.search_isbn(isbn))
			logging.debug("ISBN Results: {}".format(isbn_results))  # Debug print statement

		if result_sets:
			final_results = result_sets
			logging.debug("Final Results: {}".format(final_results))  # Debug print statement
			self.bookShownData = final_results
			self.result_listbox.delete(0, tk.END)

			for book in final_results:
				# Ensure the book data has the expected structure
				try:
					print(book)
					self.result_listbox.insert(tk.END, f"{book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")
					print(f"Inserted into Listbox: {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}")  # Debug print
				except IndexError as e:
					print("Error with book data structure:", book, e)  # Debug print for errors in data structure

			self.switchButtonState(0)
		else:
			self.result_listbox.delete(0, tk.END)
			self.result_listbox.insert(tk.END, "No results found.")


	def deleteBook(self, bookId):
		""" Διαγραφή Βιβλίου με χρήση bookId """
		self.db.delete_book(db, bookId)

	def on_double_click(self, event):
		selection = self.result_listbox.curselection()
		if selection:
			index = selection[0]
			book_list = list(self.bookShownData)  # Convert the set to a list
			value = book_list[index]
			self.deleteFields()
			self.entry_field1.insert(0, value[1])
			self.entry_field2.insert(0, value[3])
			self.defaultCategory.set(self.categoryOptions[value[2]])
			self.entry_field4.insert(0, value[4])
			self.bookID = value[0]
			self.bookIDLabel.configure(text=f"{value[0]}")
			self.switchButtonState(1)

			self.selectedBook = {
	            'title': value[1],
	            'category': value[3],
	            'author': value[2],
	            'isbn': value[4],
	            'total_stock': value[5],
	            'current_stock': value[6],
	            'book_id': value[0]
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

	###############################################################
	# Pop-up code
	def wrongDatePopup(self):
		""" Popup παράθυρο μηνύματος εσφαλμένης ημερομηνίας """			
		popup = tk.Toplevel()
		popup.title("Εσφαλμένη ημερομηνία")

		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")
        
		tk.Label(popup, text="Εσφαλμένη ημερομηνία. Η μορφή πρέπει να είναι 2023-12-01.").grid(row=0, column=0, columnspan=2, pady=5, padx=10)
		tk.Label(popup, text="Μεταξύ > 2023-01-01 και 2024-12-12").grid(row=1, column=0, columnspan=2, pady=5, padx=10)
		ok_button = tk.Button(popup, text="OK", command= lambda: popup.destroy())
		ok_button.grid(row=2, column=1, pady=10, padx=20,sticky="w")
  

	def deleteBookPopup(self):
			popup = tk.Toplevel()

			XYPoints = self.centerizePopup(popup)
			popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

			tk.Label(popup, text="Επιθυμείτε να διαγράψετε την επιλεγμένη καταχώρηση βιβλίου;").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

			insert_button = tk.Button(popup, text="Ναι, διαγραφή", command= lambda: deleteAndClose())
			insert_button.grid(row=1, column=0, pady=10, padx=20,sticky="w")

			close_button = tk.Button(popup, text="Ακύρωση", command=popup.destroy)
			close_button.grid(row=1, column=1, pady=10, padx=20, sticky="e")

			def deleteAndClose():
				self.deleteBook(self.selectedBook["book_id"])
				self.showBooks("")
				self.bookIDLabel.configure(text=f"-")
				popup.destroy()
