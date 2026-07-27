import json
from contact_model import Contact

class ContactManager:
    def __init__(self, username: str):
        self.owner_id = f"{username}_contacts"
        self.filename = 'contacts.json'
        self.contacts = []
        self.load_from_file()
 
    def contact_from_json(self, json_obj: dict):
        return Contact(
            first=json_obj.get('first_name'),
            last=json_obj.get('surname'),
            phone=json_obj.get('phone'),
            owner_id=json_obj.get('owner_id'),
            email=json_obj.get('email'),
            company=json_obj.get('company'),
            address=json_obj.get('address'),
            id=json_obj.get('id'),
        )
 
    def find_matches(self, query: str):
        query = query.strip().lower()
        return [
            contact for contact in self.contacts
            if (query in (contact.first_name or '').lower() or
                query in (contact.surname or '').lower() or
                query in (contact.phone or '').lower()or
                query in str(contact.id).lower())
        ]
 
    #  CRUD create read update dele
 
    def add_new_contact(self, first_name: str, surname: str, phone: str, email: str = None, company: str = None, address: str = None,):
        contact = Contact(
            first = first_name,
            last = surname,
            phone =  phone,
            owner_id = self.owner_id,
            email = email,
            company = company,
            address = address,
            id = None,
        )
        self.contacts.append(contact)
        self.save_to_file()
        return contact.to_dict()
 
    def get_all_contacts(self):
        return [contact.to_dict() for contact in self.contacts]
 
    def search_contact(self, query: str):
        results = self.find_matches(query)
        return [c.to_dict() for c in results] if results else []
 
    def delete_contact(self, query: str):
        matches = self.find_matches(query)
 
        if not matches:
            return ("Contact not found")
 
        if len(matches) > 1:
            return ("Multiple contacts found.", [c.to_dict() for c in matches])
 
        contact = matches[0]
        self.contacts.remove(contact)
        self.save_to_file()
        return ("Contact successfully deleted", contact.to_dict())
 
    def edit_contact(self, query: str, updated_data: dict):
        matches = self.find_matches(query)
 
        if not matches:
            return ("Contact not found")
 
        if len(matches) > 1:
            return ("Multiple contacts found.", [c.to_dict() for c in matches])
 
        contact = matches[0]
        contact.update_contact(**updated_data)
        self.save_to_file()
        return ("Contact updated successfully", contact.to_dict())
 
    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read().strip()
            all_contacts_info = json.loads(content) if content else []
        except FileNotFoundError:
            all_contacts_info = []
 
        self.contacts = [
            self.contact_from_json(item)
            for item in all_contacts_info
            if item.get('owner_id') == self.owner_id
        ]
 
    def save_to_file(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read().strip()
            all_contacts_info = json.loads(content) if content else []
        except FileNotFoundError:
            all_contacts_info = []

        other_contacts = [contact for contact in all_contacts_info if contact.get('owner_id') != self.owner_id]
        updated = other_contacts + self.get_all_contacts()
        
        with open(self.filename, 'w') as file:
            file.write(json.dumps(updated))
 