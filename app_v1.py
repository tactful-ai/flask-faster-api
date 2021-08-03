from flask import Flask, make_response, jsonify, request
from flask_restful import Api, reqparse
import jwt
import datetime
from data.Courses_ import courses
from data.Students_ import students
from helper.auth import token_required

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['X-Api-Key'] = 'asoidewfoef'

course_args = reqparse.RequestParser()
course_args.add_argument("name", type=str)
course_args.add_argument("duration", type=str)
course_args.add_argument("teachers", action='append')


@app.route("/courses", methods=["GET"])
@token_required
def get():
    return jsonify({'Courses ': courses}), 200


@app.route("/courses", methods=["POST"])
@token_required
def post_course():
    args = course_args.parse_args()
    course = {"name": args["name"],
              "course_id": len(courses),
              "duration": args["duration"],
              "teachers": args["teachers"]}
    courses.append(course)
    return jsonify({'Message': "Successful Added"}), 200


@app.route("/courses/<int:course_id>", methods=["PUT"])
@token_required
def put(course_id):
    if course_id <= len(courses):
        args = course_args.parse_args()
        course = {"name": args["name"],
                  "course_id": course_id,
                  "duration": args["duration"],
                  "teachers": args["teachers"]}
        courses[course_id] = course
        return jsonify({"Updated ": courses[course_id]}), 200
    else:
        return jsonify({"Message": "course id not found"}), 404


@app.route("/courses/<int:course_id>", methods=["DELETE"])  # here authenticate with token param and header
@token_required
def delete_course(course_id):
    if course_id <= len(courses):
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == app.config['X-Api-Key']:
            courses.remove(courses[course_id])
            return jsonify({'Message': "Successful Deleted"}), 200
        else:
            return jsonify({"Message": "ERROR: Unauthorized"}), 401
    else:
        return jsonify({"Message": "course id not found"}), 404


@app.route("/")
def index():
    return "Here Courses api"


@app.route('/gettoken')
def login():
    auth = request.authorization  # username = anthony, password = secret
    if auth and auth.password == 'secret':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


student_args = reqparse.RequestParser()
student_args.add_argument("name", type=str, help="name is required.", required=True)
student_args.add_argument("course_id", type=str, help="course id is required.", required=True)


@app.route('/enroll', methods=["POST"])
@token_required
def enrol():
    try:
        args = student_args.parse_args()
        student = {
            "name": args["name"],
            "course_id": args["course_id"]
        }
        students.append(student)
        return jsonify({"Message:": "Successfully Enrolled", "Students": students}), 200
    except Exception as e:
        return make_response(jsonify({"Error": ": {}, status 400 Bad request".format(e)}), 500)


if __name__ == '__main__':
    app.run(debug=True)
