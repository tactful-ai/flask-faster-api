import jwt
from functools import wraps
from flask import request, jsonify , make_response

SECRET_KEY = "thisisthesecretkey"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/courses?token=alshfjfjdklsfj89549834ur

        if not token:
            return {'message': 'Token is missing!'}, 403

        try:
            data = jwt.decode(token, SECRET_KEY)
        except:
            return {'message': 'Token is invalid!'}, 403

        return f(*args, **kwargs)

    return decorated
