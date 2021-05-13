import json
from bson.json_util import dumps

from ..order.order import Order

from ..util import lambda_method, lambda_method_custom, auth, required, optional
from ..env import DELETEPRODUCT, UPDATEPRODUCT, CREATEPRODUCT
from ..errors import AppError
from json.encoder import JSONEncoder

# pylint: disable=no-value-for-parameter


@auth(None)
@lambda_method_custom
def delete(event, context, **kwargs):

    pp = event["params"]["path"]

    order_id = required(pp["id"], str)

    order = Order()
    response = order.delete(order_id)

    return response


@auth(None)
@lambda_method_custom
def update(event, context, **kwargs):

    body = event["body"]

    status = required(body["status"], str)
    order_id = required(body["id"], str)

    order = Order()
    response = order.update(order_id, status)

    return response


@lambda_method
def create(event, context, **kwargs):

    body = json.loads(event["body"])

    if body["quoteOrder"] == True:

        order_data = {
            "clientName": required(body["clientName"], str),
            "clientEmail": required(body["clientEmail"], str),
            "clientPhone": required(body["clientPhone"], str),
            "files": optional(body["files"], list),
            "images": optional(body["images"], list),
            "notes": optional(body["notes"], str),
            "allowContact": required(body["allowContact"], bool),
            "quoteOrder": required(body["quoteOrder"], bool),
        }

    elif body["quoteOrder"] == False:
        order_data = {
            "title": required(body["title"], str),
            "clientName": required(body["clientName"], str),
            "clientEmail": required(body["clientEmail"], str),
            "clientPhone": required(body["clientPhone"], str),
            "deliverPrice": body["deliverPrice"],
            "deliverMethod": required(body["deliverMethod"], str),
            "productId": required(body["productId"], str),
            "amount": required(body["amount"], int),
            "allowContact": required(body["allowContact"], bool),
            "quoteOrder": required(body["quoteOrder"], bool),
            "state": body["state"],
            "cep": body["cep"],
            "location": body["location"],
        }

    order = Order()
    response = order.create(order_data)

    return response


@auth(None)
@lambda_method_custom
def show(event, context, **kwargs):
    pp = event["params"]["path"]

    order_id = required(pp["id"], str)

    order = Order()
    response = order.show(order_id)["order"][0]

    response["_id"] = str(response['_id'])

    if "productId" in response:
        response["productId"] = str(response["productId"])
    
    response["createdAt"] = response["createdAt"].strftime("%d/%m/%Y, %H:%M:%S")

    return response


@auth(None)
@lambda_method_custom
def orders_list(event, context, **kwargs):
    order = Order()
    response = order.orders_list()

    for o in response["orders"]:
        o["_id"] = str(o["_id"])
        o["createdAt"] = o["createdAt"].strftime("%d/%m/%Y, %H:%M:%S")

    return response
