import traceback
import functools
import json
import jwt
from typing import Callable
from collections import namedtuple

from .errors import AppError
from .env import JWT_SECRET


def required(param, instance):
    if isinstance(param, instance):

        return param
    else:
        raise AppError("Invalid data").set_code(400)


def notNone(param):
    if param:

        return param
    else:
        raise AppError("Invalid data").set_code(400)


def optional(param, instance):
    if isinstance(param, instance):

        return param
    else:
        return None


def e404():
    raise AppError("Invalid data").set_code(404)


def dict_to_namedtuple(typename, data):
    return namedtuple(typename, data.keys())(
        *(dict_to_namedtuple(typename + '_' + k, v) if isinstance(v, dict) else v for k, v in data.items())
    )


def respond(body, code=200):
    return {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Headers': 'Accept',
            'Access-Control-Allow-Origin': '*',  # Required for CORS support to work
            # Required for cookies, authorization headers with HTTPS
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
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


def lambda_method_custom(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return respond_custom(fun(*args, **kwargs))
        except AppError as e:
            traceback.print_exc()
            return respond_custom({'error': str(e), 'class': type(e).__name__}, code=e.code)
        except Exception as e:
            traceback.print_exc()
            return respond_custom({'error': str(e), 'class': type(e).__name__}, code=500)
    return wrapper


def respond_custom(body, code=None):
    if code:
        return {
            'statusCode': code,
            'headers': {
                'Access-Control-Allow-Headers': 'Accept',
                'Access-Control-Allow-Origin': '*',  # Required for CORS support to work
                # Required for cookies, authorization headers with HTTPS
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE'
            },
            'body': body
        }
    return body


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
    @lambda_method_custom
    def delete(event, context, **kwargs):
        payload = kwargs.get("payload") # Access token payload ex: {'sub': '1234567890', 'name': 'John Doe', 'iat': 1516239022}
        ...
        return {"ok": 1}

    Args:
      f:
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
        auth_token = xs[0].get("headers")["Authorization"]

        if not auth_token:
            raise AppError(f'Unauthorized: Missing Token {auth_token}')

        token_method, auth_token = auth_token.split(' ')

        if not auth_token or token_method.lower() != 'bearer':
            print("Failing due to invalid token_method or missing auth_token")
            raise AppError(
                'Unauthorized: invalid token_method or missing auth_token')

        try:
            payload = jwt.decode(auth_token, JWT_SECRET, algorithms="HS256")

            permissions = payload["permissions"]
            verified = payload["verified"]

            if verified == False:
                raise AppError('Unauthorized: Unverified user')

            if permission:
                if permission not in permissions:
                    raise AppError('Unauthorized: Permission denied')

            return f(payload=payload, *xs, **kws)
        except Exception as e:
            print(f'Exception encountered: {e}')
            raise AppError(f'Unauthorized: {e}')

    return aux
