from os import abort
from flask import Flask, request, make_response, jsonify
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from courses.repos import MemoryRepo
from courses.usecases.course_use_cases import CourseUseCases
from services.auth import encode_auth_token, requires_auth

Repo = MemoryRepo()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, version='1.0', title='Courses API',
    description='A simple Course API',
)

ns = api.namespace('courses', description='Course operations')
token_res = api.namespace('tokens', description='Tokens Operations')

course = api.model('Course', 
{
    'id': fields.String(readonly=True, description='Course unique identifier'),
    'name': fields.String(required=True, description='Course name'),
    'price': fields.Float(required=True, description='Course Price'),
    'duration': fields.String(required=True, description='Course Duration'),
    'students_count': fields.Integer(required=True, description='Number of Students')
})


@ns.route('/')
class CoursesList(Resource):
    '''Shows a list of all courses, and lets you POST to add new courses'''
    @ns.doc('list_courses')
    @ns.marshal_list_with(course)
    @requires_auth()
    def get(self,payload):
        try:
            query_params = request.args
            username = payload['username']
            coursesUC = CourseUseCases(Repo)
            courses_list = coursesUC.get_course_list(username, query_params)
            if courses_list is None or len(courses_list) <= 0:
                    return make_response(jsonify({
                        'error': 'No courses found'
                    }), 404)
                
            return [course.format() for course in courses_list]
        except Exception as e:
            api.abort(400)      

    @ns.doc('create_course')
    @ns.expect(course)
    @ns.marshal_with(course, code=201)
    @requires_auth()
    def post(self, payload):
        try:
            body = api.payload
            name = body['name']
            price = body['price']
            duration = body['duration']
            students_count = body['students_count']
            username = payload['username']
            
            coursesUC = CourseUseCases(Repo)
            result = coursesUC.create_course(username, name, price, duration, students_count)

            if result is None:
                api.abort(400)

            return result.format()
        except Exception as e:
            api.abort(500)

@ns.route('/<string:id>')
@ns.response(404, 'Course not found')
@ns.param('id', 'The course identifier')
class Course(Resource):
    @ns.doc('delete_course')
    @ns.response(204, 'Course deleted')
    @requires_auth()
    def delete(self, id, payload):
        try:
            username = payload['username']
            coursesUC = CourseUseCases(Repo)
            result = coursesUC.delete_course(username, id)
            if result is None or len(result) <= 0:
                return {
                    'error': 'Cannot delete Course'
                }, 400
            return {
                'message': "Deleted Successfully"
            }, 204
        except Exception as e:
            {
                "error" : "Message: {}, status 400 Bad request".format(e)
            }, 500


    @ns.expect(course)
    @ns.marshal_with(course)
    @requires_auth()
    def put(self, id, payload):
        try:
            body = api.payload
            name = body['name']
            price = body['price']
            duration = body['duration']

            username = payload['username']
            
            coursesUC = CourseUseCases(Repo)
            result = coursesUC.edit_course(username, id, name, price, duration)
            if result is None or (isinstance(result, list) and len(result) <= 0 ):
                return {
                    'error': 'Cannot edit Course'
                }, 400
            
            return result.format(), 200
        except Exception as e:
            return {
                "error" : "Message: {}, status 400 Bad request".format(e)
            }, 500

@ns.route('/enroll/<string:id>')
@ns.response(404, 'Course not found')
@ns.param('id', 'The course identifier')
class EnrollCourse(Resource):
    @ns.doc('enroll_course')
    @ns.marshal_with(course, code=201)
    @requires_auth()
    def post(self, id, payload):
        try:
            username = payload["username"]
            coursesUC = CourseUseCases(Repo)
            result = coursesUC.enroll_course(username, id)
            if result is None:
                return {
                    'error': 'Cannot enroll Course'
                }, 400       
            return {
                "message": "Enrolled",
                "course": result.format()
            }, 200
        except Exception as e:
            return {
                "error" : "Message: {}, status 400 Bad request".format(e)
            }, 500

@token_res.route('/')
class TokenResource(Resource):
    @token_res.doc('generate_token')
    def get(self):
        try:
            auth_token = encode_auth_token("random string", "geekahmed")
            if auth_token:
                return {
                            'success': True,
                            'message': 'Successfully generated.',
                            'auth_token': auth_token
                        }, 200
        except Exception as e:
            return {
                "error" : "Message: {}, status 400 Bad request".format(e)
            }, 400