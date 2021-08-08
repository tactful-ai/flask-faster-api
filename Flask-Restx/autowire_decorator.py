import flask
from flask_restx import Api, Resource, fields, marshal_with, reqparse
from typing import List
from functools import wraps
import inspect


def autowire_decorator(path):
    def decorator(func):

        #model = get_model(func.__annotations__['return'])
        #path_params = get_path_params(path)
        signature = inspect.signature(func)
        parameters = dict(signature.parameters)
        parameters.pop('self')
        # for param in path_params:
        #    parameters.pop(param, None)

        #parser = get_parser(signature,parameters)

        # test_example
        model = api.model('Course', {
            'name': fields.String(required=True, description='The course name'),
            'duration': fields.Integer(required=True, description='The course duration'),
            'teachers': fields.List(fields.String, description='The course teachers'),
        })
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='The course name')

        @wraps(func)
        @api.expect(parser)
        @api.marshal_with(model)
        def wrapper(*args, **kwargs):
            args_parser = parser.parse_args()
            return func(*args, **args_parser, **kwargs)
        return wrapper
    return decorator
