import json
from typing import Dict, Tuple


class DataManager:
    """Responisble for manipulating with contact data (saving, writing).

        The data should have this form: {"Ondřej Marek" : {"person_name" : "Pepa", <**optional data - date of birth, telephone number, note, ...>}}
    """
    def __init__(self):
        self.data_filename: str = 'contacts.json'
        self.contacts: Dict[str, Dict[str, str]] = self.load_all_contacts()

    def load_all_contacts(self) -> Dict[str, Dict[str, str]]:
        try:
            # Contacts file exists
            contacts = self.load_contacts()
        except FileNotFoundError:
            # No contacts file, so create one
            contacts = {}
            self.create_contacts_file()

        return contacts

    def get_all_contacts(self) -> Dict[str, Dict[str, str]]:
        return self.contacts

    def get_person(self, person_name: str) -> Dict[str, str]:
        return self.contacts[person_name]

    def get_all_names(self) -> Tuple[str]:
        return tuple(self.contacts.keys())

    def remove_person(self, person_name: str):
        del self.contacts[person_name]
        self.write_contacts()

    def load_contacts(self) -> Dict[str, Dict[str, str]]:
        with open(self.data_filename, 'r+') as file:
            contacts = json.load(file)
        return contacts

    def write_contacts(self):
        with open(self.data_filename, 'w') as file:
            json.dump(self.contacts, file)

    def create_contacts_file(self):
        with open(self.data_filename, 'w') as file:
            json.dump({}, file)

