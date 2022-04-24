from tkinter import Frame, Button, LEFT, ACTIVE, ttk, StringVar, Listbox, Label
from typing import List

from dialog import Dialog


class BirthdayReminderDialog(Dialog):
    def __init__(self, parent, name_list: List[str]):
        self.name_list: List[str] = name_list
        super().__init__(parent, title="Dnešní narozeniny")

    def body(self, master: Frame):
        lbl = Label(master, text="Dnes má narozeniny:", font=self.font)
        lbl.grid(column=0, row=0, sticky='w', columnspan=2)

        people_var = StringVar(value=self.name_list)
        listbox = Listbox(master, listvariable=people_var, font=self.font)

        listbox.grid(column=0, row=1, sticky='nwes', padx=20)

        # link a scrollbar to a listbox
        scrollbar = ttk.Scrollbar(master, orient='vertical', command=listbox.yview)
        listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=1, sticky='ns')

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack(side="bottom")
