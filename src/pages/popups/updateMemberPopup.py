import tkinter as tk
from src.database.db import Database as dtb
from src.functions.membersPageFunctions.membersPageFunctions import *

def updateMemberPopup(self, memberDetails):
		popup = tk.Toplevel()
		popup.title("Ενημέρωση μέλους")

		XYPoints = centerizePopup(self, popup)
		popup.geometry(f"+{XYPoints["x"]}+{XYPoints["y"]}")

		tk.Label(popup, text="Φύλο:").grid(row=0, column=0, sticky="w", padx=10)
		gender=tk.IntVar(value=memberDetails["gender"])
		entry_field6 = tk.Spinbox(popup, from_= 1, to = 99, increment=1,
    	textvariable=gender)
		entry_field6.grid(row=0, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Ηλικία:").grid(row=1, column=0, sticky="w", padx=10)
		age=tk.IntVar(value=memberDetails["age"])
		entry_field2 = tk.Spinbox(popup, from_= 1, to = 99, width=4, increment=1,
    	textvariable=age)
		entry_field2.grid(row=1, column=1, sticky="ew", padx=10)

		insert_button = tk.Button(popup, text="Ενημέρωση", command= lambda: updateMember(entry_field2.get(), entry_field6.get()))
		insert_button.grid(row=2, column=0, pady=10, padx=10,sticky="w")
		
		close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
		close_button.grid(row=2, column=1, pady=10, sticky="w")

		def updateMember(age, gender):
			memberDetails = {
				'name': self.entry_field1.get(),
                'age': age,
                'occupation': self.entry_field2.get(),
                'tel': self.entry_field3.get(),
                'email': self.entry_field4.get(),
                'gender': gender,
				'member_id': self.selectedMember["member_id"]
			}
			dtb.update_member(self.db, memberDetails)
			showMembers(self, self.db, "")
			self.memberIDLabel.configure(text=f"-")
			popup.destroy()