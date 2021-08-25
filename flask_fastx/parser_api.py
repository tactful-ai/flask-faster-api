""" This module enable to add parameters to be parsed """

import ast
from flask_restx import reqparse  # type: ignore
from flask_fastx.params import Param

LocationToRestX = {
    'Query': 'args',
    'Body': 'json',
    'Form': 'form',
    'Header': 'headers',
    'Cookie': 'cookies',
    'File': 'files',
    'Path': 'path',
}


def get_parser(parameters) -> reqparse:
    """
    Parse all parameters which taken from the provided auto-wire decorator and
    return the results as a parser.
    """
    parser = reqparse.RequestParser()
    for param in parameters.values():
        location: str = get_param_location(param)
        param_type = get_param_type(param)
        default = None
        if location == 'path':
            continue
        param_default: Param
        param_default = param.default
        if param_default.default:
            default = param_default.default
        if str(param_type).find('typing.List') != -1:
            list_type = get_list_type(param_type)
            parser.add_argument(str(param.name), type=list_type, action='split',
                                location=location, default=default)

        elif str(param_type).find('typing.Literal') != -1:
            res = get_literal_tuple(str(param_type))
            if res and len(res) > 0:
                parser.add_argument(str(param.name), type=type(res[0]), choices=res,
                                    location=location, default=default)
        else:
            parser.add_argument(str(param.name), type=param_type,
                                location=location, default=default)

    return parser


def get_param_type(param):
    """ return parameter type """
    return param.annotation


def get_literal_tuple(param_type):
    """
    get literal option from annotation string and return result in tuple.
    """
    s_index: int = str(param_type).index('[')
    e_index: int = str(param_type).index(']')
    str_list = str(param_type)[s_index + 1:e_index]

    res = ast.literal_eval(str_list)
    if res:
        return tuple(res)

    return None


def get_param_location(param) -> str:
    """
    take a param and return his location in rest_x .
    """
    for location, value in LocationToRestX.items():
        if str(param).find(location) != -1:
            return value

    return LocationToRestX['Path']


def get_list_type(param_type):
    """
    return type of given list
    """
    if str(param_type).find('[str]') != -1:
        return str

    if str(param_type).find('[int]') != -1:
        return int

    if str(param_type).find('[float]') != -1:
        return float

    if str(param_type).find('[bool]') != -1:
        return bool

    return str
