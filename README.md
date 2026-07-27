Contact Manager API

A simple FastAPI app for user registration/login (JWT auth) and per-user contact
management (create, read, search, update, delete). Data is persisted to flat
JSON files (users.json, contacts.json) on disk — no database required.

Project structure

user_model.py          User data class
contact_model.py        Contact data class
user_authentication.py  UserManager: register/authenticate/load/save users
contact_manager.py      ContactManager: CRUD for one user's contacts
app.py                  FastAPI app, routes, JWT middleware

Setup

bashpip install fastapi uvicorn pyjwt pydantic
uvicorn app:app --reload

The API runs at http://localhost:8000. Interactive docs are available at
http://localhost:8000/docs (this route is exempt from auth).

Authentication

All routes except /, /auth/*, /docs, and /openapi.json require an
Authorization header containing the raw JWT returned by /auth/login
(no Bearer  prefix — just the token string itself).

Endpoints

MethodPathAuth requiredDescriptionGET/NoHealth checkPOST/auth/registerNoCreate a new userPOST/auth/loginNoLog in, returns a JWTGET/contactsYesList all contacts for the logged-in userPOST/contactsYesAdd a new contactGET/contacts/search?query=YesSearch contacts by name, phone, or idPUT/contacts/{query}YesEdit a contact matched by queryDELETE/contacts/{query}YesDelete a contact matched by query

Example request bodies

POST /auth/register

json{
  "first_name": "Jane",
  "last_name": "Doe",
  "address": "1 Main St",
  "date_of_birth": "1990-01-01",
  "email": "jane@example.com",
  "username": "janedoe",
  "password": "pass123"
}

POST /auth/login

json{ "username": "janedoe", "password": "pass123" }

POST /contacts

json{
  "first_name": "Bob",
  "surname": "Smith",
  "phone": "555-1234",
  "email": "bob@example.com",
  "company": "Acme",
  "address": "2 Side St"
}

PUT /contacts/{query} (only include fields you want to change)

json{ "phone": "555-9999" }

Testing with Bruno


Create a new collection (e.g. "Contact Manager API") with a base URL
environment variable, e.g. baseUrl = http://localhost:8000.
Add requests for each endpoint above.
For Login, save the response token field into a Bruno environment
variable (e.g. via a post-response script: bru.setEnvVar("token", res.body.token)).
For all /contacts requests, add a header Authorization: {{token}}
(no Bearer prefix).
Suggested test order: Register → Login → Add Contact → Get All Contacts →
Search Contacts → Edit Contact → Delete Contact. Also try Get All Contacts
with no/garbage Authorization header to confirm you get a 401.


Bugs found and fixed while testing

While verifying the app end-to-end (registering a user, logging in, and
exercising every contact endpoint), the following issues turned up and were
fixed:


app.py — add_contact typo crashed POST /contacts with a 500.
request.state.getsub doesn't exist; it should be request.state.sub
(the attribute the auth middleware actually sets).
app.py — the root / route was being blocked by the auth middleware.
The middleware whitelist only checked for paths starting with /auth,
/docs, /openapi.json, so GET / returned 401 instead of the health
check message. Added / to the whitelist.
user_authentication.py — broken success messages.
register() returned the literal string 'Registration successful, {username}' (not an f-string, so the placeholder was never filled in),
and login() had the same issue with 'Login successful, [username]'.
Both now use f-strings so the actual username is included.


Known limitations (not fixed, just flagged)


Plaintext passwords. Passwords are stored and compared as plain text
in users.json. Fine for a learning project, but never do this for
anything real — hash passwords (e.g. with bcrypt or passlib) before
storing them.
No password length/strength validation on registration.
update_user / update_contact use value or self.value, so passing
an empty string ("") for a field won't clear it — it'll be treated as
falsy and the old value will be kept. Use is not None checks if you want
to support intentionally clearing a field to empty.
IDs are derived from int(time.time()), so creating two users/contacts
within the same second could in theory produce the same ID.
JWTs never expire (no exp claim set), so tokens are valid forever
until the secret key changes.
Secret key is hardcoded in app.py. For anything beyond local testing,
load it from an environment variable instead.