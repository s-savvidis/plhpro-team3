import tkinter as tk
from src.database.db import Database as dtb
from src.functions.membersPageFunctions.membersPageFunctions import *

def updateMemberPopup(self, memberDetails):
		popup = tk.Toplevel()
		popup.title("Ενημέρωση μέλους")

		genderOptions = [
		"f",
		"m",
		"o",
		] 

		defaultGender = tk.StringVar()
		defaultGender.set(genderOptions[0]) # default value
  
		XYPoints = centerizePopup(self, popup)
		popup.geometry(f"+{XYPoints["x"]}+{XYPoints["y"]}")
  
		tk.Label(popup, text="Όνοματεπώνυμο:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=10)  
		entry_field1 = tk.Entry(popup)
		entry_field1.grid(row=0, column=1, sticky="ew", pady=(10,0), padx=10)
  
		tk.Label(popup, text="Ηλικία:").grid(row=1, column=0, sticky="w", padx=10)
		age=tk.IntVar(value=memberDetails["age"])
		entry_field2 = tk.Spinbox(popup, from_= 1, to = 99, width=4, increment=1,
    	textvariable=age)
		entry_field2.grid(row=1, column=1, sticky="ew", padx=10)  

		tk.Label(popup, text="Επάγγελμα:").grid(row=2, column=0, sticky="w", padx=10)
		entry_field3 = tk.Entry(popup)
		entry_field3.grid(row=2, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Τηλέφωνο:").grid(row=3, column=0, sticky="w", padx=10)
		entry_field4 = tk.Entry(popup)
		entry_field4.grid(row=3, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="email:").grid(row=4, column=0, sticky="w", padx=10)
		entry_field5 = tk.Entry(popup)
		entry_field5.grid(row=4, column=1, sticky="ew", padx=10)

		tk.Label(popup, text="Φύλο:").grid(row=5, column=0, sticky="w", padx=10)
		entry_field6 = tk.OptionMenu(popup, defaultGender, *genderOptions)
		entry_field6.grid(row=5, column=1, sticky="ew", padx=10)



		insert_button = tk.Button(popup, text="Ενημέρωση", command= lambda: updateMember(entry_field1.get(), entry_field2.get(), entry_field3.get(), entry_field4.get(), entry_field5.get(), entry_field6.get()))
		insert_button.grid(row=6, column=0, pady=10, padx=10,sticky="w")
		
		close_button = tk.Button(popup, text="Κλείσιμο", command=popup.destroy)
		close_button.grid(row=6, column=1, pady=10, sticky="w")

		def updateMember():
			memberDetails = {
			'name': entry_field1.get(),
			'age': entry_field2(),
			'occupation': entry_field3.get(),
			'tel': entry_field4.get(),
			'email': entry_field5.get(),
			'gender': defaultGender.get()
			}
			dtb.update_member(self.db, memberDetails)
			showMembers(self, self.db, "")
			self.memberIDLabel.configure(text=f"-")
			popup.destroy()