import pytest

from backend.user.user import User

def test_user_registration():
    name = "Saymon Treviso"
    email = "saymonp.trevisan@gmail.com"
    password = "banana123"
    permissions = ["create:product", "delete:product", "update:product"]

    user = User()

    response = user.register(name, email, password, permissions)

    assert response == {"msg": "verification email sent"}

def test_user_registration_twice():
    ...

def test_user_registration_with_out_permissions():
    ...

