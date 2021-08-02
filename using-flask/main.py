from flask import Flask, jsonify, request, make_response
from flask.helpers import make_response
from random import randrange
from models import Course
from dummy import array_of_courses
from auth import encode_auth_token, requires_auth

app = Flask(__name__)

@app.route("/courses", methods=['GET'])
def get_courses():
    query_params = request.args
    if query_params:
        name = query_params.get('name')
        duration = query_params.get('duration')
        
        search_result = list(filter(lambda course : (course.name == name or course.duration == duration), array_of_courses))

        if search_result is None:
            return make_response(jsonify({
                'error': 'No courses for these filters'
            }), 404)
        
        return make_response(jsonify([course.format() for course in search_result]), 200)
    else:
        courses = [x.format() for x in array_of_courses]
        return make_response(jsonify(courses), 200)

@app.route("/courses", methods=['POST'])
@requires_auth()
def add_courses(payload):
    try:
        body = request.get_json()

        name = body['name']
        price = body['price']
        duration = body['duration']
        
        if any(course.name == name for course in array_of_courses):
            return make_response(jsonify({
                'error': 'The Course is already existed'
            }), 400)

        new_course = Course(randrange(100), name, price, duration)
        array_of_courses.append(new_course)

        return make_response(jsonify(new_course.format()), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/courses/<id>", methods=['PUT'])
@requires_auth()
def edit_course(id, payload):
    try:
        body = request.get_json()
        name = body['name']
        price = body['price']
        duration = body['duration']
        if not any(course.id == int(id) for course in array_of_courses):
            return make_response(jsonify({
                'error': 'Course not found'
            }), 404)        

        for course in array_of_courses:
            if course.id == int(id):
                if name is not None:
                    course.name = name
                if price is not None:
                    course.price = price
                if duration is not None:
                    course.duration = duration
        return make_response(jsonify(course.format()), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)
@app.route("/courses/<id>", methods=['DELETE'])
@requires_auth()
def delete_course(id, payload):
    try:
        if not any(course.id == int(id) for course in array_of_courses):
            return make_response(jsonify({
                'error': 'Course not found'
            })), 404   
        
        array_of_courses[:] = list(filter(lambda course : course.id != int(id), array_of_courses))
        
        return make_response(jsonify({
            'message': "Deleted Successfully"
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/courses/enroll", methods=["POST", "GET"])
def enroll_in_course():
    try:
        course_id = request.form['id']
        if not any(course.id == int(course_id) for course in array_of_courses):
            return make_response(jsonify({
                'error': 'Course not found'
            }), 404)       

        for course in array_of_courses:
            if course.id == int(course_id):
                course.students_count += 1
        
        return make_response(jsonify({
            "message": "Enrolled"
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "error" : "Message: {}, status 400 Bad request".format(e)
        }), 500)

@app.route("/generate_token", methods=["GET"])
def generate_token():
    try:
        auth_token = encode_auth_token("random string",123)
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