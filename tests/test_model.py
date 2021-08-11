from flaskresty import *
from flaskresty.model_api import create_model
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

class ModelMatcher:
    model: dict

    def __init__(self, model):
        self.model = model

    def __eq__(self, other):
        return self.model['id'] == other['id'] and \
                self.model['title'] == other['title'] and \
                self.model['duration'] == other['duration'] and \
                type(self.model['teachers']) == type(other['teachers']) and \
                type(self.model['intlist']) == type(other['intlist']) and \
                self.model['bool'] == other['bool'] and \
                self.model['float'] == other['float'] and \
                self.model['dict'] == other['dict']
        
        


class TestModel(unittest.TestCase):        
        def test_one(self):
            self.assertEqual(ModelMatcher(create_model(input)), model)
            
            

    
if __name__ == '__main__':
    
    unittest.main()
      
    
        