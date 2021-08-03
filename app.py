from flask import Flask, jsonify, request
from auth import auth,encode_jwt
app = Flask(__name__)

courses = [
    {
        'id': 1,
        'name': 'OS'
    },
    {
        'id': 2,
        'name': 'Arch'

    },
    {
        'id': 3,
        'name': 'VLSI'

    },
]

# Login
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username=="admin" and password=="admin":
        return {'token':encode_jwt(username)}
    return {'message':'Invalid username or password'}, 401

# List Courses

@app.route('/api/courses', methods=['GET'])
@auth
def listCourses():
    return jsonify({'courses': courses})

# Add Course


@app.route('/api/courses', methods=['POST'])
@auth
def addCourse():
    course = request.get_json()
    courses.append(course)
    return jsonify(course)

# Get Course


@app.route('/api/courses/<int:id>', methods=['GET'])
@auth
def getCourse(id):
    for course in courses:
        if course['id'] == id:
            return jsonify(course)
    return jsonify({'message': 'course not found'})

# Edit Course


@app.route('/api/courses/<int:id>', methods=['PUT'])
@auth
def editCourse(id):
    for course in courses:
        if course['id'] == id:
            requestData = request.get_json()
            if('id' in requestData):
                course['id'] = requestData['id']
            if('name' in requestData):
                course['name'] = requestData['name']
            return jsonify(course)
    return jsonify({'message': 'course not found'})

# Delete Course


@app.route('/api/courses/<int:id>', methods=['DELETE'])
@auth
def deleteCourse(id):
    index = 0
    for course in courses:
        if course['id'] == id:
            return jsonify(courses.pop(index))
        index += 1
    return jsonify({'message': 'course not found'})


app.run(port=3000)
