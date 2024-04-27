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
		submit_button = tk.Button(self, text="Αναζήτηση", command=self.submit_form)
		submit_button.grid(row=4, column=1, pady=10)
		home_button = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		home_button.grid(row=4, column=2, pady=10)


	def submit_form(self):
		field1_value = self.entry_field1.get()
		field2_value = self.entry_field2.get()
		field3_value = self.entry_field3.get()
		field4_value = self.entry_field4.get()
		print("Field 1:", field1_value)
		print("Field 2:", field2_value)
		print("Field 3:", field3_value)
		print("Field 4:", field4_value)