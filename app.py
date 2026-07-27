import jwt 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from authentication_route import auth_router, user_manager, SECRET_KEY, ALGORITHM
from Contact_router import contact_router
 
app = FastAPI(title='Contact Manager', description='This app was built to help users manage their contacts', version= '1.0.0' )

@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.url.path == '/' or request.url.path.startswith('/auth') or request.url.path.startswith('/docs') or request.url.path.startswith('/openapi.json'):
        return await call_next(request)

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JSONResponse(content={'message':'Invalid or missing token'}, status_code=401) 
    
    token = auth_header

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return JSONResponse(content={'message':'Invalid or missing token'}, status_code=401) 
    
    if not payload.get('id'):
        return JSONResponse(content={'message':'Invalid or missing token'}, status_code=401) 
    request.state.id = payload.get('id')
    request.state.sub = payload.get('sub')
    
    return await call_next(request)
 
        
app.include_router(auth_router, prefix="/auth")
app.include_router(contact_router, prefix = "/contacts")

@app.get("/")
def home():
    return {'message': 'Contact Manager API is running successfully!!!'}




