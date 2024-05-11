import tkinter as tk

def deleteBookPopup(self):
		popup = tk.Toplevel()

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

		# Set the position of the popup window
		popup.geometry(f"+{x}+{y}")	

		tk.Label(popup, text="Επιθυμείτε να διαγράψετε την επιλεγμένη καταχώρηση βιβλίου;").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

		insert_button = tk.Button(popup, text="Ναι, διαγραφή", command= lambda: deleteAndClose())
		insert_button.grid(row=1, column=0, pady=10, padx=20,sticky="w")
		
		close_button = tk.Button(popup, text="Ακύρωση", command=popup.destroy)
		close_button.grid(row=1, column=1, pady=10, padx=20, sticky="e")

		def deleteAndClose():
			self.deleteBook(self.db, self.selectedBook["book_id"])
			self.showBooks(self.db, "")
			self.bookIDLabel.configure(text=f"-")
			popup.destroy()
