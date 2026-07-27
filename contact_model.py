import time

class Contact:
    def __init__(self, first, last, phone, owner_id, email = None, company = None, address = None, id = None):
        self.first_name = first
        self.surname = last
        self.phone = phone
        self.owner_id = owner_id
        self.email = email
        self.company = company
        self.address = address
        self.id = id if id is not None else int(time.time())
    
    def to_dict(self):
        return{
            'id': self.id,
            'owner_id': self.owner_id,
            'first_name': self.first_name,
            'surname': self.surname,
            'phone': self.phone,
            'email': self.email,
            'company': self.company,
            'address': self.address,
        }

    def update_contact(
        self,
        first_name=None,
        surname=None,
        phone=None,
        email=None,
        company=None,
        address=None,
    ): 
        self.first_name = first_name if first_name is not None else self.first_name
        self.surname = surname if surname is not None else self.surname
        self.phone = phone if phone is not None else self.phone
        self.email = email if email is not None else self.email
        self.company = company if company is not None else self.company
        self.address = address if address is not None else self.address
 