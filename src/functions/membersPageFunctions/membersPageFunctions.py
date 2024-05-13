import tkinter as tk
from src.database.db import Database as dtb

def deleteFields(self):
    self.entry_field1.delete(0, tk.END)
    self.entry_field2.delete(0, tk.END) 
    self.entry_field3.delete(0, tk.END) 
    self.entry_field4.delete(0, tk.END)

def switchButtonState(self, value):
    if (value == 0):
        self.save_button['state'] = tk.DISABLED
        self.delete_button['state'] = tk.DISABLED
    elif (value == 1):
        self.save_button['state'] = tk.NORMAL
        self.delete_button['state'] = tk.NORMAL

def showMembers(self, db, memberName):
    deleteFields(self)
    members = dtb.search_name(db, memberName)
    self.memberShownData = members
    self.result_listbox.delete(0, tk.END) 
    
    for member in members:
        self.result_listbox.insert(tk.END, f"  {member[1]} - Ηλικία: {member[2]} - {member[3]} - {member[4]} - {member[5]} - Φύλο: {member[6]}") 
    switchButtonState(self, 0)

def deleteMember(self, db, memberId):
    dtb.delete_member(db, memberId)

def on_double_click(self, event):
    selection = self.result_listbox.curselection()
    if selection:
        index = selection[0]
        value = self.memberShownData[index]
        deleteFields(self)
        self.entry_field1.insert(0, value[1])
        self.entry_field2.insert(0, value[2])
        self.entry_field3.insert(0, value[3])
        self.entry_field4.insert(0, value[4])
        self.entry_field5.insert(0, value[5])
        self.memberID = value[0]
        self.memberIDLabel.configure(text=f"{value[0]}")
        switchButtonState(self, 1)

        self.selectedMember = {
            'name': value[1],
            'age': value[2],
            'occupation': value[3],
            'tel': value[4],
            'email': value[5],
            'gender': value[6],
            'member_id': value[0]
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


        

