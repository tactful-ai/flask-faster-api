#This is the unit test of the create_model function
#Author: Seif Ashraf

# Testing Methodology
# send return types example as a dict to the function to simulate the output of the annotations function
# let create_model() process input and get its output
# compare its output types with a sample model
# NOTE: typing.List needs comparing its type of fields.List with the create_model output type cuz idk why

from flask_restx_square import *
from flask_restx_square.model_api import create_model
from typing import Dict, List, Optional, OrderedDict, get_type_hints
from flask_restx import fields
from datetime import date
import unittest
from enum import Enum



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


#class for the model model to match it to the model generated 
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


descriptions = dict()

#the unit testing function
class TestModel(unittest.TestCase):
    def test_one(self):
        self.assertEqual(ModelMatcher(
            create_model(input, descriptions)), model)


if __name__ == '__main__':

    unittest.main()
