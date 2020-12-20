import json
from ..util import lambda_method, auth
from ..errors import AppError
from backend.mail.mail import Mail

# pylint: disable=no-value-for-parameter

@auth("delete:user")
@lambda_method
def delete(event, context, **kwargs):
    print("payload", kwargs.get("payload"))
    # TODO Deleta usuário do banco
    return {"ok": 1}