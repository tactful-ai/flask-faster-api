from flask import request, abort
from functools import wraps
from jose import jwt
import datetime

black_list_tokens = []
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)

    if not auth_header:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or not header_parts:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be in the format'
                           ' Bearer token'}, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'}, 401)

    return header_parts[1]




def encode_auth_token(secret_key, username):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'username': username
        }
        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(secret_key, auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret_key)
        is_blacklisted_token = auth_token in black_list_tokens
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def requires_auth():
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = decode_auth_token("random string", auth_token=token)
            return f(payload, *args, **kwargs)
        return wrapper

    return requires_auth_decorator