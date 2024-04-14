import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ηλεκτρονική δανειστική βιβλιοθήκη")
        self.geometry("1000x800")

        # Sidebar
        self.sidebar_frame = tk.Frame(self, width=200)
        self.sidebar_frame.pack(side="left", fill="both")
        self.sidebar_frame.pack_propagate(0)  # Prevent frame from resizing

        self.sidebar_border_frame = tk.Frame(self.sidebar_frame, width=2, bg="black")
        self.sidebar_border_frame.pack(side="right", fill="y")

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Widgets
        # Widgets for the sidebar
        self.sidebar_label = tk.Label(self.sidebar_frame, text="Εργαλεία", font=("Helvetica", 16))
        self.sidebar_label.pack(pady=20)

        self.sidebar_button = tk.Button(self.sidebar_frame, text="Button1", command=self.button_clicked)
        self.sidebar_button.pack(padx=10, pady=10, anchor="w")
        self.sidebar_button = tk.Button(self.sidebar_frame, text="Button2", command=self.button_clicked)
        self.sidebar_button.pack(padx=10, pady=10, anchor="w")

        # Widgets for the main page
        self.homepage_label = tk.Label(self.main_frame, text="Αρχική σελίδα", font=("Helvetica", 16))
        self.homepage_label.pack(pady=20)

    # Functions
    def button_clicked(self):
        print("Clicked")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
