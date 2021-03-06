import bcrypt
import secrets
from datetime import datetime, timedelta
import jwt
from bson import ObjectId
from typing import List

from ..services.mongo import db
from ..mail.mail import Mail

from ..env import JWT_SECRET
from backend.errors import AppError


class User(object):

    def __init__(self):
        pass

    def login(self, email: str, password: str):
        if not email or not password:
            raise AppError("Invalid data").set_code(404)

        user = db.users.find_one({"email": email})

        if not user:
            raise AppError("User not found").set_code(404)

        if not bcrypt.checkpw(password.encode(), user["password"]):
            raise AppError("Autentication failed").set_code(404)

        payload = {
            "sub": user["email"],
            "exp": datetime.now() + timedelta(hours=12),
            "id": str(user["_id"]),
            "verified": user["isVerified"],
            "name": user["name"],
            "permissions": user["permissions"]
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        print(token)
        return {"name": user["name"], "email": user["email"], "permissions": user["permissions"], "verified": user["isVerified"], "token": token}

    def register(self, name: str, email: str, password: str, permissions: List[str] = None):
        if not name or not email or not password:
            raise AppError("Invalid data").set_code(404)

        email_service = Mail()

        # Checa se usuário já existe
        check_user = db.users.find_one({"email": email})

        if check_user:
            if check_user["isVerified"] == True:
                return {"msg": "User already exists"}
            else:
                if not bcrypt.checkpw(password.encode(), check_user["password"]):
                    raise AppError("User already registered and not validated")

                token = secrets.token_hex(16)
                db.secretToken.update({"_userId": check_user["_id"]}, {
                    "_userId": check_user["_id"], "token": token, "createdAt": datetime.now()}, upsert=True)
                # Envia email com novo token
                to = check_user["email"]
                reply_to = "No reply"
                subject = "Email de Verificação"
                message = f"Novo link de confirmação https://bemaker.store/user/validation/{token}"

                email_service.send_email(to, reply_to, subject, message)

                return {"msg": "New email verification sent", "_id": check_user["_id"]}

        try:
            inserted_user = db.users.insert_one({
                "name": name,
                "email": email,
                "password": bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
                "permissions": permissions if permissions else [],
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
        message = f"Link de confirmação https://bemaker.store/user/validation/{token}"

        email_service.send_email(to, reply_to, subject, message)

        return {"msg": "Verification email sent"}

    def email_confirmation(self, confirmation_token: str):
        secret_token = db.secretToken.find_one({"token": confirmation_token})

        if not secret_token:
            raise AppError("No token validation found").set_code(404)

        user_id = secret_token["_userId"]

        db.users.update_one({"_id": user_id}, {"$set": {"isVerified": True}})

        db.secretToken.delete_one({"token": confirmation_token})

        return {"msg": "User verified"}

    def request_password_reset(self, email: str):
        """Gera o passwordResetToken e manda para o email"""

        token = secrets.token_hex(16)

        db.users.update_one({"email": email}, {
                            "$set": {"passwordResetToken": token}})

        # Envia email com passwordResetToken
        to = email
        reply_to = "No reply"
        subject = "Redefinição de senha"
        message = f"Redefinir a sua senha https://bemaker.store/password/reset/{token}"

        email_service = Mail()
        email_service.send_email(to, reply_to, subject, message)

        return {"msg": "Password request sent"}

    def password_reset(self, new_password: str, password_reset_token: str):
        """Verifica passwordResetToken e atualiza senha"""

        verify = db.users.find_one(
            {"passwordResetToken": password_reset_token})
        if verify:
            password = bcrypt.hashpw(
                new_password.encode('utf8'), bcrypt.gensalt())
            db.users.update_one({"passwordResetToken": password_reset_token}, {
                                "$set": {"password": password}})

            return {"msg": "Password updated"}
        else:

            return {"msg": "User not found"}

    def delete(self, id: str, email: str):
        db.users.delete_one({"_id": ObjectId(id), "email": email})

        return {"msg": "User deleted"}

    def update_permissions(self, id: str, permissions: List[str]):
        db.users.update_one({"_id": ObjectId(id)}, {
                            "$set": {"permissions": permissions}})

        return {"user permissions updated": id}

    def list_users(self):
        users = []

        for x in db.users.find({"isVerified": True}, {"_id": 1, "name": 1, "email": 1, "permissions": 1}):
            users.append(x)

        return {"users": users}
