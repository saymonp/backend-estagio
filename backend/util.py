import traceback
import functools
import json
import jwt

from .errors import AppError
from .env import JWT_SECRET


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
def auth(f, permission):
    def aux(*xs, **kws):
        print(xs[0]["header"])
        header = json.loads(xs[0]["header"])
        auth_token = header["authorization"]

        if not auth_token:
            raise Exception('Unauthorized')

        token_method, auth_token = auth_token.split(' ')

        if not auth_token or token_method.lower() != 'bearer':
            print("Failing due to invalid token_method or missing auth_token")
            raise Exception('Unauthorized')
        
        try:
            payload = jwt.decode(auth_token, JWT_SECRET)
            # Checa permissões
            print(payload)
            return payload
        except Exception as e:
            print(f'Exception encountered: {e}')
            raise Exception('Unauthorized')
        
        return f(*xs, **kws)
        
    return aux