import tkinter as tk
from src.database.db import Database as dtb

def deleteFields(self):
    self.entry_field1.delete(0, tk.END)
    self.entry_field2.delete(0, tk.END) 
    self.entry_field3.delete(0, tk.END) 
    self.entry_field4.delete(0, tk.END)

def switchButtonState(self, value):
    if value == 0:
        self.save_button['state'] = tk.DISABLED
        self.delete_button['state'] = tk.DISABLED
    elif value == 1:
        self.save_button['state'] = tk.NORMAL
        self.delete_button['state'] = tk.NORMAL


def showBorrowings(self, db, memberID):
    deleteFields(self)
    borrowings = dtb.search_borrowing(db, memberID)
    self.borrowingShownData = borrowings
    self.result_listbox.delete(0, tk.END)
    
    for borrowing in borrowings:
        self.result_listbox.insert(tk.END, f" member_id: {borrowing[2]} - book_id: {borrowing[1]} - {borrowing[3]} - return_status: {borrowing[4]} rating: {borrowing[5]}")
    
    switchButtonState(self, 0)
    
    
def deleteBorrowing(self, db, borrowingId):
    dtb.delete_borrowing(db, borrowingId)

def on_double_click(self, event):
    selection = self.result_listbox.curselection()
    if selection:
        index = selection[0]
        value = self.borrowingShownData[index]
        deleteFields(self)
        self.entry_field1.insert(0, value[2])
        self.entry_field2.insert(0, value[1])
        self.entry_field3.insert(0, value[3])
        self.entry_field4.insert(0, value[5])
        self.borrowingID = value[0]
        self.borrowingIDLabel.configure(text=f"{value[0]}")
        switchButtonState(self, 1)

        self.selectedBorrowing = {
            'member_id': value[2],
            'book_id': value[1],
            'date': value[3],
            'rating': value[5],
            'borrow_id': value[0]
        }

def centerizePopup(self, popup):	
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
    return {"x":x,"y":y}