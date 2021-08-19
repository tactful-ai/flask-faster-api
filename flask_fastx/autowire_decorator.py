"""The Autowire decorator is used to
replace @api.marshal_with decorator and
@api.expect decorator through supporting MyPy types."""
import inspect
from functools import wraps
from flask_restx import Api      # type: ignore
from flask_fastx.model_api import create_model
from flask_fastx.parser_api import get_parser

# pylint: disable=C0207

class ApiDecorator():
    """The API Decorator"""

    def __init__(self) -> None:
        """Initialize the API decorator"""
        self.api = Api()

    def set_api(self, api: Api) -> None:
        """Set the API"""
        self.api = api

    def get_api(self) -> Api:
        """Get the API"""
        return self.api


API = ApiDecorator()


def register_api(api_main):
    """Register The Main App Api"""
    API.set_api(api_main)


def get_params_description(doc):
    """Get the parameters description from the docstring"""
    params_description = {}
    if doc is not None:
        doc = doc.split('\n')
        for line in doc:
            if ':' in line:
                line = line.split(':')
                line[0] = line[0].strip()
                params_description[line[0]] = line[1]
    return params_description


def autowire(func):
    """The Autowire Decorator that wraps the function"""
    api = API.get_api()
    model_name = func.__qualname__.split('.')[0]
    params_return = func.__annotations__
    params_return = params_return.get('return')
    isprimitive = False
    params_return_des = {}
    if params_return is None:
        api_model = api.model(model_name, {})
    else:
        if check_class_dict(params_return):
            params_return = {'data': params_return}
            isprimitive = True
        if hasattr(params_return, '__annotations__'):
            params_return_des = get_params_description(
                params_return.__doc__)
            params_return = params_return.__annotations__
        api_model = create_model(
            params_return, params_return_des)
        api_model = api.model(str(func.__name__)+model_name, api_model)
    signature = inspect.signature(func)
    parameters = dict(signature.parameters)
    parameters.pop('self')

    parser = get_parser(parameters)

    @wraps(func)
    @api.expect(parser)
    @api.marshal_with(api_model)
    def wrapper(*args, **kwargs):
        args_parser = parser.parse_args()
        if isprimitive:
            return {'data': func(*args, **args_parser, **kwargs)}
        return func(*args, **args_parser, **kwargs)
    return wrapper


def check_class_dict(param_type):
    """Check the class dict"""
    dict_type = str(param_type).replace("<", "")
    dict_type = dict_type.replace(">", "")
    dict_type = dict_type.split(" ")[-1]
    check_dect = dict_type != "dict" and not isinstance(param_type, dict)
    if not hasattr(param_type, '__annotations__') and check_dect:
        return True
    return False
