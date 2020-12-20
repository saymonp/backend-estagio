import json
from ..util import lambda_method, auth
from ..errors import AppError
from backend.mail.mail import Mail

# pylint: disable=no-value-for-parameter

@auth("delete")
@lambda_method
def delete(payload=None, *arg1, **arg2):
    print("payload ain", payload)
    return {"ok": 1}