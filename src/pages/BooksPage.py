import tkinter as tk

class Books(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		from HomePage import HomePage
		from UsersPage import Users
		label = tk.Label(self, text="Βιβλία", font=("Helvetica", 16))
		label.pack(padx=10, pady=10)
		start_page = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		start_page.pack()
		page_two = tk.Button(self, text="Χρήστες", command=lambda:controller.show_frame(Users))
		page_two.pack()