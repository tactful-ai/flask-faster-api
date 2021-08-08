import flask
from flask_restx import Api, Resource, fields, marshal_with, reqparse
from typing import List
from functools import wraps
import inspect


def autowire_decorator(path):
    def decorator(func):

        params_return = func.__annotations__
        modelName = func.__qualname__.split('.')[0]
        # isPrimitive, api_model = create_model(
        #    params_return.get('return'), modelName)
        # if(not isPrimitive):
        #    api_model = api.model(modelName, api_model)
        path_params = ExtractPathParams(path)
        signature = inspect.signature(func)

        parameters = dict(signature.parameters)
        parameters.pop('self')

        for param in path_params:
            parameters.pop(param, None)
        parser = get_parser(signature, parameters)

        @wraps(func)
        @api.expect(parser)
        @api.marshal_with(api_model)
        def wrapper(*args, **kwargs):
            args_parser = parser.parse_args()
            return func(*args, **args_parser, **kwargs)
        return wrapper
    return decorator
