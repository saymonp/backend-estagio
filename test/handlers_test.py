import json
import pytest
import random, string
import json

from backend.handlers.contact_email import send_contact_email
from backend.handlers.users import login, delete, register, request_password_reset, password_reset, email_confirmation, list_users, update_permissions

from backend.user.user import User
from backend.services.mongo import db


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
    email = "porolac214@bulkbye.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dXNlciIsImNyZWF0ZTp1c2VyIl19.-lF5dmarBO2aQLdY9AgW4mtB8_3c_hMplSUfowhTmMU", "Content-Type": "application/json"}, 
    "body": {"name": name, "email": email, "password": password, "permissions": permissions}}
    
    res = register(event, None)

    assert res["msg"] == "Verification email sent"


def test_user_list_users():
    event = {"body": "{\"email\": \"porolac214@bulkbye.com\"}"}
    res = list_users(event, None)

    print(res)

def test_user_login():
    event = {"body": "{\"email\": \"nhs40e+vra5gv6hlusc@sharklasers.com\", \"password\": \"banana123\"}"}
    res = login(event, None)

    have_token = "token" in res["body"]

    assert True == have_token

def test_user_update_permissions():
    # register
    name = randstr(4)
    email = f"{randstr(4)}@{randstr(3)}.com"
    password = "banana123"
    permissions = ["update:user"]

    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dXNlciIsImNyZWF0ZTp1c2VyIl19.-lF5dmarBO2aQLdY9AgW4mtB8_3c_hMplSUfowhTmMU", "Content-Type": "application/json"}, 
    "body": {"name": name, "email": email, "password": password, "permissions": permissions}}
    
    res = register(event, None)

    assert res["msg"] == "Verification email sent"

    # Get Token
    user = db.users.find_one({"email": email})
    userid = user["_id"]

    secret_token = db.secretToken.find_one({"_userId": userid})

    token = secret_token["token"]
    
    event = {"body": f"{{\"confirmation_token\": \"{token}\"}}"}
    
    response = email_confirmation(event, None)

    assert json.loads(response["body"]) == {"msg": "User verified"}

    # login
    event = {"body": f"{{\"email\": \"{email}\", \"password\": \"banana123\"}}"}
    res = login(event, None)

    have_token = "token" in res["body"]
    
    access_token = json.loads(res["body"])["token"]

    event = {"headers": 
    {"Authorization": f"bearer {access_token}", "Content-Type": "application/json"},
    "body": {"id": str(userid), "permissions": ["update:user", "create:product", "delete:product", "update:product"]}}

    res = update_permissions(event, None)
    
    assert res == {"user permissions updated": str(userid)}

def test_user_password_reset():
    # register
    name = randstr(4)
    email = f"{randstr(4)}@{randstr(3)}.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dXNlciIsImNyZWF0ZTp1c2VyIl19.-lF5dmarBO2aQLdY9AgW4mtB8_3c_hMplSUfowhTmMU", "Content-Type": "application/json"}, 
    "body": {"name": name, "email": email, "password": password, "permissions": permissions}}
    
    res = register(event, None)

    assert res["msg"] == "Verification email sent"

    # Get Token
    user = db.users.find_one({"email": email})
    userId = user["_id"]

    secret_token = db.secretToken.find_one({"_userId": userId})

    token = secret_token["token"]
    
    event = {"body": f"{{\"confirmation_token\": \"{token}\"}}"}
    
    response = email_confirmation(event, None)

    assert json.loads(response["body"]) == {"msg": "User verified"}
    
    # request_password_reset
    event = {"body": f"{{\"email\": \"{email}\"}}"}

    response = request_password_reset(event, None)
    print("reset", response)
    assert json.loads(response["body"]) == {"msg": "Password request sent"}

    user = db.users.find_one({"email": email})

    password_reset_token = user["passwordResetToken"]

    event = {"body": f"{{\"newPassword\": \"321ananab\", \"passwordResetToken\": \"{password_reset_token}\"}}"}

    reset_response = password_reset(event, None)
    print("reset", reset_response)
    assert json.loads(reset_response["body"]) == {"msg": "Password updated"}

    # second request_password_reset
    event = {"body": f"{{\"email\": \"{email}\"}}"}

    response = request_password_reset(event, None)
    print("reset", response)
    assert json.loads(response["body"]) == {"msg": "Password request sent"}

    user = db.users.find_one({"email": email})

    password_reset_token = user["passwordResetToken"]

    event = {"body": f"{{\"newPassword\": \"321ananab\", \"passwordResetToken\": \"{password_reset_token}\"}}"}

    reset_response = password_reset(event, None)
    print("reset", reset_response)
    assert json.loads(reset_response["body"]) == {"msg": "Password updated"}

def test_user_email_confirmation():
    # register
    name = randstr(4)
    email = f"{randstr(4)}@{randstr(3)}.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    event = {"headers": {"Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dXNlciIsImNyZWF0ZTp1c2VyIl19.-lF5dmarBO2aQLdY9AgW4mtB8_3c_hMplSUfowhTmMU", "Content-Type": "application/json"}, 
    "body": {"name": name, "email": email, "password": password, "permissions": permissions}}
    
    res = register(event, None)

    assert res["msg"] == "Verification email sent"

    # Get Token
    user = db.users.find_one({"email": email})
    userId = user["_id"]

    secret_token = db.secretToken.find_one({"_userId": userId})

    token = secret_token["token"]
    
    event = {"body": f"{{\"confirmation_token\": \"{token}\"}}"}
    
    response = email_confirmation(event, None)
    print(response)
    assert json.loads(response["body"]) == {"msg": "User verified"}


def randstr(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))