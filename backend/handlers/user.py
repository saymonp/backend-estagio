import json
from ..util import lambda_method, auth
from ..errors import AppError
from backend.mail.mail import Mail

# pylint: disable=no-value-for-parameter

@auth("delete:user")
@lambda_method
def delete(user_id_to_delete, **kwargs):
    print("payload ain", kwargs.get("payload"))
    print(user_id_to_delete)
    # TODO Deleta usuário do banco
    return {"ok": 1}