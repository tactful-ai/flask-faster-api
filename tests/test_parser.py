import unittest

from flask import Flask
from flask_restx import Api
from inspect import Parameter
from typing import List

from examples.flask_fastx.model_api import create_model
from examples.flask_fastx.params import Query, Body, File
from werkzeug.datastructures import FileStorage
from examples.flask_fastx.parser_api import get_parser_type


class CourseModel:
    name: str
    course_id: int
    students: List[str]


parameters = {
    "id": Parameter('id', Parameter.KEYWORD_ONLY, default=Query(), annotation=int),
    "name": Parameter('name', Parameter.KEYWORD_ONLY, default=Query(), annotation=str),
    "teachers": Parameter('teachers', Parameter.KEYWORD_ONLY, default=Body(), annotation=List[str]),
    "course": Parameter('course', Parameter.KEYWORD_ONLY, default=Body(), annotation=CourseModel),
    "courses": Parameter('courses', Parameter.KEYWORD_ONLY, default=Body(), annotation=List[CourseModel]),
    "finish": Parameter('finish', Parameter.KEYWORD_ONLY, default=Query(), annotation=bool),
    "duration": Parameter('duration', Parameter.KEYWORD_ONLY, default=Query(), annotation=float),
    "student_data": Parameter('student_data', Parameter.KEYWORD_ONLY, default=Body(), annotation=dict),
    "file1": Parameter('file1', Parameter.KEYWORD_ONLY, default=File(), annotation=FileStorage),

}

# test sub methods which used for create parser
# get_parser_type()


app = Flask(__name__)
api = Api(app)

api_model = create_model(api, parameters["course"].annotation.__annotations__, {})
api_model = api.model("CourseModel", api_model)


class TestParser(unittest.TestCase):
    def test_param_type(self):
        param_type = get_parser_type(parameters["id"].annotation, api)
        self.assertEqual(param_type, int)

        param_type = get_parser_type(parameters["teachers"].annotation, api)
        self.assertEqual(param_type, List[str])

        param_type = get_parser_type(parameters["course"].annotation, api)
        self.assertEqual(type(param_type), type(api_model))

        param_type = get_parser_type(parameters["student_data"].annotation, api)
        self.assertEqual(param_type, dict)

        param_type = get_parser_type(parameters["file1"].annotation, api)
        self.assertEqual(param_type, FileStorage)


if __name__ == '__main__':
    unittest.main()
