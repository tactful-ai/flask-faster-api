from typing import Callable
from flask_restx import reqparse
import inspect


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

        # print("name : {}".format(param.name))
        # print("param : {}".format(param))
        # print("location : {}".format(location))
        # print("default : {}".format(param.default))
        # print("annotation : {}\n".format(parameters[str(param.name)].annotation))

        parser.add_argument(str(param.name), type=parameters[str(param.name)].annotation,
                            location=location)

    return parser
