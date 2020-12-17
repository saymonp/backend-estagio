import secrets
from datetime import datetime

from ..services.mongo import db
from ..mail.mail import Mail



class User(object):

    def __init__(self):
        pass

    def login(self):
        ...

    def register(self, name: str, email: str, password: str, permissions: str = None):
        email_service = Mail()

        # Checa se usuário já existe
        check_user = db.users.find_one({"email": email})

        if check_user:
            if check_user["isVerified"] == True:
                return {"msg": "User already exists"}
            else:
                token = secrets.token_hex(16)
                db.secretToken.find_one_and_replace({"_userId": check_user["_id"]}, {
                                                    "_userId": check_user["_id"], "token": token, "createdAt": datetime.now()})
                # Envia email com novo token
                to = check_user["email"]
                reply_to = "No reply"
                subject = "Email de Verificação"
                message = f"Link de confirmação http://localhost:4200/user/validation{token}"

                email_service.send_email(to, reply_to, subject, message)

                return {"msg": "User already exists, new email verification sent"}

        user = db.users.insert({
            "name": name,
            "email": email,
            "password": password,
            "permissions": permissions,
            "isVerified": False,
        })

        token = secrets.token_hex(16)

        db.secretToken.insert({
            "_userId": user._id,
            "token": token,
            "createdAt": datetime.now(),
        })

        # Envia email
        to = email
        reply_to = "No reply"
        subject = "Email de Verificação"
        message = f"Link de confirmação http://localhost:4200/user/validation{token}"

        email_service.send_email(to, reply_to, subject, message)

        return {"msg": "verification email sent"}


    def email_confirmation(self, confirmation_token):
        secret_token = db.secretToken.find_one({"token": confirmation_token})
        user_id = secret_token["_userId"]

        db.users.find_one_and_update({"_id": user_id}, {"isVerified": True})

        return {"msg": "User verified"}

    def delete(self):
        ...

    def add_permissions(self):
        ...

    def revoke_permissions(self):
        ...
