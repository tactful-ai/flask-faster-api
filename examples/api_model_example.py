from flask import Flask, request
from flask_restx import Api, Resource
from flask_restx_square import autowire, register_api
from flask_restx_square.model_api import create_model
from flask_restx_square.parser_api import get_parser
from data import courses

app = Flask(__name__)
api = Api(app)

register_api(api)

course_Model = dict({
    'id': int,
    'title': str,
    'duration': int
})


@api.route('/<int:id>')
class Course(Resource):
    @autowire
    def get(self, id) -> course_Model:
        for course in courses:
            if course['id'] == id:
                return course


if __name__ == '__main__':
    app.run(debug=True)
