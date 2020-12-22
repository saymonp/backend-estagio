import traceback
import functools
import json
import jwt
from typing import Callable

from .errors import AppError
# from .env import JWT_SECRET


def respond(body, code=200):
    return {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Required for CORS support to work
            # Required for cookies, authorization headers with HTTPS
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(body, default=str),
    }


def lambda_method(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return respond(fun(*args, **kwargs))
        except AppError as e:
            traceback.print_exc()
            return respond({'error': str(e), 'class': type(e).__name__}, code=e.code)
        except Exception as e:
            traceback.print_exc()
            return respond({'error': str(e), 'class': type(e).__name__}, code=500)
    return wrapper


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parametrized
def auth(f: Callable, permission: str):
    """Authentication for functions.

    Check the validation of the user's token and permissions for functions that need authentication,
    used as a decorator like:

    @auth("delete:user") # Permission required for the function delete, for a case that doesn't need a permission it's @auth(None)
    @lambda_method
    def delete(event, context, **kwargs):
        payload = kwargs.get("payload") # Access token payload ex: {'sub': '1234567890', 'name': 'John Doe', 'iat': 1516239022}
        ...
        return {"ok": 1}

    Args:
      function:
        A restricted function
      permission:
        If the user needs specific permission to access the function 
        use the decorator like @auth("create:product").
        If no specific permission is required to use the decorator like @auth(None)

    Returns:
        A dict with the payload of the token.
        Example:
        {'sub': '1234567890', 'name': 'John Doe', 'iat': 1516239022}

    Raises:
      Unauthorized: Failing due to invalid token_method or missing auth_token
    """
    def aux(*xs, **kws):
        #header = json.loads(xs[0]["headers"])
        auth_token = xs[0].get("headers")["Authorization"]

        if not auth_token:
            raise Exception('Unauthorized')

        token_method, auth_token = auth_token.split(' ')

        if not auth_token or token_method.lower() != 'bearer':
            print("Failing due to invalid token_method or missing auth_token")
            raise Exception('Unauthorized')
        
        try:
            payload = jwt.decode(auth_token, "banana123")
            # TODO Checa permissões
            print(payload)

            return f(payload=payload, *xs, **kws)
        except Exception as e:
            print(f'Exception encountered: {e}')
            raise Exception('Unauthorized')
        
        return f(*xs, **kws)
        
    return aux