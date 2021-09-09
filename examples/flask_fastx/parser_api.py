""" This module enable to add parameters to be parsed """

import typing
from flask_restx import reqparse, model  # type: ignore
from werkzeug.datastructures import FileStorage

from flask_fastx.params import Param
from examples.flask_fastx.model_api import create_model
# pylint: disable=missing-function-docstring


class ApiPayloadModel:
    """The API Payload Model"""
    def __init__(self):
        self.model_parameters = {}
        self.payload_model = None

    def set_model(self, model_):
        self.payload_model = model_

    def set_model_parameters(self, params):
        self.model_parameters = params

    def get_model(self):
        return self.payload_model


payloadModel = ApiPayloadModel()

python2type = {
    'str': str,
    'bool': bool,
    'int': int,
    'float': float,
    'relation': None,
    'list': list,
    'dict': dict,
    'KT': dict,
    'datetime': str,
    'time': str,
    'any': str,
    'FileStorage': FileStorage
}

LocationToRestX = {
    'Query': 'args',
    'Body': 'json',
    'Form': 'form',
    'Header': 'headers',
    'Cookie': 'cookies',
    'File': 'files',
    'Path': 'path',
}


def get_parser(parameters, api) -> reqparse:
    """Parse all parameters which taken from the provided auto-wire decorator and
    return the results as a parser."""
    parser = reqparse.RequestParser()
    param_default: Param
    for param in parameters.values():
        location: str = get_param_location(param)
        field_type = param.annotation
        param_default = param.default
        if location == 'path':
            continue
        try:
            field_type = get_parser_type(field_type, api)
            if isinstance(field_type, (model.Model, type(typing.List[model.Model]))):
                continue
            if not field_type:
                raise Exception(f"Cannot parse {str(param.name)} of type {field_type.__name__}"
                                f" to a Fastx Type")
        except Exception as error:
            raise Exception(f"Cannot parse {str(param.name)} of type {field_type.__name__}"
                            f" to a Fastx type") from error

        parser.add_argument(str(param.name), type=field_type, location=location,
                            default=param_default.default, help=param_default.help,
                            required=param_default.required, ignore=param_default.ignore,
                            choices=param_default.choices, action=param_default.action,
                            nullable=param_default.nullable, operators=param_default.operators,
                            store_missing=param_default.store_missing, trim=param_default.trim,
                            case_sensitive=param_default.case_sensitive)
    return parser


def get_parser_type(attr_type, api=None):
    """ return attribute type to parse"""
    field_type = None
    if hasattr(attr_type, '__origin__'):
        field_type = get_generic_type(attr_type, api)
    elif attr_type.__name__ in python2type:
        field_type = python2type[attr_type.__name__]
    else:
        field_type = complex_to_payload(attr_type, api)
    return field_type


def complex_to_payload(attr_type, api):
    """convert complex type (user define class) to model and attach it to api and parser it
     to payload model at body"""
    payload_model = None
    if hasattr(attr_type, '__annotations__'):
        params = attr_type.__annotations__
        payload_model = create_model(api, params, {})
        payload_model = api.model(str(attr_type.__name__), payload_model)
        payloadModel.set_model_parameters(params)
        payloadModel.set_model(payload_model)
    return payload_model


def get_generic_type(attr_type, api):
    """ return type of generic attribute"""
    generic_type = attr_type.__origin__
    generic_args = attr_type.__args__ if attr_type.__args__ else None
    generic_arg = generic_args[0] if generic_args else None
    generic_type_mapped = None
    field_type = None

    if generic_type in [typing.Union, typing.Optional]:
        if len(generic_args) == 2 and generic_args[1] == type(None):
            return get_parser_type(generic_args[0], api)
        raise Exception(f"Union types are not supported in Fastx types, found {generic_args}")

    generic_type_mapped = generic_type.__name__
    if generic_type_mapped and len(generic_args) == 1:
        field_arg = get_parser_type(generic_arg, api)
        if field_arg:
            if generic_type == list and isinstance(field_arg, model.Model):
                payloadModel.set_model([field_arg])
                field_type = typing.List[type(field_arg)]
            else:
                field_type = attr_type
    else:
        raise Exception(f"Unknown Generic type {generic_type}")
    return field_type


def get_payload_model():
    """return payload Model"""
    return payloadModel.get_model()


def get_param_location(param) -> str:
    """ return parameter location in rest_x ."""
    for location, value in LocationToRestX.items():
        if str(param).find(location) != -1:
            return value

    return LocationToRestX['Path']
