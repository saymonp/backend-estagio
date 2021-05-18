import pytest
from datetime import datetime

from backend.order.order import Order
from backend.services.mongo import db


def test_order_create():
    order_data = {
        "title": "Orçamento",
        "status": "Pendente",
        "clientName": "client_name",
        "clientEmail": "client_email",
        "clientPhone": "client_phone",
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "notes": "notes if notes else None",
        "quoteOrder": True,
        "allowContact": True
    }

    order = Order()

    response = order.create(order_data)
    test = "order_created" in response

    assert test == True


def test_order_delete():
    order_data = {
        "title": "Orçamento",
        "status": "Pendente",
        "clientName": "client_name",
        "clientEmail": "client_email",
        "clientPhone": "client_phone",
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "files": [],
        "images": [],
        "notes": "notes if notes else None",
        "quoteOrder": False,
        "allowContact": True,
    }

    order = Order()

    # order_created = order.create(order_data)

    # id = order_created["order_created"]

    response = order.delete("60a08f1a6f9ab097cf3166d2")
    print(response)
    assert response == {"msg": "Order deleted"}


def test_order_list():
    order = Order()

    response = order.orders_list()
    print(response)
    assert response["orders"] is not None


def test_order_show():
    order_data = {
        "title": "Orçamento",
        "status": "Pendente",
        "clientName": "client_name",
        "clientEmail": "client_email",
        "clientPhone": "client_phone",
        "cep": "98700000",
        "deliverPrice": 12.21,
        "amount": 1,
        "deliverMethod": 1,
        "notes": "notes if notes else None",
        "productId": "608ce08a32a9c32438f4a7f4",
        "quoteOrder": False,
        "allowContact": True,
        "state": "RS",
        "location": "Ijuí",
    }

    order = Order()

    response = order.create(order_data)

    response = order.show(response["order_created"])
    print(response)
    test = "order" in response

    assert test is not None


def test_order_update():
    order_data = {
        "title": "Orçamento",
        "status": "Pendente",
        "name": "client_name",
        "email": "client_email",
        "clientPhone": "client_phone",
        "files": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "images": [{"key": "......", "url": "...."}, {"key": "......", "url": "...."}],
        "notes": "notes if notes else None",
        "quoteOrder": True,
        "allowContact": True,
    }

    order = Order()

    res = order.create(order_data)

    id = res["order_created"]

    response = order.update(id, "Concluído")

    assert response == {"msg": "order_updated"}
