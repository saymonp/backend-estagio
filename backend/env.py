from os import getenv

HOST_UMBLER = getenv("HOST_UMBLER")
PORT_UMBLER = getenv("PORT_UMBLER")
USER_UMBLER = getenv("USER_UMBLER")
PASS_UMBLER = getenv("PASS_UMBLER")

HOST_ZOHO = getenv("HOST_ZOHO")
PORT_ZOHO = getenv("PORT_ZOHO")
USER_ZOHO = getenv("USER_ZOHO")
PASS_ZOHO = getenv("PASS_ZOHO")

PROD_MONGO_URI = getenv("PROD_MONGO_URI")
DEV_MONGO_URI = getenv("DEV_MONGO_URI")

JWT_SECRET = getenv("JWT_SECRET")

DELETEUSER = getenv("DELETEUSER")
UPDATEUSER = getenv("UPDATEUSER")
CREATEUSER = getenv("CREATEUSER")

CREATEPRODUCT = getenv("CREATEPRODUCT")
DELETEPRODUCT = getenv("DELETEPRODUCT")
UPDATEPRODUCT = getenv("UPDATEPRODUCT")
