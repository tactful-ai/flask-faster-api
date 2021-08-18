from typing import List
from flask import Flask, request
from flask_restx import Api, Resource
from flask_fastx import autowire, register_api
from flask_fastx.model_api import create_model
from flask_fastx.parser_api import get_parser
from .data import courses

app = Flask(__name__)
api = Api(app)

# register_api(api)

# @api.route('/<int:id>')
# class Course(Resource):
#     @autowire
#     def get(self, int: id) -> int:
#         for course in courses:
#             if course['id'] == id:
#                 return course


if __name__ == '__main__':
    app.run(debug=True)
