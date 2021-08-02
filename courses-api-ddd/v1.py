from flask import Flask, jsonify, request, make_response
from flask.helpers import make_response
from courses.repos import MemoryRepo
from courses.usecases.course_use_cases import CourseUseCases

from services.auth import encode_auth_token, requires_auth

Repo = MemoryRepo()

app = Flask(__name__)

@app.route("/courses", methods=['GET'])
@requires_auth()
def get_courses(payload):
    try:
        query_params = request.args
        username = payload['username']
        coursesUC = CourseUseCases(Repo)
        courses_list = coursesUC.get_course_list(username, query_params)
        if courses_list is None or len(courses_list) <= 0:
                return make_response(jsonify({
                    'error': 'No courses found'
                }), 404)
            
        return make_response(jsonify([course.format() for course in courses_list]), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 400)        


@app.route("/courses", methods=['POST'])
@requires_auth()
def add_courses(payload):
    try:
        body = request.get_json()
        name = body['name']
        price = body['price']
        duration = body['duration']
        students_count = body['students_count']
        username = payload['username']
        
        coursesUC = CourseUseCases(Repo)
        result = coursesUC.create_course(username, name, price, duration, students_count)

        if result is None:
            return make_response(jsonify({
                'error': 'Cannot add Course'
            }), 400)

        return make_response(jsonify(result.format()), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/courses/<id>", methods=['PUT'])
@requires_auth()
def edit_course(payload, id):
    try:
        body = request.get_json()
        name = body['name']
        price = body['price']
        duration = body['duration']

        username = payload['username']
        
        coursesUC = CourseUseCases(Repo)
        result = coursesUC.edit_course(username, id, name, price, duration)
        if result is None or (isinstance(result, list) and len(result) <= 0 ):
            return make_response(jsonify({
                'error': 'Cannot edit Course'
            }), 400)
        
        return make_response(jsonify(result.format()), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/courses/<course_id>", methods=['DELETE'])
@requires_auth()
def delete_course(payload, course_id):
    try:
        username = payload['username']
        coursesUC = CourseUseCases(Repo)
        result = coursesUC.delete_course(username, course_id)
        if result is None or len(result) <= 0:
            return make_response(jsonify({
                'error': 'Cannot delete Course'
            }), 400)  
        return make_response(jsonify({
            'message': "Deleted Successfully"
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/courses/enroll", methods=["POST", "GET"])
@requires_auth()
def enroll_in_course(payload):
    try:
        username = payload["username"]
        course_id = request.form['id']
        coursesUC = CourseUseCases(Repo)
        result = coursesUC.enroll_course(username, course_id)
        
        if result is None:
            return make_response(jsonify({
                'error': 'Cannot enroll Course'
            }), 400)        
        return make_response(jsonify({
            "message": "Enrolled",
            "course": result.format()
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/generate_token", methods=["GET"])
def generate_token():
    try:
        auth_token = encode_auth_token("random string", "geekahmed")
        if auth_token:
            return make_response(jsonify({
                        'success': True,
                        'message': 'Successfully generated.',
                        'auth_token': auth_token
                    }), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)