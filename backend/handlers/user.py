import json
from ..util import lambda_method
from ..errors import AppError

# @auth("delete:user")
# @lambda_method
# def delete(event, context, **kwargs):
#     print("payload", kwargs.get("payload"))
#     # TODO Deleta usuário do banco
#     return event
@lambda_method
def delete(event, context):
    return "a"
    

@lambda_method
def test_event(event, context):

    return {"ok": event}