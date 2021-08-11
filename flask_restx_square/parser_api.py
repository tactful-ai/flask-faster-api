import ast
from flask_restx import reqparse


def get_parser(signature, parameters) -> reqparse:
    parser = reqparse.RequestParser()
    location: str = 'args'  # default location -> 'args'

    for param in parameters.values():
        if param.name == "self":
            continue

        if str(param).find('Query') != -1:
            location = 'args'

        elif str(param).find('Body') != -1:
            location = 'form'

        elif str(param).find('Header') != -1:
            location = 'headers'

        elif str(param).find('Cookie') != -1:
            location = 'cookies'

        elif str(param).find('Path') != -1:
            continue
        else:
            location = 'args'

        annotation = parameters[str(param.name)].annotation

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
    s: int = str(annotation).index('[')
    e: int = str(annotation).index(']')
    str_list = str(annotation)[s + 1:e]

    res = ast.literal_eval(str_list)

    if res:
        return tuple(res)
