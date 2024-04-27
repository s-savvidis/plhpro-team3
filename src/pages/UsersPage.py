import tkinter as tk

class Users(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		from HomePage import HomePage
		from BooksPage import Books
		label = tk.Label(self, text="Χρήστες", font=("Helvetica", 16))
		label.pack(padx=10, pady=10)
		start_page = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		start_page.pack()
		page_one = tk.Button(self, text="Βιβλία", command=lambda:controller.show_frame(Books))
		page_one.pack()