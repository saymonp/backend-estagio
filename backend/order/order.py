from datetime import datetime
import jwt
from bson import ObjectId
from typing import List

from ..services.mongo import db
from ..services.s3 import S3

from backend.errors import AppError


class Order(object):

    def _init_(self):
        pass

    def create(self, order):
        if order["quoteOrder"] == True:
            # Quote Order
            inserted_order = db.orders.insert_one({
                "title": "Orçamento",
                "status": "Pendente",
                "clientName": order["clientName"],
                "clientEmail": order["clientEmail"],
                "clientPhone": order["clientPhone"],
                "files": order["files"] if order["files"] else [],
                "images": order["images"] if order["images"] else [],
                "notes": order["notes"],
                "quoteOrder": order["quoteOrder"],
                "allowContact": order["allowContact"],
                "createdAt": datetime.utcnow()
            })

            return {"order_created": inserted_order.inserted_id}

        elif order["quoteOrder"] == False:
            # Product Order
            inserted_order = db.orders.insert_one({
                "title": order["title"],
                "status": "Pendente",
                "clientName": order["clientName"],
                "clientEmail": order["clientEmail"],
                "clientPhone": order["clientPhone"],
                "cep": order["cep"],
                "deliverPrice": order["deliverPrice"],
                "deliverMethod": order["deliverMethod"],
                "productId": ObjectId(order["productId"]),
                "amount": order["amount"],
                "quoteOrder": order["quoteOrder"],
                "allowContact": order["allowContact"],
                "createdAt": datetime.utcnow()
            })

            return {"order_created": inserted_order.inserted_id}

    def update(self, id: str, status: str):
        updated_order = db.orders.update_one(
            {"_id": ObjectId(id)}, {"$set": {"status": status}})

        return {"msg": "order_updated"}

    def delete(self, id: str):
        files = db.orders.find_one({"_id": ObjectId(id), "quoteOrder": True}, {
                                   "files": 1, "images": 1})

        if files and files["files"]:
            s3 = S3()
            for f in files["images"]:
                s3.delete(f.key)

        if files and files["images"]:
            s3 = S3()
            for img in files["images"]:
                s3.delete(img.key)

        db.orders.delete_one({"_id": ObjectId(id)})

        return {"msg": "Order deleted"}

    def orders_list(self):
        orders = []

        for x in db.orders.find({}, {"_id": 1, "title": 1, "clientName": 1, "clientEmail": 1, "clientPhone": 1, "status": 1, "createdAt": 1}):
            orders.append(x)

        return {"orders": orders}

    def show(self, id: str):
        # order = db.orders.find_one({"_id": ObjectId(id)})

        order = db.orders.aggregate([
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            },
            {
                "$lookup": {
                    "from": "products",
                    "localField": "productId",
                    "foreignField": "_id",
                    "as": "productData"
                }
            },
            {
                "$project": {
                    "title": 1,
                    "status": 1,
                    "clientName": 1,
                    "clientEmail": 1,
                    "clientPhone": 1,
                    "cep": 1,
                    "deliverPrice": 1,
                    "deliverMethod": 1,
                    "productId": 1,
                    "amount": 1,
                    "quoteOrder": 1,
                    "files": 1,
                    "images": 1,
                    "notes": 1,
                    "createdAt": 1,
                    "productData": {
                        "title": 1,
                        "price": 1,
                        "description": 1,
                        "files": 1,
                        "images": 1
                    }
                },

            },

        ])

        return {"order": [o for o in order]}
