from ..product.product import Product

from ..util import lambda_method, lambda_method_custom, auth, required, optional
from ..errors import AppError
from ..env import DELETEPRODUCT, UPDATEPRODUCT, CREATEPRODUCT

# pylint: disable=no-value-for-parameter


@auth(DELETEPRODUCT)
@lambda_method_custom
def delete(event, context, **kwargs):

    pp = event["params"]["path"]

    product_id = required(pp["id"], str)

    product = Product()
    response = product.delete(product_id)

    return response


@auth(UPDATEPRODUCT)
@lambda_method_custom
def update(event, context, **kwargs):

    body = event["body"]
    user_id = kwargs["payload"]["sub"]

    product = {
        "productId": required(body["productId"], str),
        "title": required(body["clientName"], str),
        "price": required(body["clientName"], float),
        "width": required(body["clientName"], float),
        "height": required(body["clientName"], float),
        "orderAvailable": required(body["clientName"], bool),
        "description": required(body["clientName"], str),
        "images": required(body["clientName"], list),
        "files": optional(body["clientName"], list),
        "heightPacked": required(body["clientName"], float),
        "weightPacked": required(body["clientName"], float),
        "widthPacked": required(body["clientName"], float),
        "diameterPacked": required(body["clientName"], float),
        "formatPacked": required(body["clientName"], int),
    }

    product = Product()
    response = product.update(product, user_id)

    return response


@auth(CREATEPRODUCT)
@lambda_method_custom
def create(event, context, **kwargs):

    body = event["body"]
    user_id = kwargs["payload"]["sub"]

    product_data = {
        "title": required(body["clientName"], str),
        "price": required(body["clientName"], float),
        "width": required(body["clientName"], float),
        "height": required(body["clientName"], float),
        "orderAvailable": required(body["clientName"], bool),
        "description": required(body["clientName"], str),
        "images": required(body["clientName"], list),
        "files": optional(body["clientName"], list),
        "heightPacked": required(body["clientName"], float),
        "weightPacked": required(body["clientName"], float),
        "widthPacked": required(body["clientName"], float),
        "diameterPacked": required(body["clientName"], float),
        "formatPacked": required(body["clientName"], int),
    }

    product = Product()
    response = product.create(product_data, user_id)

    return response


@lambda_method
def show(event, context, **kwargs):

    pp = event['pathParameters']

    product_id = required(pp["id"], str),

    product = Product()
    response = product.show(product_id)

    return response


@lambda_method
def products_list(event, context, **kwargs):

    product = Product()
    response = product.products_list()

    return response