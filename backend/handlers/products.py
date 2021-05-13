from ..product.product import Product

from ..util import lambda_method, lambda_method_custom, auth, required, optional, notNone
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
    user_id = required(kwargs["payload"]["id"], str)

    product_data = {
        "productId": required(body["productId"], str),
        "title": required(body["title"], str),
        "price": notNone(body["price"]),
        "width": notNone(body["width"]),
        "height": notNone(body["height"]),
        "orderAvailable": required(body["orderAvailable"], bool),
        "description": required(body["description"], str),
        "images": required(body["images"], list),
        "files": optional(body["files"], list),
        "heightPacked": notNone(body["heightPacked"]),
        "weightPacked": notNone(body["weightPacked"]),
        "widthPacked": notNone(body["widthPacked"]),
        "diameterPacked": notNone(body["diameterPacked"]),
        "formatPacked": notNone(body["formatPacked"]),
    }

    product = Product()
    response = product.update(product_data, user_id)

    return response


@auth(CREATEPRODUCT)
@lambda_method_custom
def create(event, context, **kwargs):

    body = event["body"]
    user_id = required(kwargs["payload"]["id"], str)

    product_data = {
        "title": required(body["title"], str),
        "price": notNone(body["price"]),
        "width": notNone(body["width"]),
        "height": notNone(body["height"]),
        "orderAvailable": required(body["orderAvailable"], bool),
        "description": required(body["description"], str),
        "images": required(body["images"], list),
        "files": optional(body["files"], list),
        "heightPacked": notNone(body["heightPacked"]),
        "weightPacked": notNone(body["weightPacked"]),
        "widthPacked": notNone(body["widthPacked"]),
        "diameterPacked": notNone(body["diameterPacked"]),
        "formatPacked": notNone(body["formatPacked"]),
        "lengthPacked": notNone(body["diameterPacked"])
    }

    product = Product()
    response = product.create(product_data, user_id)
    response["product_created"] = str(response["product_created"])
    
    return response

@lambda_method
def show(event, context, **kwargs):

    pp = event["pathParameters"]

    product_id = required(pp["id"], str)

    product = Product()
    response = product.show(product_id)

    return response


@lambda_method
def products_list(event, context, **kwargs):

    product = Product()
    response = product.products_list()

    return response
