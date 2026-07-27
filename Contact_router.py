from fastapi import APIRouter, Request, Response
from receive_info import ContactCreationRequest, ContactUpdateRequest
from contact_manager import ContactManager


contact_router = APIRouter()

@contact_router.get("/")
def get_all_contacts(request: Request, response: Response):
    manager = ContactManager(username = request.state.sub)
    return manager.get_all_contacts()

@contact_router.post("/add_contact")
def add_contact(request: Request, response: Response, contact: ContactCreationRequest):
    current_sub = request.state.sub
    manager = ContactManager(username=current_sub)
    new_contact = manager.add_new_contact(
        first_name=contact.first_name,
        surname=contact.surname,
        phone=contact.phone,
        email=contact.email,
        company=contact.company,
        address=contact.address,
    )
    response.status_code = 201
    return new_contact
 
@contact_router.get("/search")
def search_contacts(request: Request, response: Response, query: str):
    manager = ContactManager(username=request.state.sub)
    results = manager.search_contact(query)
    if not results:
        response.status_code = 404
        return 'No contacts found matching that query'
    return results

@contact_router.put("/edit/{query}")
def edit_contact(query: str, request: Request, response: Response, contact:ContactUpdateRequest):
    manager = ContactManager(username = request.state.sub)

    updated_data = {
        "first_name": contact.first_name,
        "surname": contact.surname,
        "phone": contact.phone,
        "email": contact.email,
        "company": contact.company,
        "address": contact.address,
    }
    result = manager.edit_contact(query=query, updated_data=updated_data)
    if result == 'Contact not found':
        response.status_code = 404
        return result
    
    message, data = result
    if message == "Multiple contacts found.":
        response.status_code = 409
        return {'message': message, 'matches': data}
 
    return {'message': message, 'contact': data}

@contact_router.delete("/delete/{query}")
def delete_contact(query: str, request: Request, response: Response):
    manager = ContactManager(username = request.state.sub)
    result = manager.delete_contact(query)
 
    if result == "Contact not found":
        response.status_code = 404
        return result
 
    message, data = result
    if message == "Multiple contacts found.":
        response.status_code = 409
        return {'message': message, 'matches': data}
 
    return {'message': message, 'contact': data}
