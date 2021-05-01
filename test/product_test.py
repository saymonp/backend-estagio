import pytest
from datetime import datetime

from backend.product.product import Product
from backend.services.mongo import db


def test_product_create():
    product_data = {
        "title": "product",
        "price": 32.34,
        "width": 1.2,
        "height": 1.2,
        "orderAvailable": True,
        "description": "product.....",
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "heightPacked": 1.2,
        "weightPacked": 1.2,
        "widthPacked": 1.2,
        "diameterPacked": 1.2,
        "formatPacked": 1,
        "createdAt": datetime.utcnow()
    }

    product = Product()

    user_id = "5ffdf8e2501ff95d8bf444d9"

    response = product.create(product_data, user_id)
    test = "product_created" in response

    assert test == True


def test_product_delete():
    product_data = {
        "title": "product",
        "price": 32.34,
        "width": 1.2,
        "height": 1.2,
        "orderAvailable": True,
        "description": "product.....",
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "heightPacked": 1.2,
        "weightPacked": 1.2,
        "widthPacked": 1.2,
        "diameterPacked": 1.2,
        "formatPacked": 1,
        "createdAt": datetime.utcnow()
    }

    product = Product()

    user_id = "5ffdf8e2501ff95d8bf444d9"

    product_created = product.create(product_data, user_id)

    id = product_created["product_created"]

    response = product.delete(str(id))

    assert response == {"msg": "Product deleted"}


def test_product_list():
    product = Product()

    response = product.products_list()
    print(response)
    assert response["products"] is not None


def test_product_show():
    product_data = {
        "title": "product",
        "price": 32.34,
        "width": 1.2,
        "height": 1.2,
        "orderAvailable": True,
        "description": "product.....",
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "heightPacked": 1.2,
        "weightPacked": 1.2,
        "widthPacked": 1.2,
        "diameterPacked": 1.2,
        "formatPacked": 1,
        "createdAt": datetime.utcnow()
    }

    product = Product()

    user_id = "5ffdf8e2501ff95d8bf444d9"

    response = product.create(product_data, user_id)

    response = product.show(response["product_created"])
    print(response)
    test = "product" in response

    assert test is not None


def test_product_update():
    product_data = {
        "title": "product",
        "price": 32.34,
        "width": 1.2,
        "height": 1.2,
        "orderAvailable": True,
        "description": "product.....",
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "heightPacked": 1.2,
        "weightPacked": 1.2,
        "widthPacked": 1.2,
        "diameterPacked": 1.2,
        "formatPacked": 1,
        "createdAt": datetime.utcnow()
    }

    product = Product()

    user_id = "5ffdf8e2501ff95d8bf444d9"

    res = product.create(product_data, user_id)

    product_id = res["product_created"]

    update_data = {
        "productId": str(product_id),
        "title": "productUpdate",
        "price": 32.34,
        "width": 1.2,
        "height": 1.2,
        "orderAvailable": True,
        "description": "product.....",
        "images": [{"key": "update", "url": "...."}, {"key": "......", "url": "...."}],
        "files": [{"key": "update", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "heightPacked": 1.2,
        "weightPacked": 1.2,
        "widthPacked": 1.2,
        "diameterPacked": 1.2,
        "formatPacked": 1,
        "createdAt": datetime.utcnow()
    }

    response = product.update(update_data, user_id)

    assert response == {"msg": "product_updated"}
