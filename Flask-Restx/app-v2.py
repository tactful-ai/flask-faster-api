from flask import Flask, Blueprint, jsonify, request
from flask_restx import Api, Resource, fields, marshal_with, reqparse
from typing import List
from functools import wraps

from werkzeug import Request
from auth import auth, encode_jwt


app = Flask(__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
blueprint = Blueprint('api', __name__, url_prefix='/api/v2')

api = Api(blueprint, version='2.0', title='Courses API',
          authorization=authorizations)
app.register_blueprint(blueprint)

courses_ns = api.namespace('courses', description='Courses Endpoints')
auth_ns = api.namespace('auth', description='Authentication Endpoints')
course = api.model('Course', {
    'name': fields.String(required=True, description='The course name'),
    'duration': fields.Integer(required=True, description='The course duration'),
    'teachers': fields.List(fields.String, description='The course teachers'),
})


class CourseDAO(object):
    counter = 0
    courses = []

    @staticmethod
    def get(id):
        for course in CourseDAO.courses:
            if course['id'] == id:
                return course
        api.abort(404, "Course {} doesn't exist".format(id))

    @staticmethod
    def create(data):
        course = data
        course['id'] = CourseDAO.counter = CourseDAO.counter + 1
        CourseDAO.courses.append(course)
        return course

    @staticmethod
    def update(id, data):
        course = CourseDAO.get(id)
        course.update(data)
        return course

    @staticmethod
    def delete(id):
        course = CourseDAO.get(id)
        CourseDAO.courses.remove(course)


def autowire_decorator(func):
    params = func.__annotations__

    @wraps(func)
    def path_wrapper(*args, **kwargs):
        return args[0]
    resource = path_wrapper.__qualname__.split('.')[0]
    # todo-path params

    # return_params=params['return']
    #model = get_model(return_params)
    params.pop('return', None)

    #parser = get_parser(params)

    #test_example
    model = api.model('Course', {
        'name': fields.String(required=True, description='The course name'),
        'duration': fields.Integer(required=True, description='The course duration'),
        'teachers': fields.List(fields.String, description='The course teachers'),
    })
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='The course name')
    parser.add_argument('duration', type=int, help='The course duration')
    parser.add_argument('teachers', type=List[str], help='The course teachers')

    @wraps(func)
    @api.expect(parser)
    @api.marshal_with(model)
    def wrapper(*args, **kwargs):
        args_parser = parser.parse_args()
        return func(*args, *args_parser.values(), **kwargs)
    return wrapper


@ api.route('/')
class CourseList(Resource):
    @ courses_ns.doc('list_courses', security='apikey')
    # @auth
    @ courses_ns.marshal_list_with(course)
    def get(self):
        return CourseDAO.courses

    @ courses_ns.doc('create_course', security='apikey')
    @ autowire_decorator
    def post(self, name: str, duration: int, teachers: List[str]) -> course:
        course_data = {
            'name': name,
            'duration': duration,
            'teachers': teachers
        }
        return CourseDAO.create(course_data), 201


@ api.route('/<int:id>')
class Course(Resource):
    @ courses_ns.doc('get_course', security='apikey')
    # @auth
    # @courses_ns.marshal_with(course)
    def get(self, id):
        return CourseDAO.get(id)

    @ courses_ns.doc('update_course', security='apikey')
    # @auth
    @ courses_ns.expect(course)
    @ courses_ns.marshal_with(course)
    def put(self, id):
        return CourseDAO.update(id, api.payload)

    @ courses_ns.doc('delete_course', security='apikey')
    # @auth
    @ courses_ns.response(204, 'Course deleted')
    def delete(self, id):
        CourseDAO.delete(id)
        return '', 204


@ auth_ns.route('/login')
class Login(Resource):
    @ auth_ns.doc('login')
    @ auth_ns.response(200, 'Success')
    @ auth_ns.expect({'username': fields.String, 'password': fields.String})
    def post(self):
        username = api.payload['username']
        password = api.payload['password']
        if username == "admin" and password == "admin":
            return {'token': encode_jwt(username)}
        return {'message': 'Invalid username or password'}, 401


if __name__ == '__main__':
    app.run(debug=True)
