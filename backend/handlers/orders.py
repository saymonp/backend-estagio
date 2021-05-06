from ..order.order import Order

from ..util import lambda_method, lambda_method_custom, auth, required, optional
from ..env import DELETEPRODUCT, UPDATEPRODUCT, CREATEPRODUCT
from ..errors import AppError

# pylint: disable=no-value-for-parameter


@auth(DELETEPRODUCT)
@lambda_method_custom
def delete(event, context, **kwargs):
    try:
        pp = event["params"]["path"]
        
        order_id = required(pp["id"], str)

        order = Order()
        response = order.delete(order_id)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@auth(UPDATEPRODUCT)
@lambda_method_custom
def update(event, context, **kwargs):
    try:
        body = event["body"]

        status = required(body["status"], str)

        order = Order()
        response = order.update(status)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@auth(CREATEPRODUCT)
@lambda_method_custom
def create(event, context, **kwargs):
    try:
        body = event["body"]

        if body["quoteOrder"] == True:

            order = {
                "clientName": required(body["clientName"], str),
                "clientEmail": required(body["clientName"], str),
                "clientPhone": required(body["clientName"], str),
                "files": optional(body["clientName"], list),
                "images": optional(body["clientName"], list),
                "notes": optional(body["clientName"], str),
                "allowContact": required(body["allowContact"], str),
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
                "allowContact": required(body["allowContact"], str),
                "quoteOrder": required(body["clientName"], bool),
            }

        order = Order()
        response = order.create(order)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@lambda_method
def show(event, context, **kwargs):
    try:
        pp = event['pathParameters']

        order_id = required(pp["id"], str)

        order = Order()
        response = order.show(order_id)

        return response
    except Exception as e:
        raise AppError(e).set_code(404)


@lambda_method
def orders_list(event, context, **kwargs):
    try:
        order = Order()
        response = order.orders_list()

        return response
    except Exception as e:
        raise AppError(e).set_code(404)
