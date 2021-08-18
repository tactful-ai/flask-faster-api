from typing import Dict, List, Optional, OrderedDict, get_type_hints
from flask_restx import fields  # type: ignore
from datetime import date

# class for the model model to match it to the model generated


class ModelMatcher:
    model: dict

    def __init__(self, model):
        self.model = model

    def __eq__(self, other):

        return type(self.model['id']) == other['id'] and \
            type(self.model['title']) == other['title'] and \
            type(self.model['duration']) == other['duration'] and \
            type(self.model['teachers']) == type(other['teachers']) and \
            type(self.model['intlist']) == type(other['intlist']) and \
            type(self.model['bool']) == other['bool'] and \
            type(self.model['float']) == other['float'] and \
            type(self.model['dict']) == other['dict']


model = {
    'id': fields.Integer,
    'title': fields.String,
    'duration': fields.Integer,
    'teachers': fields.List(fields.String),
    'intlist': fields.List(fields.Integer),
    'bool': fields.Boolean,
    'float': fields.Float,
    'dict': fields.Raw,
}


input = {
    'id': "<class 'int'>",
    'title': "<class 'str'>",
    'duration': "<class 'int'>",
    'teachers': "typing.List[str]",
    'intlist': "typing.List[int]",
    'bool': "<class 'bool'>",
    'float': "<class 'float'>",
    'dict': "<class 'dict'>",
}
