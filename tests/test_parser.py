import unittest
from inspect import Parameter
from typing import List
try:
    from typing import  Literal
except:
    from typing_extensions import Literal
from fastapi import Query, Body, Header 
from flask_restx_square.parser_api import get_param_location, get_list_type, get_literal_tuple

parameters = {
    "id": Parameter('id', Parameter.KEYWORD_ONLY, default=Query(None), annotation=int),
    "name": Parameter('name', Parameter.KEYWORD_ONLY, default=Query(None), annotation=str),
    "teachers": Parameter('teachers', Parameter.KEYWORD_ONLY, default=Query(None), annotation=List[str]),
    "students_id": Parameter('students_id', Parameter.KEYWORD_ONLY, default=Body(None), annotation=List[int]),
    "option1": Parameter('option1', Parameter.KEYWORD_ONLY, default=Query(None), annotation=Literal[1, 5, 20]),
    "finish": Parameter('finish', Parameter.KEYWORD_ONLY, default=Query(None), annotation=bool),
    "duration": Parameter('duration', Parameter.KEYWORD_ONLY, default=Query(None), annotation=float),
    "option2": Parameter('option2', Parameter.KEYWORD_ONLY, default=Header(None),
                         annotation=Literal["course1", "course2", "course3"])
}

# test sub methods which used for create parser
# get_param_location()
# get_literal_tuple()
# get_list_type()


class TestParser(unittest.TestCase):
    def test_param_location(self):
        location = get_param_location(parameters["id"])
        self.assertIsNotNone(location)
        self.assertNotEqual(location, 'sss')
        self.assertNotEqual(location, 'form')
        self.assertEqual(location, 'args')

        location = get_param_location(parameters["students_id"])
        self.assertIsNotNone(location)
        self.assertNotEqual(location, 'headers')
        self.assertNotEqual(location, "true")
        self.assertEqual(location, 'form')

        location = get_param_location(parameters["option2"])
        self.assertNotEqual(location, 'args')
        self.assertEqual(location, 'headers')

        location = get_param_location(parameters["name"])
        self.assertNotEqual(location, 'headers')
        self.assertEqual(location, 'args')

    def test_literal_param(self):

        res = get_literal_tuple(parameters["option1"].annotation)
        self.assertIsNotNone(res)
        self.assertNotEqual(res, tuple(("1", "5", "50")))
        self.assertNotEqual(res, tuple((-1, -5, -20)))
        self.assertEqual(res, tuple((1, 5, 20)))

        res = get_literal_tuple(parameters["option2"].annotation)
        self.assertIsNotNone(res)
        self.assertNotEqual(res, tuple(("xx", "yy", "zz")))
        self.assertNotEqual(res, tuple((55, -8888)))
        self.assertEqual(res, tuple(("course1", "course2", "course3")))

    def test_list_typeof(self):
        type_ = get_list_type(parameters["teachers"].annotation)
        self.assertNotEqual(type_, int)
        self.assertNotEqual(type_, complex)
        self.assertIsNotNone(type_)
        self.assertEqual(type_, str)

        type_ = get_list_type(parameters["students_id"].annotation)
        self.assertNotEqual(type_, str)
        self.assertNotEqual(type_, float)
        self.assertIsNotNone(type_)
        self.assertEqual(type_, int)


if __name__ == '__main__':
    unittest.main()
