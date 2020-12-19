import json
from ..util import lambda_method, auth
from ..errors import AppError
from backend.mail.mail import Mail

# pylint: disable=no-value-for-parameter

@auth("delete")
@lambda_method
def delete(event, context):
    return {"ok": 1}