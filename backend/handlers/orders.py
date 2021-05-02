import json

from ..order.order import Order

from ..util import lambda_method, lambda_method_custom, auth, required, optional
from ..env import DELETEPRODUCT, UPDATEPRODUCT, CREATEPRODUCT

# pylint: disable=no-value-for-parameter

# DELETE


@auth(DELETEPRODUCT)
@lambda_method_custom
def delete(event, context, **kwargs):
    body = event["body"]

    id = required(body["id"], str)

    order = Order()
    response = order.delete(id)

    return response

# PATCH


@auth(UPDATEPRODUCT)
@lambda_method_custom
def update(event, context, **kwargs):
    body = event["body"]

    status = required(body["status"], str)

    order = Order()
    response = order.update(status)

    return response

# POST


@auth(CREATEPRODUCT)
@lambda_method_custom
def create(event, context, **kwargs):
    body = event["body"]

    if body["quoteOrder"] == True:

        order = {
            "clientName": required(body["clientName"], str),
            "clientEmail": required(body["clientName"], str),
            "clientPhone": required(body["clientName"], str),
            "files": optional(body["clientName"], list),
            "images": optional(body["clientName"], list),
            "notes": optional(body["clientName"], str),
            "quoteOrder": required(body["clientName"], str),
        }

    elif body["quoteOrder"] == False:
        order = {
            "title": required(body["clientName"], str),
            "clientName": required(body["clientName"], str),
            "clientEmail": required(body["clientName"], str),
            "clientPhone": required(body["clientName"], str),
            "cep": required(body["clientName"], str),
            "deliverPrice": required(body["clientName"], float),
            "deliverMetod": required(body["clientName"], str),
            "_productId": required(body["clientName"], str),
            "amount": required(body["clientName"], int),
            "quoteOrder": required(body["clientName"], bool),
        }

    order = Order()
    response = order.create(order)

    return response

# GET w/ path params


@lambda_method
def show(event, context, **kwargs):
    pp = event['pathParameters']

    order = Order()
    response = order.show(pp["id"])

    return response

# GET


@lambda_method
def orders_list(event, context, **kwargs):
    order = Order()
    response = order.orders_list()

    return response
