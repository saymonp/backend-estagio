import secrets
from datetime import datetime

import bcrypt

from ..services.mongo import db
from ..mail.mail import Mail



class User(object):

    def __init__(self):
        pass

    def login(self):
        ...

    def register(self, name: str, email: str, password: str, permissions: str = None):
        print(name, email, password, permissions)
        if not name or not email or not password:
            raise Exception("Invalid data")

        email_service = Mail()

        # Checa se usuário já existe
        check_user = db.users.find_one({"email": email})

        if check_user:
            if check_user["isVerified"] == True:
                return {"msg": "User already exists"}
            else:
                token = secrets.token_hex(16)
                db.secretToken.update({"_userId": check_user["_id"]}, {
                                                    "_userId": check_user["_id"], "token": token, "createdAt": datetime.now()}, upsert=True)
                # Envia email com novo token
                to = check_user["email"]
                reply_to = "No reply"
                subject = "Email de Verificação"
                message = f"Novo link de confirmação http://localhost:4200/user/validation/{token}"

                email_service.send_email(to, reply_to, subject, message)

                return {"msg": "User already exists, new email verification sent"}

        try:
            inserted_user = db.users.insert_one({
                "name": name,
                "email": email,
                "password": bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
                "permissions": permissions,
                "isVerified": False,
            })

            token = secrets.token_hex(16)

            db.secretToken.insert_one({
                "_userId": inserted_user.inserted_id,
                "token": token,
                "createdAt": datetime.now()
            })
        except TypeError:
            return {"msg": "Invalid data"}

        # Envia email
        to = email
        reply_to = "No reply"
        subject = "Email de Verificação"
        message = f"Link de confirmação http://localhost:4200/user/validation/{token}"

        email_service.send_email(to, reply_to, subject, message)

        return {"msg": "Verification email sent"}


    def email_confirmation(self, confirmation_token):
        secret_token = db.secretToken.find_one({"token": confirmation_token})

        if not secret_token:
            raise Exception("No token validation found")

        user_id = secret_token["_userId"]

        db.users.find_one_and_update({"_id": user_id}, {"isVerified": True})

        return {"msg": "User verified"}

    def delete(self):
        ...

    def add_permissions(self):
        ...

    def revoke_permissions(self):
        ...
