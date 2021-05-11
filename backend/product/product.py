from datetime import datetime, timedelta
from bson import ObjectId

from ..services.mongo import db
from ..services.s3 import S3
from ..config.s3config import s3config


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
            "files": product["files"] if product["files"] else [],
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
            "files": product["files"] if product["files"] else [],
            "heightPacked": product["heightPacked"],
            "weightPacked": product["weightPacked"],
            "widthPacked": product["widthPacked"],
            "diameterPacked": product["diameterPacked"],
            "formatPacked": product["formatPacked"],
            "createdAt": datetime.utcnow()}})

        return {"msg": "product_updated"}

    def delete(self, id):
        product = db.products.find_one({"_id": ObjectId(id)}, {
                                     "files": 1, "images": 1})

        if product and product["files"] or product["images"]:
            s3 = S3(s3config.buckets.upload_bucket,
                    s3config.REGION_NAME, s3config.limits_file_size)
            if product["files"]:
                for f in product["files"]:
                    s3.delete(f["key"])

            if product["images"]:
                for img in product["images"]:
                    s3.delete(img["key"])

        db.products.delete_one({"_id": ObjectId(id)})

        return {"msg": "Product deleted"}

    def products_list(self):
        products = []

        for x in db.products.find({}, {"_id": 1, "title": 1, "price": 1, "images": {"$slice": 1}}):
            products.append(x)

        return {"products": products}

    def show(self, id: str):
        product = db.products.find_one({"_id": ObjectId(id)})

        return {"product": product}
