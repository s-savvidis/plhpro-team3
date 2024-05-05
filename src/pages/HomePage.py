import tkinter as tk
import os


class HomePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Αρχική σελίδα", font=("Helvetica", 16))
		label.pack(padx=20, pady=20)
		script_dir = os.path.dirname(os.path.abspath(__file__))
		images_dir = os.path.join(script_dir, "../images/")

		from .BooksPage import BooksPage
		from .UsersPage import UsersPage
		
		

		
        # Books Button
		books_image_path = os.path.join(images_dir, "books.png")
		rawBooksImage = tk.PhotoImage(file=books_image_path)
		resizedBooksImage = rawBooksImage.subsample(2, 2)  
		booksButton = tk.Button(self, image=resizedBooksImage, command=lambda: controller.show_frame(BooksPage))
		booksButton.image = resizedBooksImage  
		booksButton.pack(side="left", padx=100)
		
        # Users Button
		users_image_path = os.path.join(images_dir, "users.png")
		raw_users_image = tk.PhotoImage(file=users_image_path)
		resizedUsersImage = raw_users_image.subsample(4, 4)  
		usersButton = tk.Button(self, image=resizedUsersImage, command=lambda: controller.show_frame(UsersPage))
		usersButton.image = resizedUsersImage  
		usersButton.pack(side="right", padx=100)
