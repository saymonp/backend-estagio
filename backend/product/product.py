from datetime import datetime, timedelta
from bson import ObjectId

from ..services.mongo import db
from ..services.s3 import S3


class Product(object):

    def __init__(self):
        pass

    def create(self, product, user_id):

        inserted_product = db.products.insert_one({
            "userId": ObjectId(user_id),
            "title": product["title"],
            "price": product["price"],
            "width": product["width"],
            "height": product["height"],
            "orderAvailable": product["orderAvailable"],
            "description": product["description"],
            "images": product["images"],
            "files": product["files"],
            "heightPacked": product["heightPacked"],
            "weightPacked": product["weightPacked"],
            "widthPacked": product["widthPacked"],
            "diameterPacked": product["diameterPacked"],
            "formatPacked": product["formatPacked"],
            "createdAt": datetime.utcnow()
        })

        return {"product_created": inserted_product.inserted_id}

    def update(self, product, user_id):
        inserted_product = db.products.update_one({"_id": ObjectId(product["productId"])}, {"$set": {
            "userId": ObjectId(user_id),
            "title": product["title"],
            "price": product["price"],
            "width": product["width"],
            "height": product["height"],
            "orderAvailable": product["orderAvailable"],
            "description": product["description"],
            "images": product["images"],
            "files": product["files"],
            "heightPacked": product["heightPacked"],
            "weightPacked": product["weightPacked"],
            "widthPacked": product["widthPacked"],
            "diameterPacked": product["diameterPacked"],
            "formatPacked": product["formatPacked"],
            "createdAt": datetime.utcnow()}})

        return {"msg": "product_updated"}

    def delete(self, id):
        files = db.products.find_one({"_id": ObjectId(id)}, {
                                     "files": 1, "images": 1})

        if files and files["files"]:
            s3 = S3()
            for f in files["images"]:
                s3.delete(f.key)

        if files and files["images"]:
            s3 = S3()
            for img in files["images"]:
                s3.delete(img.key)

        db.products.delete_one({"_id": ObjectId(id)})

        return {"msg": "Order deleted"}

    def products_list(self):
        products = []

        for x in db.products.find({}, {"_id": 1, "title": 1, "price": 1, "images": 1}):
            products.append(x)

        return {"products": products}

    def show(self, id: str):
        product = db.products.find_one({"_id": ObjectId(id)})

        return {"product": product}
