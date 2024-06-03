import logging
import tkinter as tk
from src.database.library_member_manage import library_members as dtb
from .HomePage import HomePage

class UsersPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.memberShownData = []
		self.selectedMember = {
				'name',
                'age',
                'occupation',
                'tel',
                'email',
                'gender',
				'member_id'
		}

		tk.Label(self, text="Ονοματεπώνυμο:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		self.entry_field1 = tk.Entry(self, width=60)
		self.entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=(0,200))

		tk.Label(self, text="Ηλικία:").grid(row=1, column=0, sticky="w", padx=10)
		self.entry_field2 = tk.Entry(self, width=60)
		self.entry_field2.grid(row=1, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="Επάγγελμα:").grid(row=2, column=0, sticky="w", padx=10)
		self.entry_field3 = tk.Entry(self, width=60)
		self.entry_field3.grid(row=2, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text="Τηλέφωνο:").grid(row=3, column=0, sticky="w", padx=10)
		self.entry_field4 = tk.Entry(self, width=60)
		self.entry_field4.grid(row=3, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text=f"email:").grid(row=4, column=0, sticky="w", padx=10)
		self.entry_field5 = tk.Entry(self, width=60)
		self.entry_field5.grid(row=4, column=1, sticky="ew", padx=(0,200))

		tk.Label(self, text=f"Member ID:").grid(row=5, column=0, sticky="w", padx=10)
		self.memberIDLabel = tk.Label(self, text=f"-")
		self.memberIDLabel.grid(row=5, column=1, sticky="w", padx=(0,200))
  

		search_button = tk.Button(self, text="Αναζήτηση", width=10, command=lambda: self.showMembers(self.entry_field1.get()))
		search_button.grid(row=6, column=0, pady=10, padx=10,sticky="w")

		self.add_button = tk.Button(self, text="Nέο μέλος", width=10, command=lambda: self.newMemberPopup())
		self.add_button.grid(row=0, column=2, pady=(10,0), padx=10, sticky="ew")
		
		self.save_button = tk.Button(self, text="Ενημέρωση", state="disabled", width=10, command=lambda:self.updateMemberPopup(self.selectedMember))
		self.save_button.grid(row=1, column=2, padx=10, sticky="w")

		self.delete_button = tk.Button(self, text="Διαγραφή", state="disabled", width=10, command=lambda:self.deleteMemberPopup())
		self.delete_button.grid(row=2, column=2, padx=10, sticky="w")

		self.recommend_button = tk.Button(self, text="Προτάσεις", state="disabled", width=10, command=lambda: self.recommendationsPopup(self.selectedMember))
		self.recommend_button.grid(row=3, column=2, padx=10, sticky="w")
  
		self.preferences_button = tk.Button(self, text="Προτιμήσεις", state="disabled", width=10, command=lambda: self.preferencesPopup(self.selectedMember))
		self.preferences_button.grid(row=4, column=2, padx=10, sticky="w")		

		home_button = tk.Button(self, text="Αρχική σελίδα", width=10, command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="w")

		listbox_frame = tk.Frame(self)
		listbox_frame.grid(row=7, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

		self.result_listbox = tk.Listbox(listbox_frame)
		self.result_listbox.grid(row=0, column=0, sticky="nsew")

		scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.result_listbox.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.result_listbox.config(yscrollcommand=scrollbar.set)

		self.db = dtb("src/database/members_sqlite.db")

		self.result_listbox.bind("<Double-Button-1>", lambda event: self.on_double_click(event))

		self.rowconfigure(7, weight=1)
		self.columnconfigure(0, weight=1)
		listbox_frame.rowconfigure(0, weight=1)
		listbox_frame.columnconfigure(0, weight=1)

	### Members Functions
	def deleteFields(self):
		self.entry_field1.delete(0, tk.END)
		self.entry_field2.delete(0, tk.END)
		self.entry_field3.delete(0, tk.END)
		self.entry_field4.delete(0, tk.END)
		self.entry_field5.delete(0, tk.END)

	def switchButtonState(self, value):
		if (value == 0):
			self.save_button['state'] = tk.DISABLED
			self.delete_button['state'] = tk.DISABLED
			self.recommend_button['state'] = tk.DISABLED
			self.preferences_button['state'] = tk.DISABLED
		elif (value == 1):
			self.save_button['state'] = tk.NORMAL
			self.delete_button['state'] = tk.NORMAL
			self.recommend_button['state'] = tk.NORMAL
			self.preferences_button['state'] = tk.NORMAL

	def showMembers(self, memberName):
		self.deleteFields()
		members = self.db.search_name(memberName)
		self.memberShownData = members
		self.result_listbox.delete(0, tk.END) 

		for member in members:
			if member[6] == 'm':
				gen = 'άνδρας'
			elif member[6] == 'f':
				gen = 'γυναίκα'
			else:
				gen = 'άλλο'
			self.result_listbox.insert(tk.END, f"  {member[1]} - Ηλικία: {member[2]} - {member[3]} - {member[4]} - {member[5]} - {gen}") 
		self.switchButtonState(0)

	def initialShowBooks(self):
		self.deleteFields()
		books = self.db.search_title("")
		self.bookShownData = books
		self.result_listbox.delete(0, tk.END) 

		for book in books:
			self.result_listbox.insert(tk.END, f"  {book[1]} - {book[3]} - ISBN: {book[4]} | Total stock: {book[5]} Current stock: {book[6]}") 
		self.switchButtonState(0)

	def check_email(email):
		# Ελέγχουμε αν το email έχει την κατάλληλη μορφή
		if "@" in email and "." in email:
		    # Eλέγχουμε ότι το παπάκι "@" βρίσκεται πρίν από την τελευταία τελεία "."
			papaki = False
			teleia = False
			for i, y in enumerate(email):
				if y == "@":
					papaki = True
                	# Ελέγχουμε ότι το παπάκι "@" δεν είναι ο πρώτος χαρακτήρας 
					if i == 0:
						return False
				if y == "." and papaki:
					teleia = True
                	# ελέγχουμε ότι η τελεία "." δεν είναι ο τελευταίος χαρακτήρας
					if i == len(email) - 1:
						return False
			return papaki and teleia
		return False



	def deleteMember(self, memberId):
		""" Διαγραφή μέλους με χρήση member Id """
		self.db.delete_member(memberId)

	def on_double_click(self, event):
		selection = self.result_listbox.curselection()
		if selection:
			index = selection[0]
			member_list = list(self.memberShownData)  # Convert the set to a list
			value = member_list[index]
			self.deleteFields()
			self.entry_field1.insert(0, value[1])
			self.entry_field2.insert(0, value[3])
			self.entry_field3.insert(0, value[3])
			self.entry_field4.insert(0, value[4])
			self.entry_field5.insert(0, value[5])
			self.memberID = value[0]
			self.memberIDLabel.configure(text=f"{value[0]}")
			self.switchButtonState(1)

			self.selectedMember = {
            	'name': value[1],
            	'age': value[2],
            	'occupation': value[3],
            	'tel': value[4],
            	'email': value[5],
            	'gender': value[6],
            	'member_id': value[0]
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
	def newMemberPopup(self):
		popup = tk.Toplevel()
		popup.title("Εισαγωγή νέου μέλους")
	
		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		genderOptions = [
			"γυναίκα",
			"άνδρας",
			"άλλο",
		] 

		defaultGender = tk.StringVar()
		defaultGender.set(genderOptions[0]) # default value

		tk.Label(popup, text="Όνοματεπώνυμο:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		entry_field1 = tk.Entry(popup)
		entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=10)

		tk.Label(popup, text="Ηλικία:").grid(row=1, column=0, sticky="w", padx=10)
		age=tk.IntVar(value=0)
		entry_field2 = tk.Spinbox(popup, from_= 1, to = 99, width=4, increment=1,
		textvariable=age)
		entry_field2.grid(row=1, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Επάγγελμα:").grid(row=2, column=0, sticky="w", padx=10)
		entry_field3 = tk.Entry(popup)
		entry_field3.grid(row=2, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Τηλέφωνο:").grid(row=3, column=0, sticky="w", padx=10)
		entry_field4 = tk.Entry(popup)
		entry_field4.grid(row=3, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="email:").grid(row=4, column=0, sticky="w", padx=10)
		entry_field5 = tk.Entry(popup)
		entry_field5.grid(row=4, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Φύλο:").grid(row=5, column=0, sticky="w", padx=10)
		entry_field6 = tk.OptionMenu(popup, defaultGender, *genderOptions)
		entry_field6.grid(row=5, column=1, sticky="ew", padx=10)

		insert_button = tk.Button(popup, text="Εισαγωγή", command= lambda: addMember())
		insert_button.grid(row=6, column=0, pady=10, padx=10,sticky="w")
	
		close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
		close_button.grid(row=6, column=1, pady=10, sticky="w")

		def addMember():
		
			email = entry_field5.get()
			
			if defaultGender.get() == 'γυναίκα':
				gen = 'f'
			elif defaultGender.get() == 'άνδρας':
				gen = 'm'
			else:
				gen = 'o'

			memberDetails = {
				'full_name': entry_field1.get(),
				'age': entry_field2.get(),
				'occupation': entry_field3.get(),
				'telephone_number': entry_field4.get(),
				'email': email,
				'gender': gen
			}
  
			if not self.check_email(email):
				error_label = tk.Label(popup, text="Το email που εισάγατε δεν έχει σωστή μορφή", fg="red")
				error_label.place(x=10, y=-6)
			    
			elif (
			entry_field1.get()
			and age.get()
			and entry_field3.get()
			and entry_field4.get()
  			and email
			and defaultGender.get()
			):
				self.db.insert_member(memberDetails)
				self.showMembers("")
				self.memberIDLabel.configure(text=f"-")
				popup.destroy()
			else:
				error_label = tk.Label(popup, text="Πρέπει να συμπληρώσετε όλα τα πεδία          ", fg="red")
				error_label.place(x=10, y=-6)

	def deleteMemberPopup(self):
		popup = tk.Toplevel()

		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		tk.Label(popup, text="Επιθυμείτε να διαγράψετε την επιλεγμένη καταχώρηση μέλους;").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

		insert_button = tk.Button(popup, text="Ναι, διαγραφή", command= lambda: deleteAndClose())
		insert_button.grid(row=1, column=0, pady=10, padx=20,sticky="w")
		
		close_button = tk.Button(popup, text="Ακύρωση", command=popup.destroy)
		close_button.grid(row=1, column=1, pady=10, padx=20, sticky="e")

		def deleteAndClose():
			self.deleteMember(self.selectedMember["member_id"])
			self.showMembers("")
			self.memberIDLabel.configure(text=f"-")
			popup.destroy()

	def updateMemberPopup(self, memberDetails):
		popup = tk.Toplevel()
		popup.title("Ενημέρωση μέλους")

		genderOptions = [
		"γυναίκα",
		"άνδρας",
		"άλλο",
		] 

		if memberDetails["gender"] == 'f':
			gen = 'γυναίκα'
		elif memberDetails["gender"] == 'm':
			gen = 'άνδρας'
		else:
			gen = 'άλλο'
		defaultGender = tk.StringVar(value=gen)
  
		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")
  
		tk.Label(popup, text="Όνοματεπώνυμο:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		entry_field1 = tk.Entry(popup, textvariable=tk.StringVar(value=memberDetails['name']))
		entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=10)
  
		tk.Label(popup, text="Ηλικία:").grid(row=1, column=0, sticky="w", padx=10)
		age=tk.IntVar(value=memberDetails["age"])
		entry_field2 = tk.Spinbox(popup, from_= 1, to = 99, width=4, increment=1,
    	textvariable=age)
		entry_field2.grid(row=1, column=1, sticky="ew", padx=10)  

		tk.Label(popup, text="Επάγγελμα:").grid(row=2, column=0, sticky="w", padx=10)
		entry_field3 = tk.Entry(popup, textvariable=tk.StringVar(value=memberDetails['occupation']))
		entry_field3.grid(row=2, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Τηλέφωνο:").grid(row=3, column=0, sticky="w", padx=10)
		entry_field4 = tk.Entry(popup, textvariable=tk.StringVar(value=memberDetails['tel']))
		entry_field4.grid(row=3, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="email:").grid(row=4, column=0, sticky="w", padx=10)
		entry_field5 = tk.Entry(popup, textvariable=tk.StringVar(value=memberDetails['email']))
		entry_field5.grid(row=4, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Φύλο:").grid(row=5, column=0, sticky="w", padx=10)
		entry_field6 = tk.OptionMenu(popup, defaultGender, *genderOptions)
		entry_field6.grid(row=5, column=1, sticky="ew", padx=10)

		insert_button = tk.Button(popup, text="Ενημέρωση", command=lambda: updateMember())
		insert_button.grid(row=6, column=0, pady=10, padx=10,sticky="w")
		
		close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
		close_button.grid(row=6, column=1, pady=10, sticky="w")
  


		def updateMember():
      
			email = entry_field5.get()
			
			if defaultGender.get() == 'γυναίκα':
				gen = 'f'
			elif defaultGender.get() == 'άνδρας':
				gen = 'm'
			else:
				gen = 'o'
   
			memberDetails = {
			'full_name': entry_field1.get(),
			'age': age.get(),
			'occupation': entry_field3.get(),
			'telephone_number': entry_field4.get(),
			'email': email,
			'gender': gen,
			'member_id': self.selectedMember["member_id"]
			}
			
			if not self.check_email(email):
				error_label = tk.Label(popup, text="Το email που εισάγατε δεν έχει σωστή μορφή", fg="red")
				error_label.place(x=10, y=-6)
			    
			elif (
			entry_field1.get()
			and age.get()
			and entry_field3.get()
			and entry_field4.get()
  			and email
			and defaultGender.get()
			): 
				self.db.update_member(memberDetails)
				self.showMembers("")
				self.memberIDLabel.configure(text=f"-")
				popup.destroy()
    
			else:
				error_label = tk.Label(popup, text="Πρέπει να συμπληρώσετε όλα τα πεδία          ", fg="red")
				error_label.place(x=10, y=-6)

	def recommendationsPopup(self, selectedMember):
		popup = tk.Toplevel()
  
		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		member_id = selectedMember.get("member_id", None)

		if member_id is not None:
			tk.Label(popup, text="Προτάσεις δανεισμών για το επιλεγμένο μέλος:").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

			recommendations_listbox = tk.Listbox(popup)
			recommendations_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

			def showRecommendations():
				db = dtb("src/database/members_sqlite.db")
				recommendations = self.db.recommendations(member_id)
				for book_id, title in recommendations:
					recommendations_listbox.insert(tk.END, f"{title}, ID: {book_id}")
        
			showRecommendations()
		else:
			tk.Label(popup, text="Δεν βρέθηκε το ID μέλους.").grid(row=0, column=0, columnspan=2, pady=10, padx=10)
    
		close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
		close_button.grid(row=2, column=1, pady=10, sticky="e")
		popup.rowconfigure(1, weight=1)
		popup.columnconfigure(0, weight=1)
   
	def preferencesPopup(self, selectedMember):
		popup = tk.Toplevel()

		XYPoints = self.centerizePopup(popup)
		popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

		member_id = selectedMember.get("member_id", None)
		pass