import json

from ..user.user import User

from ..util import lambda_method, lambda_method_custom, auth
from ..errors import AppError
from ..env import DELETEPRODUCT, UPDATEPRODUCT, CREATEPRODUCT

import bcrypt

# pylint: disable=no-value-for-parameter

# DELETE
@auth(DELETEPRODUCT)
@lambda_method_custom
def delete(event, context, **kwargs):
    body = event["body"]

    return {"order deleted": body["id"]}

# PATCH
@auth(UPDATEPRODUCT)
@lambda_method_custom
def update(event, context, **kwargs):
    body = event["body"]

    return {"order updated": body["id"]}

# POST
@auth(CREATEPRODUCT)
@lambda_method_custom
def create(event, context, **kwargs):

    body = event["body"]

    return {"order created": body["id"]}

# GET w/ path params
@lambda_method
def show(event, context, **kwargs):
    body = json.loads(event["body"])

    return {"order": body}

# GET
@lambda_method
def order_list(event, context, **kwargs):
    body = json.loads(event["body"])

    return {"orders": body}
