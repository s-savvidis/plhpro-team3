import tkinter as tk

from .HomePage import HomePage

class StatisticsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		label = tk.Label(self, text="Χρήστες", font=("Helvetica", 16))
		label.pack(padx=10, pady=10)
		start_page = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		start_page.pack()