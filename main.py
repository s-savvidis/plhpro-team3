import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Ηλεκτρονική δανειστική βιβλιοθήκη")
        self.geometry("1000x800")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, Books, Users):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
    
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

class HomePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Αρχική σελίδα", font=("Helvetica", 16))
		label.pack(padx=20, pady=20)
		
        # Books Button
		rawBooksImage = tk.PhotoImage(file="./images/books.png")
		resizedBooksImage = rawBooksImage.subsample(2, 2)  
		booksButton = tk.Button(self, image=resizedBooksImage, command=lambda: controller.show_frame(Books))
		booksButton.image = resizedBooksImage  
		booksButton.pack(side="left", padx=100)
		
        # Users Button
		rawUsersImage = tk.PhotoImage(file="./images/users.png")
		resizedUsersImage = rawUsersImage.subsample(4, 4)  
		usersButton = tk.Button(self, image=resizedUsersImage, command=lambda: controller.show_frame(Books))
		usersButton.image = resizedUsersImage  
		usersButton.pack(side="right", padx=100)

class Books(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Βιβλία", font=("Helvetica", 16))
		label.pack(padx=10, pady=10)
		start_page = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		start_page.pack()
		page_two = tk.Button(self, text="Χρήστες", command=lambda:controller.show_frame(Users))
		page_two.pack()

class Users(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Χρήστες", font=("Helvetica", 16))
		label.pack(padx=10, pady=10)
		start_page = tk.Button(self, text="Αρχική σελίδα", command=lambda:controller.show_frame(HomePage))
		start_page.pack()
		page_one = tk.Button(self, text="Βιβλία", command=lambda:controller.show_frame(Books))
		page_one.pack()

class MainMenu:
	def __init__(self, master):
		menubar = tk.Menu(master)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		master.config(menu=menubar)


app = MainWindow()
app.mainloop()

       