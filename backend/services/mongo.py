from pymongo import MongoClient

from ..env import PROD_MONGO_URI, DEV_MONGO_URI

db = MongoClient(DEV_MONGO_URI).get_default_database()