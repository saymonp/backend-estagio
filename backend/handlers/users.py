import json

from ..user.user import User

from ..util import lambda_method, lambda_method_custom, auth
from ..errors import AppError
from ..env import DELETEUSER, UPDATEUSER

import bcrypt

# pylint: disable=no-value-for-parameter

@auth(DELETEUSER)
@lambda_method_custom
def delete(event, context, **kwargs):
    body = event["body"]

    u = User()
    u.delete(body["id"], body["email"])
    
    return {"deleted user": body["id"]}
    

@lambda_method
def login(event, context, **kwargs):
    ...

@lambda_method
def register(event, context, **kwargs):
    ...

@lambda_method
def email_confirmation(event, context, **kwargs):
    ...

@lambda_method
def request_password_reset(event, context, **kwargs):
    ...

@lambda_method
def password_reset(event, context, **kwargs):
    ...

@auth(UPDATEUSER)
@lambda_method
def update_permissions(event, context, **kwargs):
    ...

@lambda_method
def list_users(event, context, **kwargs):
    ...