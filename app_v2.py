from flask import Flask, make_response, jsonify, request
from flask_restx import Resource, Api
from flask_restful import reqparse
import jwt
import datetime
from data.Courses_ import courses
from data.Students_ import students
from helper.auth import token_required


app = Flask(__name__)
api = Api(app, version='2.0', title='Courses API v2', )
ns = api.namespace('courses', description='Course CRUD operations')
lg = api.namespace('login', description='get access token')

app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['X-Api-Key'] = 'asoidewfoef'

course_args = reqparse.RequestParser()
course_args.add_argument("name", type=str)
course_args.add_argument("duration", type=str)
course_args.add_argument("teachers", action='append')


@lg.route('/')
class Login(Resource):
    def get(self):
        auth = request.authorization  # username = anthony, password = secret

        if auth and auth.password == 'secret':
            token = jwt.encode(
                {'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@ns.route('/')
class Courses(Resource):
    @token_required
    def get(self):
        return {'Courses ': courses}, 200

    @token_required
    def post(self):
        args = course_args.parse_args()
        course = {"name": args["name"],
                  "course_id": len(courses),
                  "duration": args["duration"],
                  "teachers": args["teachers"]}
        courses.append(course)
        return {'Message': "Successful Added"}, 200


@ns.route("/<int:course_id>")
class Courses(Resource):
    @token_required
    def put(self, course_id):
        if course_id <= len(courses):
            args = course_args.parse_args()
            course = {"name": args["name"],
                      "course_id": course_id,
                      "duration": args["duration"],
                      "teachers": args["teachers"]}
            courses[course_id] = course
            return {"Updated ": courses[course_id]}, 200
        else:
            return {"Message": "course id not found"}, 404


@ns.route("/<int:course_id>")  # here authenticate with token param and header
class Courses(Resource):
    @token_required
    def delete(self, course_id):
        if course_id <= len(courses):

            headers = request.headers
            auth = headers.get("X-Api-Key")
            if auth == app.config['X-Api-Key']:
                courses.remove(courses[course_id])
                return {'Message': "Successful Deleted"}, 200
            else:
                return {"Message": "ERROR: Unauthorized"}, 401
        else:
            return {"Message": "course id not found"}, 404


student_args = reqparse.RequestParser()
student_args.add_argument("name", type=str, help="name is required.", required=True )
student_args.add_argument("course_id", type=str, help="course id is required.", required=True)


@ns.route('/enroll')
class CourseEnroll(Resource):
    @token_required
    def post(self):
        try:
            args = student_args.parse_args()
            student = {
                "name": args["name"],
                "course_id": args["course_id"]
            }
            students.append(student)
            return {"Message:": "Successfully Enrolled", "Students": students}, 200
        except Exception as e:
            return {"Error": ": {}, status 400 Bad request".format(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)

