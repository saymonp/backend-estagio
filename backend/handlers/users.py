import json

from ..user.user import User

from ..util import lambda_method, auth
from ..errors import AppError
from ..env import DELETEUSER, UPDATEUSER

import bcrypt

# pylint: disable=no-value-for-parameter

@auth(DELETEUSER)
@lambda_method
def delete(event, context, **kwargs):
    try:
        #body = json.loads(event)

        # u = User()
        # u.delete(body["id"], body["email"])
        
        return {"deleted user": event["body"]["id"], "test": bcrypt.gensalt()}
    
    except Exception as e:
        raise AppError(f"User deletion failed {e}")

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