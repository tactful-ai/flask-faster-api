from flask import request
from functools import wraps
import jwt


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if auth_jwt(request.headers.get('Authorization'))['payload']:
            return func(*args, **kwargs)
        headerToken = request.headers.get('token')
        cookieToken = request.cookies.get('token')
        queryToken = request.args.get('token')
        if not headerToken and not cookieToken and not queryToken:
            return {'message': 'Token is missing'}, 401
        if headerToken != 'secret' and cookieToken != 'secret' and queryToken != 'secret':
            return {'message': 'Invalid Token'}, 401
        return func(*args, **kwargs)
    return wrapper


def auth_jwt(token):
    try:
        payload = jwt.decode(token, 'secret')
        return {'payload': payload['sub']}
    except jwt.ExpiredSignatureError:
        return {'payload': None, 'message': 'Signature expired'}
    except jwt.InvalidTokenError:
        return {'payload': None, 'message': 'Invalid token'}
