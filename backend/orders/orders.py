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

    def create(self):
        # send email
        ...

    def update(self):
        # Concluido, em entrega...
        ...
    
    def delete(self):
        # Deletar e deletar files
        ...
    
    def orders_list(self):
        # Listagem
        ...
        
    def show(self):
        # Mostra todos os detalhes do order
        ...
