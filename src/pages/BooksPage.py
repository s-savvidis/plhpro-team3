import tkinter as tk

class Books(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		from HomePage import HomePage

		tk.Label(self, text="Τίτλος:").grid(row=0, column=0, sticky="e")
		self.entry_field1 = tk.Entry(self)
		self.entry_field1.grid(row=0, column=1)
		tk.Label(self, text="Συγγραφέας:").grid(row=1, column=0, sticky="e")
		self.entry_field2 = tk.Entry(self)
		self.entry_field2.grid(row=1, column=1)
		tk.Label(self, text="Κατηγορία:").grid(row=2, column=0, sticky="e")
		self.entry_field3 = tk.Entry(self)
		self.entry_field3.grid(row=2, column=1)
		tk.Label(self, text="ISBN:").grid(row=3, column=0, sticky="e")
		self.entry_field4 = tk.Entry(self)
		self.entry_field4.grid(row=3, column=1)
		submit_button = tk.Button(self, text="Αναζήτηση", command=self.open_popup)
		submit_button.grid(row=4, column=1, pady=10)
		home_button = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=4, column=2, pady=10)






		# field1_value = self.entry_field1.get()
		# field2_value = self.entry_field2.get()
		# field3_value = self.entry_field3.get()
		# field4_value = self.entry_field4.get()
		# print("Field 1:", field1_value)
		# print("Field 2:", field2_value)
		# print("Field 3:", field3_value)
		# print("Field 4:", field4_value)
  
	def open_popup(self):
		popup = tk.Toplevel(self)
		popup.title("Αναζήτηση")

		tk.Label(popup, text="Τίτλος:").grid(row=0, column=0, padx=5, pady=5)
		name_entry = tk.Entry(popup)
		name_entry.grid(row=0, column=1, padx=5, pady=5)
		
		tk.Label(popup, text="Συγγραφέας:").grid(row=1, column=0, padx=5, pady=5)
		email_entry = tk.Entry(popup)
		email_entry.grid(row=1, column=1, padx=5, pady=5)
		
		tk.Label(popup, text="Κατηγορία:").grid(row=2, column=0, padx=5, pady=5)
		age_entry = tk.Entry(popup)
		age_entry.grid(row=2, column=1, padx=5, pady=5)

		tk.Label(popup, text="ISBN:").grid(row=3, column=0, padx=5, pady=5)
		age_entry = tk.Entry(popup)
		age_entry.grid(row=3, column=1, padx=5, pady=5)

		submit_button = tk.Button(popup, text="Επιλογή", command=popup.destroy)
		submit_button.grid(row=4, columnspan=2, padx=5, pady=5)

		def submit_form(self):
			open_popup_button = tk.Button(self, text="Open Popup", command=self.open_popup)
			open_popup_button.pack(padx=10, pady=10)