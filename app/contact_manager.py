import datetime
import tkinter
from tkinter import ttk, font
from tkinter.messagebox import showinfo
from typing import Dict

from PIL import Image, ImageTk

from app.birthday_reminder_dialog import BirthdayReminderDialog
from app.choose_details_dialog import ChooseDetailsDialog
from data_manager import DataManager
from contact_dialog import ContactDialog, AddContactDialog, EditContactDialog


class App:
    def __init__(self):
        self.details_filter: Dict[str, bool] = {"birthday": True, "email": True, "phone_number": True, "note": True}
        self.sort_descending = False

        self.root = tkinter.Tk()
        self.init_root()

        self.data_manager: DataManager = DataManager()

        self.create_toolbuttons()
        self.create_listbox()

        self.show_today_birthdays()

        self.root.mainloop()

    def init_root(self):
        """
        Inits the main window
        """
        self.root.geometry('700x500')
        self.root.resizable(False, False)
        self.root.title('Správce kontaktů')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=2)

    def on_add_click(self, event=None):
        """
        Gets called when the add button is clicked
        """
        dialog = AddContactDialog(self.root, self.data_manager, self.current_contacts)
        self.sort_contacts()

    def on_remove_click(self, event=None):
        """
        Gets called when the remove button is clicked
        """
        answer = tkinter.messagebox.askyesno(title='Smazání kontaktu', message='Opravdu chcete smazat tenhle kontakt?')
        if answer:
            person_to_delete = self.listbox.get(self.listbox.curselection()[0])
            self.data_manager.remove_person(person_to_delete)
            self.current_contacts.set(self.data_manager.get_all_names())
            if not self.current_contacts.get():
                self.edit_btn["state"] = "disabled"
                self.remove_btn["state"] = "disabled"

        self.sort_contacts()

    def on_edit_click(self, event=None):
        """
        Gets called when the edit button is clicked
        """
        dialog = EditContactDialog(self.root, self.data_manager, self.current_contacts,
                                   self.listbox.get(self.listbox.curselection()[0]))
        self.sort_contacts()

    def sort_contacts(self):
        if self.sort_descending:
            self.current_contacts.set(sorted(self.data_manager.get_all_names(), key=str.lower, reverse=True))
        else:
            self.current_contacts.set(sorted(self.data_manager.get_all_names(), key=str.lower))

    def on_eye_click(self, event=None):
        """
        Gets called when the visibility button is clicked
        """
        dialog = ChooseDetailsDialog(self.root, self.details_filter)
        self.details_filter["birthday"] = dialog.birthday_var.get()
        self.details_filter["email"] = dialog.email_var.get()
        self.details_filter["phone_number"] = dialog.phone_number_var.get()
        self.details_filter["note"] = dialog.note_var.get()

    def on_sort_click(self, event=None):
        self.sort_descending = not self.sort_descending

        if self.sort_descending:
            self.sort_btn.config(relief="sunken")
            self.current_contacts.set(sorted(self.data_manager.get_all_names(), key=str.lower, reverse=True))
        else:
            self.sort_btn.config(relief="raised")
            self.current_contacts.set(sorted(self.data_manager.get_all_names(), key=str.lower))

    def create_toolbuttons(self):
        """
        Creates buttons for adding, editing and removing a contact

        """

        # create a frame (container for buttons)
        frame = tkinter.Frame(self.root)
        frame.grid(column=0, row=0, sticky='nwes')

        # load images
        pencil_image = Image.open("assets/pencil.png").resize((30, 30))
        pencil_photo = ImageTk.PhotoImage(pencil_image)

        plus_image = Image.open("assets/plus.png")
        plus_photo = ImageTk.PhotoImage(plus_image)

        delete_image = Image.open("assets/delete.png").resize((30, 30))
        delete_photo = ImageTk.PhotoImage(delete_image)

        eye_image = Image.open("assets/eye.png").resize((30, 30))
        eye_photo = ImageTk.PhotoImage(eye_image)

        # create buttons
        self.add_btn: tkinter.Button = tkinter.Button(frame, text="Přidat kontakt", command=self.on_add_click,
                                                      image=plus_photo, compound="left")
        self.add_btn.image = plus_photo
        self.edit_btn: tkinter.Button = tkinter.Button(frame, text="Editovat", command=self.on_edit_click,
                                                       image=pencil_photo, compound="left")
        self.edit_btn.image = pencil_photo

        self.remove_btn: tkinter.Button = tkinter.Button(frame, text="Odstranit", command=self.on_remove_click,
                                                         image=delete_photo, compound="left")
        self.remove_btn.image = delete_photo

        self.visibility_btn: tkinter.Button = tkinter.Button(frame, command=self.on_eye_click, image=eye_photo)
        self.visibility_btn.image = eye_photo

        self.sort_btn: tkinter.Button = tkinter.Button(frame, text="Seřadit sestupně", command=self.on_sort_click,
                                                       relief="raised")

        self.add_btn.grid(column=0, row=0, padx=(20, 0), pady=(20, 10))
        self.edit_btn.grid(column=1, row=0, padx=(10, 0), pady=(20, 10))
        self.remove_btn.grid(column=2, row=0, padx=(10, 0), pady=(20, 10))
        self.visibility_btn.grid(column=3, row=0, padx=(10, 0), pady=(20, 10))
        self.sort_btn.grid(column=0, row=1, padx=(10, 0), pady=(0, 10))

        self.edit_btn["state"] = "disabled"
        self.remove_btn["state"] = "disabled"

        self.create_searchbox(frame)

    def create_searchbox(self, master: tkinter.Frame):
        master.columnconfigure(4, weight=1)
        frame = tkinter.Frame(master, borderwidth=1, relief="sunken", highlightthickness=1)
        frame.grid(column=4, row=0, padx=(80, 0), pady=(20, 10), sticky="nwse")

        self.search_entry_content: tkinter.StringVar = tkinter.StringVar()
        self.search_entry: tkinter.Entry = tkinter.Entry(frame, borderwidth=0, highlightthickness=0,
                                                         textvariable=self.search_entry_content)

        search_tool_image = Image.open("assets/searchtool.png")
        search_tool_photo = ImageTk.PhotoImage(search_tool_image)

        image_label = tkinter.Label(frame, image=search_tool_photo)
        image_label.image = search_tool_photo
        image_label.pack(side="left", fill="y")
        self.search_entry.pack(side="right", fill="both", expand=True)

        self.search_entry_content.trace_add("write", self.search)

    def search(self, *args):
        # are there any items in the listbox?
        if self.data_manager.get_all_contacts():
            # searchbox isnt empty
            if self.search_entry_content.get():
                self.search_contacts(self.search_entry.get())
            # otherwise show everything
            else:
                self.current_contacts.set(self.data_manager.get_all_names())

    def search_contacts(self, searched_string: str):
        result = []
        searched_string = searched_string.lower()
        for value in self.data_manager.get_all_contacts().values():
            if searched_string in value["person_name"].lower():
                result.append(value["person_name"])
                continue
            if "email" in value:
                if searched_string in value["email"].lower():
                    result.append(value["person_name"])
                    continue
            if "phone_number" in value:
                if searched_string in value["phone_number"].lower():
                    result.append(value["person_name"])
                    continue

        self.current_contacts.set(result)

    def on_double_click(self, event=None):
        """Gets called whenever an item inside the listbox is double clicked"""
        if self.current_contacts.get():
            dialog = ContactDialog(self.root, self.listbox.get(self.listbox.curselection()[0]), self.data_manager,
                                   self.details_filter)

    def on_contact_select(self, event=None):
        """Gets called whenever an item inside the listbox is selected"""
        if self.current_contacts.get():
            self.edit_btn["state"] = "normal"
            self.remove_btn["state"] = "normal"

    def on_listbox_focus_out(self, event=None):
        """Gets called whenever the listbox loses focus"""
        self.edit_btn["state"] = "disabled"
        self.remove_btn["state"] = "disabled"

    def create_listbox(self):
        """
        Creates a listbox containing all contacts
        """
        font_style = font.Font(family="serif", size=20)

        self.current_contacts = tkinter.StringVar(value=self.data_manager.get_all_names())
        self.listbox = tkinter.Listbox(self.root, listvariable=self.current_contacts, font=font_style)
        self.sort_contacts()

        self.listbox.grid(column=0, row=1, sticky='nwes')

        # link a scrollbar to a listbox
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.listbox.yview)
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=1, sticky='ns')

        self.listbox.bind('<Double-1>', self.on_double_click)
        self.listbox.bind('<FocusOut>', self.on_listbox_focus_out)
        self.listbox.bind('<<ListboxSelect>>', self.on_contact_select)

    def show_today_birthdays(self):
        """
        When someone from the saved contacts has birthday the day the app is launched, it will show a window with
        his name
        """
        name_list = []
        for person in self.data_manager.get_all_contacts().values():
            if "birthday" in person:
                if datetime.datetime.strptime(person["birthday"], "%d.%m.%Y").date() == datetime.date.today():
                    name_list.append(person["person_name"])

        if name_list:
            dialog = BirthdayReminderDialog(self.root, name_list)


app = App()
