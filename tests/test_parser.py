import unittest
from inspect import Parameter
from typing import List, Tuple
from fastapi import Query, Body, Header, File
from werkzeug.datastructures import FileStorage
from flask_restx_square.parser_api import get_param_location, get_list_type, get_literal_tuple, get_param_type
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


parameters = {
    "id": Parameter('id', Parameter.KEYWORD_ONLY, default=Query(None), annotation=int),
    "name": Parameter('name', Parameter.KEYWORD_ONLY, default=Query(None), annotation=str),
    "teachers": Parameter('teachers', Parameter.KEYWORD_ONLY, default=Query(None), annotation=List[str]),
    "students_id": Parameter('students_id', Parameter.KEYWORD_ONLY, default=Body(None), annotation=List[int]),
    "option1": Parameter('option1', Parameter.KEYWORD_ONLY, default=Query(None), annotation=Literal[1, 5, 20]),
    "finish": Parameter('finish', Parameter.KEYWORD_ONLY, default=Query(None), annotation=bool),
    "duration": Parameter('duration', Parameter.KEYWORD_ONLY, default=Query(None), annotation=float),
    "student_data": Parameter('student_data', Parameter.KEYWORD_ONLY, default=Body(None), annotation=dict),
    "file1": Parameter('file1', Parameter.KEYWORD_ONLY, default=File(None), annotation=FileStorage),
    "option2": Parameter('option2', Parameter.KEYWORD_ONLY, default=Header(None),
                         annotation=Literal["course1", "course2", "course3"])
}

# test sub methods which used for create parser
# get_param_type()
# get_param_location()
# get_literal_tuple()
# get_list_type()


class TestParser(unittest.TestCase):
    def test_param_type(self):
        param_type = get_param_type(parameters["id"])
        self.assertEqual(param_type, int)

        param_type = get_param_type(parameters["teachers"])
        self.assertEqual(param_type, List[str])

        param_type = get_param_type(parameters["option1"])
        self.assertEqual(param_type, Literal[1, 5, 20])

        param_type = get_param_type(parameters["student_data"])
        self.assertEqual(param_type, dict)

        param_type = get_param_type(parameters["file1"])
        self.assertEqual(param_type, FileStorage)

    def test_param_location(self):
        location = get_param_location(parameters["id"])
        self.assertIsNotNone(location)
        self.assertNotEqual(location, 'form')
        self.assertEqual(location, 'args')

        location = get_param_location(parameters["students_id"])
        self.assertIsNotNone(location)
        self.assertNotEqual(location, 'headers')
        self.assertEqual(location, 'json')

        location = get_param_location(parameters["option2"])
        self.assertNotEqual(location, 'args')
        self.assertEqual(location, 'headers')

        location = get_param_location(parameters["name"])
        self.assertNotEqual(location, 'headers')
        self.assertEqual(location, 'args')

        location = get_param_location(parameters["file1"])
        self.assertEqual(location, 'files')

    def test_literal_param(self):
        res = get_literal_tuple(parameters["option1"].annotation)
        self.assertIsNotNone(res)
        self.assertNotEqual(res, tuple(("1", "5", "50")))
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
