"""The Autowire decorator is used to
replace @api.marshal_with decorator and
@api.expect decorator through supporting MyPy types."""
import inspect
from functools import wraps
from flask_restx import Api
from flaskresty.model_api import create_model
from flaskresty.path_param import ExtractPathParams
from flaskresty.parser_api import get_parser
api = Api()


def register_api(api_main):
    """Register The Main App Api"""
    global api
    api = api_main


def autowire_decorator(path):
    """The Autowire Decorator with a path parameter (the url/endpoint)"""
    def decorator(func):
        """The decorator that wraps the function"""
        params_return = func.__annotations__
        model_name = func.__qualname__.split('.')[0]
        params_return = params_return.get('return')
        isprimitive = False
        if params_return is None:
            api_model = api.model(model_name, {})
        else:
            if not isinstance(params_return, dict):
                params_return = {'data': params_return}
                isprimitive = True
            api_model = create_model(
                params_return)
            api_model = api.model(model_name, api_model)
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
            if isprimitive:
                return {'data': func(*args, **args_parser, **kwargs)}
            return func(*args, **args_parser, **kwargs)
        return wrapper
    return decorator
