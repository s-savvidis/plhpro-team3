import tkinter as tk
import os


class StatsMainPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		header = tk.Label(self, text="Διαχείριση Δανειστικής Βιβλιοθήκης", font=("Helvetica", 24))
		header.grid(row=0, column=0,padx=(150 ,20), columnspan=3, sticky="nsew", pady=(20, 50))

		script_dir = os.path.dirname(os.path.abspath(__file__))
		images_dir = os.path.join(script_dir, "../images/")

		from .BooksPage import BooksPage
		from .UsersPage import UsersPage
		from .BorrowingsPage import BorrowingsPage
		from .StatisticsPage import StatisticsPage
	
        # Κουμπί σελίδας βιβλίων
		books_image_path = os.path.join(images_dir, "books.png")
		rawBooksImage = tk.PhotoImage(file=books_image_path)
		resizedBooksImage = rawBooksImage.subsample(2, 2)  
		booksButton = tk.Button(self, image=resizedBooksImage, command=lambda: controller.show_frame(BooksPage))
		booksButton.image = resizedBooksImage  
		booksButton.grid(row=1, column=0, padx=(150, 50))

		booksLabel = tk.Label(self, text="Διαχείριση βιβλίων", font=("Helvetica", 16))
		booksLabel.grid(row=2, column=0,padx=(150,50), sticky="nsew", pady=(5, 20))
