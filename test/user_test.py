import pytest

from backend.user.user import User
from backend.services.mongo import db

def test_user_registration():
    name = "Saymon Treviso"
    email = "saymonp.trevisan@gmail.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    user = User()

    response = user.register(name, email, password, permissions)

    assert response == {"msg": "Verification email sent"}

def test_user_registration_twice():
    name = "Saymon Treviso"
    email = "registration_twice@-.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    user = User()

    user.register(name, email, password, permissions)

    response = user.register(name, email, password, permissions)

    assert response == {"msg": "User already exists, new email verification sent"}

def test_user_registration_with_an_activated_user(verified_user):
    u, expected_response = verified_user
    
    db.users.insert_one(u)

    user = User()

    if "permissions" in u:
        response = user.register(u["name"], u["email"], u["password"], u["permissions"])
    else: 
        response = user.register(u["name"], u["email"], u["password"])

    assert response == expected_response

def test_user_registration_with_out_permissions():
    name = "Saymon Treviso"
    email = "with_out_permissions@-.com"
    password = "banana123"

    user = User()

    response = user.register(name, email, password)

    assert response == {"msg": "Verification email sent"}

def test_user_registration_with_invalid_email():
    name = "Saymon Treviso"
    email = None
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    user = User()

    with pytest.raises(Exception) as e:
        user.register(name, email, password, permissions)

    assert e.value.args[0] == "Invalid data"

@pytest.fixture(scope="module",
                params=[({"name": "Jeff", "email": "activated_user@-.com", "password": "banana123", "isVerified": True}, {"msg": "User already exists"}),
                        ({"name": "Jeff", "email": "activated_user1@-.com", "password": "banana123", "isVerified": True, "permissions": ["create:product"]}, {"msg": "User already exists"})])
def verified_user(request):
    return request.param
