""" This module enable to add parameters to be parsed """

import ast
from flask_restx import reqparse  # type: ignore


def get_parser(parameters) -> reqparse:
    """
    Parse all parameters which taken from the provided auto-wire decorator and
    return the results as a parser.

    :param parameters:
    :return: parser
    """
    parser = reqparse.RequestParser()

    for param in parameters.values():
        location: str = get_location(param)
        annotation = parameters[str(param.name)].annotation

        if location == 'Path':
            continue
        if str(annotation).find('typing.List[str]') != -1:
            parser.add_argument(str(param.name), type=str, action='append',
                                location=location)
        elif str(annotation).find('typing.List[int]') != -1:
            parser.add_argument(str(param.name), type=int, action='append',
                                location=location)

        elif str(annotation).find('typing.List[float]') != -1:
            parser.add_argument(str(param.name), type=float, action='append',
                                location=location)
        elif str(annotation).find('typing.Literal') != -1:

            res = get_literal_tuple(str(annotation))
            if res and len(res) > 0:
                parser.add_argument(str(param.name), type=type(res[0]), required=True, choices=res,
                                    location=location)
        else:
            parser.add_argument(str(param.name), type=parameters[str(param.name)].annotation,
                                location=location)

    return parser


def get_literal_tuple(annotation):
    """
    get literal option from annotation string and return result in tuple.
    """
    s_index: int = str(annotation).index('[')
    e_index: int = str(annotation).index(']')
    str_list = str(annotation)[s_index + 1:e_index]

    res = ast.literal_eval(str_list)
    if res:
        return tuple(res)

    return None


def get_location(param) -> str:
    """
    take param and return his location.
    """
    if str(param).find('Query') != -1:
        return 'args'

    if str(param).find('Body') != -1:
        return 'form'

    if str(param).find('Header') != -1:
        return 'headers'

    if str(param).find('Cookie') != -1:
        return 'cookies'

    if str(param).find('Path') != -1:
        return 'Path'

    return 'args'
