from tkinter import Frame, Button, ACTIVE, LEFT, Checkbutton, BooleanVar
from typing import Dict

from dialog import Dialog


class ChooseDetailsDialog(Dialog):
    def __init__(self, parent, details_filter: Dict[str, bool]):
        self.birthday_var: BooleanVar = BooleanVar(value=details_filter["birthday"])
        self.email_var: BooleanVar = BooleanVar(value=details_filter["email"])
        self.phone_number_var: BooleanVar = BooleanVar(value=details_filter["phone_number"])
        self.note_var: BooleanVar = BooleanVar(value=details_filter["note"])

        super().__init__(parent, title="Filtr zobrazování údajů")

    def body(self, master: Frame):
        birthday_checkbox = Checkbutton(master, text="Narozeniny", variable=self.birthday_var, font=self.font)
        email_checkbox = Checkbutton(master, text="Email", variable=self.email_var, font=self.font)
        phone_number_checkbox = Checkbutton(master, text="Telefon", variable=self.phone_number_var, font=self.font)
        note_checkbox = Checkbutton(master, text="Poznámka", variable=self.note_var, font=self.font)

        birthday_checkbox.grid(column=0, row=0, padx=20, sticky="w")
        email_checkbox.grid(column=0, row=1, padx=20, sticky="w")
        phone_number_checkbox.grid(column=0, row=2, padx=20, sticky="w")
        note_checkbox.grid(column=0, row=3, padx=20, sticky="w")

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack(side="bottom")
