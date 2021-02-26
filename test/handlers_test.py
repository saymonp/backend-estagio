import json
import pytest

from backend.handlers.contact_email import send_contact_email
from backend.handlers.users import delete, register, request_password_reset, password_reset

from backend.user.user import User


def test_contact_email():
    event = {"body": "{\"clientFirstName\": \"Client Name\", \"clientLastName\": \"Client Last Name\", \"clientEmail\": \"example@teste.com\", \"subject\": \"Teste Handler Serverless\", \"message\": \"Teste Serverless...\"}"}

    response = send_contact_email(event, None)
    body = json.loads(response["body"])

    assert body == {"ok": "Email sent"}


def test_user_delete():
    user = User()
    email = "toDelete@delete"
    user_to_del = user.register("ToDelete", email, "banana123")

    user_id = user_to_del["_id"]

    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6ImRlbGV0ZTp1c2VyIn0.SeTu_ZfAORdpmtpiX9YTZ0p97pxGfxGEu3qwjQT07O4", "Content-Type": "application/json"}, "body": {"id": user_id, "email": email}}
   
    response = delete(event, None)
    print(response)
    body = response
    
    assert body == {"deleted user": user_id}

def test_user_register():
    name = "Saymon Treviso1"
    email = "saymonp.trevisan1@gmail.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dXNlciIsImNyZWF0ZTp1c2VyIl19.-lF5dmarBO2aQLdY9AgW4mtB8_3c_hMplSUfowhTmMU", "Content-Type": "application/json"}, 
    "body": {"name": name, "email": email, "password": password, "permissions": permissions}}
    
    res = register(event, None)
    print(res)
    assert res["msg"] == "Verification email sent"

def test_user_email_confirmation():
    ...

def test_user_request_password_reset():
    ...

def test_user_password_reset():
    ...

def test_user_list_users():
    ...