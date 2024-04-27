import tkinter as tk

from HomePage import HomePage
from BooksPage import Books
from UsersPage import Users

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

app = MainWindow()
app.mainloop()

       