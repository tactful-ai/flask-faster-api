"""The Autowire decorator is used to
replace @api.marshal_with decorator and
@api.expect decorator through supporting MyPy types."""
import inspect
from functools import wraps
from flask_restx import Api      # type: ignore
from flask_restx_square.model_api import create_model
from flask_restx_square.parser_api import get_parser


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
            print(line)
            if ':' in line:
                line = line.split(':')
                line[0] = line[0].strip()
                params_description[line[0]] = line[1]
    return params_description


def autowire(func):
    """The Autowire Decorator that wraps the function"""
    api = API.get_api()
    params_return = func.__annotations__
    model_name = func.__qualname__.split('.')[0]
    params_return = params_return.get('return')
    isprimitive = False
    params_return_des = {}
    if params_return is None:
        api_model = api.model(model_name, {})
    else:
        if (not isinstance(params_return, dict) and not inspect.isclass(params_return)):
            params_return = {'data': params_return}
            isprimitive = True
        if inspect.isclass(params_return):
            params_return_des = get_params_description(
                params_return.__doc__)
            params_return = params_return.__annotations__
        api_model = create_model(
            params_return, params_return_des)
        api_model = api.model(model_name, api_model)
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
