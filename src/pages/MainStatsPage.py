import logging
import tkinter as tk
from src.database.library_borrowing_manage import library_borrowings as dtb
from .HomePage import HomePage

class StatsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.bookShownData = []
        
        # Πρώτη γραμμή κουμπιών
		search_button = tk.Button(self, text="Πλήθος βιβλίων μελών σε χρονική περίοδο", width=50, command=lambda: self.ui_stats_books_member())
		search_button.grid(row=0, column=0, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Κατανομή προτιμήσεων μελών ανά κατηγορία", width=50, command=lambda: self.ui_pref_members())
		search_button.grid(row=0, column=1, pady=10, padx=10,sticky="w")

		# Δεύτερη γραμμή κουμπιών	
		search_button = tk.Button(self, text="Ιστορικό δανεισμού μελών", width=50, command=lambda: self.ui_stats_members())
		search_button.grid(row=1, column=1, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Πλήθος δανεισμών ανά συγγραφέα", width=50, command=lambda: self.ui_stats_writer())
		search_button.grid(row=1, column=0, pady=10, padx=10,sticky="w")

		# Τρίτη γραμμή κουμπιών
		search_button = tk.Button(self, text="Πλήθος δανεισμών ανά ηλικία", width=50, command=lambda: self.ui_stats_age())
		search_button.grid(row=2, column=1, pady=10, padx=10,sticky="w")

		search_button = tk.Button(self, text="Πλήθος δανεισμών ανά φύλο", width=50, command=lambda: self.ui_stats_gender())
		search_button.grid(row=2, column=0, pady=10, padx=10,sticky="w")


		#
		# Απο και Έως πλαίσια κειμένου ημερομηνίας.
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

		home_button = tk.Button(self, text="Αρχική σελίδα", width=10, command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="w")

		listbox_frame = tk.Frame(self)
		listbox_frame.grid(row=6, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")
		# Τέλος Απο και Έως πλαίσια κειμένου ημερομηνίας.

		custom_font = ('Courier New', 12, 'bold')
		self.result_listbox = tk.Listbox(listbox_frame, font=custom_font)
		self.result_listbox.grid(row=0, column=0, sticky="nsew")

		scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.result_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.result_listbox.config(yscrollcommand=scrollbar.set)
		# Σύνδεση με ΒΔ και χρήση κλάσης
		self.db = dtb("src/database/members_sqlite.db")

		self.rowconfigure(6, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	### Statistics Functions
	def ui_stats_writer(self):
		""" Πλήθος δανεισμών ανα συγγραφέα """
		myStats = self.db.stats_author()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END) 
		self.result_listbox.insert(tk.END, f"|{'Βιβλία':^8} | {'Συγγραφέας':^30}|")
		#self.result_listbox.insert(tk.END, "+"+"-"*41+"+")

		for stat in myStats:
			self.result_listbox.insert(tk.END, f"| {stat[0]:<8}| {stat[1]:<30}|")	

	def ui_stats_age(self):
		""" Πλήθος δανεισμών ανα ηλικία """
		myStats = self.db.stats_age()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8s} | {:^10s} |".format("Βιβλία","Ηλικία"))

		for stat in myStats:
			self.result_listbox.insert(tk.END, "| {:^8d} | {:^10d} |".format(stat[1],stat[0]))

	def ui_stats_members(self):
		""" Δανεισμοί όλων των μελών """	
		myStats = self.db.stats_member_history_all()
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, f"|{'Mέλος':<30} | {'Κατηγορία':<25} | {'Τίτλος':<50} | {'Ημ. δανεισμού':<14} |")

		for stat in myStats:
			self.result_listbox.insert(tk.END, f"|{stat[1]:<30} | {stat[2]:<25} | {stat[3]:<50} | {stat[4]:<14} |")

	def ui_stats_gender(self):
		""" Πλήθος δανεισμών ανα φύλο """
		myStats = self.db.stats_gender()
		myGender = ""
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^8} | {:^10} |".format("Βιβλία","Φύλο"))

		for stat in myStats:
			if stat[0] == "m":
				myGender = "Άρρεν"
			elif stat[0] == "f":
				myGender = "Θήλυ"
			else:
				myGender = "Άλλο"
			self.result_listbox.insert(tk.END, "| {:^8} | {:^10} |".format(stat[1],myGender))

	def ui_pref_members(self):
		""" Κατανομή προτιμήσεων μελών ανα κατηγορία """
		periodApo = self.entry_apo.get()
		periodDissect = periodApo.strip().split("-")
		if (len(periodDissect) != 3) or (int(periodDissect[0]) > 2024 ) or (int(periodDissect[0]) < 2023) or (int(periodDissect[1]) < 1) or (int(periodDissect[1]) > 12) or (int(periodDissect[2]) < 1) or (int(periodDissect[2]) > 31):
			logging.error("Wrong Apo date")
			self.wrongDatePopup()
			return False

		periodEos = self.entry_eos.get()
		periodDissect = periodEos.strip().split("-")
		if (len(periodDissect) != 3) or (int(periodDissect[0]) > 2024 ) or (int(periodDissect[0]) < 2023) or (int(periodDissect[1]) < 1) or (int(periodDissect[1]) > 12) or (int(periodDissect[2]) < 1) or (int(periodDissect[2]) > 31):
			logging.error("Wrong Eos date")
			self.wrongDatePopup()
			return False

		myStats = self.db.stats_pref_members(periodApo, periodEos)
		self.bookShownData = myStats
		self.result_listbox.delete(0, tk.END)
		self.result_listbox.insert(tk.END, "| {:^11} | {:^30} |".format("Αρ. Βιβλίων","Κατηγορία βιβλίων"))
		print(myStats)
		for stat in myStats:
			self.result_listbox.insert(tk.END, "| {:^11} | {:<30} |".format(stat[1],stat[0]))

	def ui_stats_books_member(self):
		""" Πλήθος βιβλίων ανα μέλος σε χρονική περίοδο """
		periodApo = self.entry_apo.get()
		periodDissect = periodApo.strip().split("-")
		if (len(periodDissect) != 3) or (int(periodDissect[0]) > 2024 ) or (int(periodDissect[0]) < 2023) or (int(periodDissect[1]) < 1) or (int(periodDissect[1]) > 12) or (int(periodDissect[2]) < 1) or (int(periodDissect[2]) > 31):
			logging.error("Wrong Apo date")
			self.wrongDatePopup()
			return False

		periodEos = self.entry_eos.get()
		periodDissect = periodEos.strip().split("-")
		if (len(periodDissect) != 3) or (int(periodDissect[0]) > 2024 ) or (int(periodDissect[0]) < 2023) or (int(periodDissect[1]) < 1) or (int(periodDissect[1]) > 12) or (int(periodDissect[2]) < 1) or (int(periodDissect[2]) > 31):
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


	def deleteFields(self):
		self.entry_field1.delete(0, tk.END)
		self.entry_field2.delete(0, tk.END)
		self.entry_field4.delete(0, tk.END)

	def on_double_click(self, event):
		selection = self.result_listbox.curselection()
		if selection:
			index = selection[0]
			book_list = list(self.bookShownData)  # Convert the set to a list
			value = book_list[index]
			self.deleteFields()
			self.entry_field1.insert(0, value[1])
			self.entry_field2.insert(0, value[3])
			#self.defaultCategory.set(self.categoryOptions[value[2]])
			self.entry_field4.insert(0, value[4])
			self.bookID = value[0]
			self.bookIDLabel.configure(text=f"{value[0]}")

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
