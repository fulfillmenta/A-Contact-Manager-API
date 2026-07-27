import jwt 
from fastapi import APIRouter, Request, Response
from receive_info import UserCreationRequest, UserLoginRequest
from pydantic import BaseModel
from user_authentication import UserManager

SECRET_KEY = 'FoxtrotUmbrellaLimaCharlieAlpha'
ALGORITHM = 'HS256'

auth_router = APIRouter()
user_manager = UserManager()

@auth_router.post('/register')
def register(request: Request, response: Response, user: UserCreationRequest):
    result = user_manager.register(
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        date_of_birth=user.date_of_birth,
        email=user.email,
        username=user.username,
        password=user.password,
    )
    if isinstance(result, str):
        response.status_code = 400
        return result
 
    response.status_code = 201
    message, user_data = result
    return {'message': message, 'user': user_data}
 
@auth_router.post('/login')
def login(response: Response, credentials: UserLoginRequest):
    user = user_manager.authenticate(
        credentials.username, 
        credentials.password,
    )
    if not user:
        response.status_code = 401
        return 'Invalid username or password'

    payload = {'id': user.id, 'sub': user.username}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {'message': 'Login successful', 'token': token, 'user': user.to_dict()}