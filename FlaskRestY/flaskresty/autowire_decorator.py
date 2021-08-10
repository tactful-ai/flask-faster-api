from flask_restx import Api
from functools import wraps
import inspect
from .model_api import create_model
from .path_param import ExtractPathParams
from .parser_api import get_parser
api = Api()


def register_api(api_main):
    global api
    api = api_main


def autowire_decorator(path):
    def decorator(func):

        params_return = func.__annotations__
        modelName = func.__qualname__.split('.')[0]
        params_return = params_return.get('return')
        isPrimitive = False
        if(params_return == None):
            api_model = api.model(modelName, {})
        else:
            if(type(params_return) != dict):
                params_return = {'data': params_return}
                isPrimitive = True
            api_model = create_model(
                params_return)
            api_model = api.model(modelName, api_model)
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
            if(isPrimitive):
                return {'data': func(*args, **args_parser, **kwargs)}
            else:
                return func(*args, **args_parser, **kwargs)
        return wrapper
    return decorator
