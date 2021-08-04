import re
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY']='Th1s1ss3cr3t'

api = Api(app, version='1.0', title='Courses API v1.0')


#api =  Api(app, prefix="/courses/v1")

#auth = HTTPBasicAuth()

# USER_DATA = {
#     "admin" : "password"
# }

courses = [
    {'id': 0,
     'title': 'CS106',
     'duration': '30',
     'teachers': ['Seif', 'Ahmed', 'Hammad'],
     'studentsCount': 0,
    },
    {'id': 1,
     'title': 'CS110',
     'duration': '45',
     'teachers': ['Mohamed', 'Ahmed', 'Hammad'],
     'studentsCount': 0,
    },
    {'id': 2,
     'title': 'CS321',
     'duration': '60',
     'teachers': ['Seif', 'Ashraf', 'Hammad'],
     'studentsCount': 0,
    }
]

# @auth.verify_password
# def verify(username, password):
#     if not (username and password):
#         return False
#     return USER_DATA.get(username) == password

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            print(e)
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)
    
    return decorated

def header_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')      #get Auth part from header 
        if auth_header:                                         #check if we get it, if yes save it, if no empty string
            auth_token = auth_header.split(" ")[1]
            print(auth_token)
        else:
            auth_token = ''

        try: 
            data = jwt.decode(auth_token, app.config['SECRET_KEY'])     #decoding the token to get the data
        except Exception as e:
            print(e)
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorator

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/courses', methods=['GET'])
@auth_required
def list():
    return jsonify({'courses': courses})


#this functions is also list but with id cuz we need when we do GET after editing the data in PUT
@app.route('/courses/<int:course_id>', methods=['GET'])
def list_id(course_id): #NOTE: course_id need to be passed to the func here
    course = [course for course in courses if course['id'] == course_id]
    return jsonify({'courses': course[0]})
    


@app.route('/courses', methods=['POST'])
def add():
    course = {'id': courses[-1]['id']+1,
              'title': request.json['title'],
              'duration': request.json['duration'],
              'teachers': request.json['teachers'],
              'studentsCount': request.json['studentsCount'],
             }
    courses.append(course)
    return jsonify({'courses': courses}), 201       #201=request succeeded  



@app.route('/courses/<int:course_id>', methods=['PUT'])
def edit(course_id):     #NOTE: course_id need to be passed to the func here
    course = [course for course in courses if course['id'] == course_id]      #searching for the course with the course_id passed and store it in var to be able to edit it
    course[0]['title'] = request.json.get('title', course[0]['title'])    
    course[0]['duration'] = request.json.get('duration', course[0]['duration'])
    course[0]['teachers'] = request.json.get('teachers', course[0]['teachers'])
    course[0]['studentsCount'] = request.json.get('studentsCount', course[0]['studentsCount'])
    return jsonify({'courses': course[0]})
    #return jsonify({'courses': courses}) #do this if you want to return it all


@app.route('/enrol/<int:course_id>', methods=['PUT'])
def enrol(course_id):   
    course = [course for course in courses if course['id'] == course_id]   
    course[0]['studentsCount'] = course[0]['studentsCount']+1
    return jsonify({'courses': course[0]})

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete(course_id):     #NOTE: course_id need to be passed to the func here
    course = [course for course in courses if course['id'] == course_id]      
    courses.remove(course[0])    
    #return jsonify({'courses': course[0]})
    return jsonify({'courses': 'Deleted Successfully!'}) #do this if you want to return it all


# @app.route('/secret', methods=['GET'])
# @header_auth
# def index():
#     return jsonify({'message' : 'NICE'})

@app.route('/query', methods=['GET'])
def query():
    args = request.args

    result = []

    if 'id' in args:
        id = request.args.get("id")
        id = int(id)
        course = [course for course in courses if course['id'] == id]
        result.append(course)
    
    if 'title' in args:
        title = request.args.get("title")
        course = [course for course in courses if course['title'] == title]
        result.append(course)
    
    if 'duration' in args:
        duration = request.args.get("duration")
        duration = int(duration)
        course = [course for course in courses if course['duration'] == duration]
        result.append(course)

    if 'teachers' in args:
        teacher = request.args.get("teachers")
        course = [course for course in courses for name in course['teachers'] if name == teacher]
        result.append(course)

    if (len(result) != 0):
        return jsonify({'courses': result})
    else:
        return jsonify({'message' : 'Query Not Found'})
    

    
    