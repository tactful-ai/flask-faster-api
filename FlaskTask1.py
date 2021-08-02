from flask import Flask, render_template, make_response, jsonify, request
from flask_restful import Resource, Api, reqparse
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
api = Api(app)

courses = [
    {'name': "Python Programming Course",
     'course_id': "0",
     'duration': "10",
     'teachers': ['ahmed', 'omar', 'mahmoud']
     },

    {'name': "Java Programming Course",
     'course_id': "1",
     'duration': "25",
     'teachers': ['mohamed', 'ahmed']
     },

    {'name': "C++ Programming Course",
     'course_id': "2",
     'duration': "15",
     'teachers': ['ahmed', 'omar', 'mahmoud']
     }

]

app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['X-Api-Key'] = 'asoidewfoef'


course_post_args = reqparse.RequestParser()
course_post_args.add_argument("name", type=str, help="name is required.", required=True)
course_post_args.add_argument("duration", type=str, help="duration  is required.", required=True)
course_post_args.add_argument("teachers", type=list, help="teachers  is required.", required=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/courses?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route("/courses", methods=["GET"])
@token_required
def get():
    return jsonify({'Courses': courses}), 200


@app.route("/courses", methods=["POST"])
@token_required
def post_course():
    args = course_post_args.parse_args()
    course = {"name": args["name"],
              "course_id": len(courses),
              "duration": args["duration"],
              "teachers": args["teachers"]}
    courses.append(course)
    return jsonify({"Created": True})


@app.route("/courses/<int:course_id>", methods=["PUT"])
@token_required
def put(course_id):
    courses[course_id]['name'] = "New Name"
    return jsonify({"Updated": True})


@app.route("/courses/<int:course_id>", methods=["DELETE"])  # here authenticate with token and header
@token_required
def delete_course(course_id):
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == app.config['X-Api-Key']:
        courses.remove(courses[course_id])
        return jsonify({'Deleted': "True"})
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401




@app.route('/login')
def login():
    auth = request.authorization  # username = anthony, password = secret

    if auth and auth.password == 'secret':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/protected")  # here api to test token authentication
@token_required
def protected():
    return jsonify({"Protected Courses:": courses})


@app.route("/protected1")  # here api to test header authentication
def protected1():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == app.config['X-Api-Key']:
        return jsonify({"Protected Courses:": courses}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401


@app.route("/")
def index():
    return "Hello i am omar gamal, this is first flask api task. "


if __name__ == '__main__':
    app.run(debug=True)
