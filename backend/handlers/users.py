import json

from ..user.user import User

from ..util import lambda_method, lambda_method_custom, auth, required, optional
from ..env import DELETEUSER, UPDATEUSER, CREATEUSER
from ..errors import AppError

# pylint: disable=no-value-for-parameter


@auth(DELETEUSER)
@lambda_method_custom
def delete(event, context, **kwargs):
    body = event["body"]

    user_id = required(body["id"], str)
    email = required(body["email"], str)

    u = User()
    u.delete(user_id, email)

    return {"deleted user": body["id"]}


@auth(UPDATEUSER)
@lambda_method_custom
def update_permissions(event, context, **kwargs):
    body = event["body"]

    user_id = required(body["id"], str)
    permissions = required(body["permissions"], list)

    u = User()
    response = u.update_permissions(user_id, permissions)

    return response


@auth(CREATEUSER)
@lambda_method_custom
def register(event, context, **kwargs):

    body = event["body"]

    name = required(body["name"], str)
    email = required(body["email"], str)
    password = required(body["password"], str)
    permissions = optional(body["permissions"], list)

    u = User()
    response = u.register(name, email, password, permissions=permissions)

    return {"msg": response["msg"], "_id": str(response["_id"]) if "_id" in response else None}


@lambda_method
def login(event, context, **kwargs):
    try:
        body = json.loads(event["body"])

        email = required(body["email"], str)
        password = required(body["password"], str)

        u = User()
        user = u.login(email, password)

        return {"user": user}
    except Exception as e:
        raise AppError(e).set_code(404)


@lambda_method
def email_confirmation(event, context, **kwargs):
    try:
        body = json.loads(event["body"])

        confirmation_token = required(body["confirmationToken"], str)

        u = User()
        response = u.email_confirmation(confirmation_token)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@lambda_method
def request_password_reset(event, context, **kwargs):
    try:
        body = json.loads(event["body"])

        email = required(body["email"], str)

        u = User()
        response = u.request_password_reset(email)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@lambda_method
def password_reset(event, context, **kwargs):
    try:
        body = json.loads(event["body"])

        new_password = required(body["newPassword"], str)
        password_reset_token = required(body["passwordResetToken"], str)

        u = User()
        response = u.password_reset(new_password, password_reset_token)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@lambda_method
def list_users(event, context, **kwargs):
    try:
        u = User()
        response = u.list_users()

        return response
    except Exception as e:
        raise AppError(e).set_code(404)
