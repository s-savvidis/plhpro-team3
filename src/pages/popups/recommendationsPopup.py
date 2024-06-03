import tkinter as tk
from src.database.db import Database as dtb
from src.functions.membersPageFunctions.membersPageFunctions import *

def recommendationsPopup(self, selectedMember):
    print("Self:", self)
    print("Selected Member:", selectedMember)
    
    popup = tk.Toplevel()

    XYPoints = centerizePopup(self, popup)
    popup.geometry(f"+{XYPoints['x']}+{XYPoints['y']}")

    member_id = selectedMember.get("member_id", None)
    print("Member ID:", member_id)  # Debugging print statement

    if member_id is not None:
        tk.Label(popup, text="Προτάσεις δανεισμών για το επιλεγμένο μέλος:").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        recommendations_listbox = tk.Listbox(popup)
        recommendations_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        def showRecommendations():
            db = dtb()
            recommendations = db.recommendations(member_id)
            for book_id, title in recommendations:
                recommendations_listbox.insert(tk.END, f"{title}, ID: {book_id}")
        
        showRecommendations()
    else:
        tk.Label(popup, text="Δεν βρέθηκε το ID μέλους.").grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
    close_button.grid(row=2, column=1, pady=10, sticky="e")

    popup.rowconfigure(1, weight=1)
    popup.columnconfigure(0, weight=1)

