import json
from user_model import User

class UserManager:
    def __init__(self):
        self.users:list[User] = []
        self.load_from_file()

    def find_user(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def user_from_json(self, json_obj: dict):
        return User(
            id=json_obj.get('id'),
            first_name=json_obj.get('first_name'),
            last_name=json_obj.get('last_name'),
            address=json_obj.get('address'),
            date_of_birth=json_obj.get('date_of_birth'),
            email=json_obj.get('email'),
            username=json_obj.get('username'),
            password=json_obj.get('password'),
        )

    def authenticate(self, username: str, password: str):
        user = self.find_user(username)
        if user and user.password == password:
            return user
        return None

    def register(self, first_name: str, last_name: str, address: str, date_of_birth: str, email: str, username: str, password: str, ):

        if '@' not in email or '.' not in email:
            return("Invalid email address")
        if self.find_user(username):
            return('Username already exists, type another username')
        user = User(id=None, first_name=first_name, last_name=last_name, address=address, date_of_birth=date_of_birth, email=email, username=username, password=password,)
        self.users.append(user)
        self.save_to_file()
        return (f'Registration successful, {username}', user.to_dict())

    def login(self, username: str, password: str):
        user = self.authenticate(username, password)
        if not user:
            return("Invalid username or password")
        return(f'Login successful, {username}', user.to_dict())

    def load_from_file(self, filename='users.json'):
            try:
                with open(filename, 'r') as file:
                    content = file.read().strip()
                user_info = json.loads(content) if content else []
            except FileNotFoundError:
                user_info = []
            self.users = [self.user_from_json(item) for item in user_info]

    def save_to_file(self, filename='users.json'):
        data = []
        for u in self.users:
            user_data = u.to_dict()
            user_data['password'] = u.password
            data.append(user_data)
        with open(filename, 'w') as file:
            file.write(json.dumps(data)) 