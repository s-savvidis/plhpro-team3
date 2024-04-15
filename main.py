import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ηλεκτρονική δανειστική βιβλιοθήκη")
        self.geometry("1000x800")

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Widgets
        # Widgets for the main page
        self.homepage_label = tk.Label(self.main_frame, text="Αρχική σελίδα", font=("Helvetica", 16))
        self.homepage_label.pack(pady=20)

        # Books button
        self.books_canvas = tk.Canvas(self.main_frame, width=400, height=400, bg="white")
        self.books_canvas.pack(side="left", padx=50)
        self.books_rectangle = self.books_canvas.create_rectangle(0, 0, 400, 400, fill="#D7D0C2")
        self.books_text = self.books_canvas.create_text(200, 200, text="Βιβλία", fill="black", font=("Helvetica", 40))
        self.books_canvas.tag_bind(self.books_rectangle, "<Button-1>", self.onClickBooks)

        # Users button
        self.users_canvas = tk.Canvas(self.main_frame, width=400, height=400, bg="white")
        self.users_canvas.pack(side="right", padx=50)
        self.users_rectangle = self.users_canvas.create_rectangle(0, 0, 400, 400, fill="#D7D0C2")
        self.users_text = self.users_canvas.create_text(200, 200, text="Χρήστες", fill="black", font=("Helvetica", 40))
        self.users_canvas.tag_bind(self.users_rectangle, "<Button-1>", self.onClickUsers)

    def onClickBooks(self, event):
        print("Βιβλία")

    def onClickUsers(self, event):
        print("Χρήστες")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
