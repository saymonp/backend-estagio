import json

from ..user.user import User

from ..util import lambda_method, lambda_method_custom, auth
from ..errors import AppError
from ..env import DELETEUSER, UPDATEUSER, CREATEUSER

import bcrypt

# pylint: disable=no-value-for-parameter

@auth(DELETEUSER)
@lambda_method_custom
def delete(event, context, **kwargs):
    body = event["body"]

    u = User()
    u.delete(body["id"], body["email"])
    
    return {"deleted user": body["id"]}

@auth(UPDATEUSER)
@lambda_method_custom
def update_permissions(event, context, **kwargs):
    body = event["body"]

    u = User()
    response = u.update_permissions(body["id"], body["permissions"])

    return response
    
@auth(CREATEUSER)
@lambda_method_custom
def register(event, context, **kwargs):
    
    body = event["body"]

    u = User()
    response = u.register(body["name"], body["email"], body["password"], permissions=body["permissions"] if "permissions" in body else None)

    return {"msg": response["msg"], "_id": str(response["_id"]) if "_id" in response else None}

@lambda_method
def login(event, context, **kwargs):
    body = json.loads(event["body"])

    u = User()
    token = u.login(body["email"], body["password"])

    return {"token": token}

@lambda_method
def email_confirmation(event, context, **kwargs):
    body = json.loads(event["body"])

    u = User()
    response = u.email_confirmation(body["confirmation_token"])

    return response

@lambda_method
def request_password_reset(event, context, **kwargs):

    body = json.loads(event["body"])

    u = User()
    response = u.request_password_reset(body["email"])

    return response

@lambda_method
def password_reset(event, context, **kwargs):
    body = json.loads(event["body"])

    u = User()
    response = u.password_reset(body["newPassword"], body["passwordResetToken"])

    return response

@lambda_method
def list_users(event, context, **kwargs):
    u = User()
    response = u.list_users()

    return response