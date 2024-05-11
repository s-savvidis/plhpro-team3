import tkinter as tk
import os


class HomePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		header = tk.Label(self, text="Διαχείρισης Δανειστικής Βιβλιοθήκης", font=("Helvetica", 24))
		header.grid(row=0, column=0,padx=20, columnspan=3, sticky="nsew", pady=(20, 50))

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
		
        # Κουμπί σελίδας χρηστών
		users_image_path = os.path.join(images_dir, "users.png")
		raw_users_image = tk.PhotoImage(file=users_image_path)
		resizedUsersImage = raw_users_image.subsample(4, 4)  
		usersButton = tk.Button(self, image=resizedUsersImage, command=lambda: controller.show_frame(UsersPage))
		usersButton.image = resizedUsersImage  
		usersButton.grid(row=1, column=1, padx=(50, 100))

		booksLabel = tk.Label(self, text="Διαχείριση χρηστών", font=("Helvetica", 16))
		booksLabel.grid(row=2, column=1,padx=(50, 100), sticky="nsew", pady=(5, 20))

        # Κουμπί σελίδας δανεισμών
		books_image_path = os.path.join(images_dir, "borrowings.png")
		rawBooksImage = tk.PhotoImage(file=books_image_path)
		resizedBooksImage = rawBooksImage.subsample(2, 2)  
		booksButton = tk.Button(self, image=resizedBooksImage, command=lambda: controller.show_frame(BorrowingsPage))
		booksButton.image = resizedBooksImage  
		booksButton.grid(row=3, column=0, padx=(150, 50))

		booksLabel = tk.Label(self, text="Διαχείριση δανεισμών", font=("Helvetica", 16))
		booksLabel.grid(row=4, column=0,padx=(150, 50), sticky="nsew", pady=(5, 20))
		
        # Κουμπί σελίδας στατιστικών
		users_image_path = os.path.join(images_dir, "statistics.png")
		raw_users_image = tk.PhotoImage(file=users_image_path)
		resizedUsersImage = raw_users_image.subsample(4, 4)  
		usersButton = tk.Button(self, image=resizedUsersImage, command=lambda: controller.show_frame(StatisticsPage))
		usersButton.image = resizedUsersImage  
		usersButton.grid(row=3, column=1, padx=(50, 100))

		booksLabel = tk.Label(self, text="Στατιστικά", font=("Helvetica", 16))
		booksLabel.grid(row=4, column=1,padx=(50, 100), sticky="nsew", pady=(5, 20))