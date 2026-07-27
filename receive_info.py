from pydantic import BaseModel

class UserCreationRequest(BaseModel):
    # Register
    first_name: str
    last_name: str
    address: str
    date_of_birth: str
    email: str
    username: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class ContactCreationRequest(BaseModel):
    # Add contact
    first_name: str
    surname: str
    phone: str
    email: str = None
    company: str = None
    address: str = None

class ContactUpdateRequest(BaseModel):
    # Edit contact
    first_name: str = None
    surname: str = None
    phone: str = None
    email: str = None
    company: str = None
    address: str = None