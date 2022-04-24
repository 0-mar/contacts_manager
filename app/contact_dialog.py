import datetime
from tkinter import Frame, ACTIVE, LEFT, Button, font, StringVar, Label, Widget, Entry
from typing import Dict, List

from dialog import Dialog
from data_manager import DataManager

LABELS: Dict[str, str] = {"person_name": "Jméno:", "birthday": "Narozeniny:", "email": "Email:",
                          "phone_number": "Telefon:", "note": "Poznámka:"}


class ContactDialog(Dialog):
    """
    Dialog, which shows details about given person.
    """

    def __init__(self, parent, person_name: str, data_manager: DataManager, details_filter: Dict[str, bool]):
        self.person_name: str = person_name
        self.data_manager: DataManager = data_manager
        self.details_filter: Dict[str, bool] = details_filter

        self.person_data: Dict[str, str] = self.data_manager.get_person(self.person_name)

        self.widget_list: List[Widget] = []

        super().__init__(parent, title="Zobrazit kontakt")
        # self.option_add('*Font', 'serif 15')

    def body(self, master: Frame):
        i = 1

        name_font = font.Font(family="serif", size=19)
        name_frame = Frame(master, background="#77bbd1")
        name_label = Label(name_frame, text=self.person_name, font=name_font, background="#77bbd1")
        name_label.pack(side="left")
        name_frame.grid(column=0, row=0, columnspan=2, pady=(0, 10), sticky="news")

        for key, val in self.person_data.items():
            if i == 1:
                i += 1
                continue

            if self.details_filter[key]:
                desc_label = Label(master, text=LABELS[key], font=self.font)
                desc_label.grid(column=0, row=i, padx=(20, 0), sticky="w")

                val_label = Label(master, text=val, font=self.font)
                val_label.grid(column=1, row=i, padx=(30, 0), sticky="w")

                self.widget_list.append(desc_label)
                self.widget_list.append(val_label)
                i += 1

        return master

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack(side="bottom")


class AddContactDialog(Dialog):
    def __init__(self, parent, data_manager: DataManager, listbox_string_var: StringVar, title="Přidat kontakt"):
        self.entry_list: List[Entry] = []
        self.text_vars: List[StringVar] = []

        self.data_manager: DataManager = data_manager
        self.listbox_string_var: StringVar = listbox_string_var

        self.valid_name: bool = False
        self.valid_birthday: bool = True
        self.valid_email: bool = True
        self.valid_phone: bool = True

        super().__init__(parent, title=title)

    def body(self, master):
        i = 1

        master.columnconfigure(1, weight=1)

        frame = Frame(master, width=650, height=20, background="#77bbd1")
        frame.grid(column=0, row=0, columnspan=3, sticky="nswe")

        for val in LABELS.values():
            desc_label = Label(master, text=val, font=self.font)
            desc_label.grid(column=0, row=i, padx=(20, 0), pady=(10, 0), sticky="w")

            text_var = StringVar()
            entry = Entry(master, font=self.font, textvariable=text_var)
            if i == 5:
                entry = Entry(master, font=self.font, textvariable=text_var, width=45)
                entry.grid(column=1, row=i, padx=(30, 0), pady=(10, 0), sticky="w", columnspan=2)
            else:
                entry.grid(column=1, row=i, padx=(30, 0), pady=(10, 0), sticky="w")

            self.entry_list.append(entry)
            self.text_vars.append(text_var)

            i += 1

        check_label_font = font.Font(family="Helvetica", size=11, slant="italic")

        self.check_name_label_var: StringVar = StringVar(value="Povinný údaj")
        self.check_name_label: Label = Label(master, textvariable=self.check_name_label_var, font=check_label_font,
                                             fg="red")
        self.check_name_label.grid(column=2, row=1, padx=(30, 30), sticky="w")

        self.check_birthday_label_var: StringVar = StringVar(value="Datum je v nesprávném tvaru")
        self.check_birthday_label: Label = Label(master, textvariable=self.check_birthday_label_var,
                                                 font=check_label_font,
                                                 fg="red")

        self.check_email_label_var: StringVar = StringVar(value="Email je v nesprávném tvaru")
        self.check_email_label: Label = Label(master, textvariable=self.check_email_label_var, font=check_label_font,
                                              fg="red")

        self.check_phone_label_var: StringVar = StringVar(value="Číslo je v nesprávném tvaru")
        self.check_phone_label: Label = Label(master, textvariable=self.check_phone_label_var, font=check_label_font,
                                              fg="red")

        self.bind_entries_with_checks()

        return master

    def buttonbox(self):
        super(AddContactDialog, self).buttonbox()
        self.ok_btn.configure(text="Uložit")
        self.ok_btn["state"] = "disabled"

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def apply(self):
        """
        Saves contact data from the dialog window
        """
        contact = {}
        keys = list(LABELS.keys())
        for i, entry in enumerate(self.entry_list):
            if entry.get() != "":
                contact[keys[i]] = entry.get()
        name = contact["person_name"]
        self.data_manager.get_all_contacts()[name] = contact
        self.data_manager.write_contacts()

        # update listbox
        self.update_listbox()

    def update_listbox(self):
        self.listbox_string_var.set(self.data_manager.get_all_names())

    def bind_entries_with_checks(self):
        """
        Binds the name, email and phone entry with check function, so user can save only valid contacts
        """
        # binds the name Entry with check function
        self.text_vars[0].trace_add("write", self.check_name)
        # binds the birthday Entry with check function
        self.text_vars[1].trace_add("write", self.check_birthday)
        # binds the email Entry with check function
        self.text_vars[2].trace_add("write", self.check_email)
        # binds the phone Entry with check function
        self.text_vars[3].trace_add("write", self.check_phone)

    def check_name(self, *args):
        if self.text_vars[0].get():
            self.check_name_label.grid_forget()
            self.valid_name = True

            self.enable_ok_button()
        else:
            self.valid_name = False
            self.check_name_label.grid(column=2, row=1, padx=(30, 30), sticky="w")
            self.ok_btn["state"] = "disabled"

    def check_birthday(self, *args):
        birthday = self.text_vars[1].get()

        if birthday:
            try:
                dt_object = datetime.datetime.strptime(birthday, "%d.%m.%Y").date()
                self.check_birthday_label.grid_forget()
                self.valid_birthday = True

                self.enable_ok_button()
            except ValueError:
                self.valid_birthday = False
                self.check_birthday_label.grid(column=2, row=2, padx=(30, 30), sticky="w")
                self.ok_btn["state"] = "disabled"
        else:
            self.check_birthday_label.grid_forget()
            self.valid_birthday = True

            self.enable_ok_button()

    def check_email(self, *args):
        email = self.text_vars[2].get()

        if email:
            email_parts = email.split("@")
            if len(email_parts) == 2 and len(email_parts[1].split(".")) == 2 and email_parts[1].split(".")[0] != ""\
                    and email_parts[1].split(".")[1]:
                self.check_email_label.grid_forget()
                self.valid_email = True

                self.enable_ok_button()
            else:
                self.valid_email = False
                self.check_email_label.grid(column=2, row=3, padx=(30, 30), sticky="w")
                self.ok_btn["state"] = "disabled"
        else:
            self.check_email_label.grid_forget()
            self.valid_email = True

            self.enable_ok_button()

    def check_phone(self, *args):
        valid_chars = "0123456789 "
        phone = self.text_vars[3].get()
        is_valid = True

        if phone:
            if phone.startswith("+"):
                phone = phone[1:]
            for char in phone:
                if char not in valid_chars:
                    is_valid = False
                    break

            if is_valid:
                self.check_phone_label.grid_forget()
                self.valid_phone = True

                self.enable_ok_button()
            else:
                self.valid_phone = False
                self.check_phone_label.grid(column=2, row=4, padx=(30, 30), sticky="w")
                self.ok_btn["state"] = "disabled"

        else:
            self.check_phone_label.grid_forget()
            self.valid_phone = True

            self.enable_ok_button()

    def enable_ok_button(self):
        if self.valid_name and self.valid_birthday and self.valid_email and self.valid_phone:
            self.ok_btn["state"] = "normal"


class EditContactDialog(AddContactDialog):
    def __init__(self, parent, data_manager: DataManager, listbox_string_var: StringVar, person_name: str):
        self.person_name: str = person_name
        super().__init__(parent, data_manager, listbox_string_var, title="Upravit kontakt")

    def body(self, master):
        super(EditContactDialog, self).body(master)
        edited_contact = self.data_manager.get_person(self.person_name)

        for i, key in enumerate(LABELS.keys()):
            if key in edited_contact:
                self.entry_list[i].insert(0, edited_contact[key])

        return master

    def buttonbox(self):
        super(EditContactDialog, self).buttonbox()
        self.ok_btn.configure(text="Upravit")

    def apply(self):
        """
        Saves contact data from the dialog window
        """
        contact = {}
        keys = list(LABELS.keys())
        for i, entry in enumerate(self.entry_list):
            if entry.get() != "":
                contact[keys[i]] = entry.get()
        name = contact["person_name"]

        del self.data_manager.get_all_contacts()[self.person_name]
        self.data_manager.get_all_contacts()[name] = contact
        self.data_manager.write_contacts()

        # update listbox
        self.update_listbox()
