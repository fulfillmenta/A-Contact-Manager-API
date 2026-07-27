import time

class User:
    def __init__(self, id, first_name, last_name, address, date_of_birth, email, username, password):
        self.id = id if id is not None else int(time.time())
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.date_of_birth = date_of_birth
        self.email = email
        self.username = username
        self.password = password
        
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
            'username': self.username,
        }
 
    def update_user(
        self,
        first_name=None,
        last_name=None,
        address=None,
        date_of_birth=None,
        email=None,
        username=None,
    ):
        self.first_name = first_name if first_name is not None else self.first_name
        self.last_name = last_name if last_name is not None else self.last_name
        self.address = address if address is not None else self.address
        self.date_of_birth = date_of_birth if date_of_birth is not None else self.date_of_birth
        self.email = email if email is not None else self.email
        self.username = username if username is not None else self.username
 