from enum import Enum
import enum
from typing import TypeVar, Mapping, Sequence, Any, get_type_hints, Optional, Union
from inspect import signature
import inspect
import typing
from flask_restx.fields import Integer, String
from imports import *
from data import courses


app = Flask(__name__)


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, version='2.0', title='Courses API v2.0',
          authorizations=authorizations)

app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


def header_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_token = request.headers.get('Authorization')

        if not auth_token:  # check if we get it, if yes save it, if no empty string
            return jsonify({'message': 'Token is missing!'})

        try:
            # decoding the token to get the data
            data = jwt.decode(auth_token, app.config['SECRET_KEY'])
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'})

        return f(*args, **kwargs)

    return decorator


course = api.model('Course', {
    'id': fields.Integer(readonly=True, description='The task course identifier'),
    'title': fields.String(required=True, description='The course title'),
    'duration': fields.Integer(required=True, description='The course duration'),
    'teachers': fields.List(fields.String),
    'studentsCount': fields.Integer(required=True, description='The course students count'),
})


editedCourse = api.model('Course', {
    'title': fields.String,
    'duration': fields.Integer,
    'teachers': fields.List(fields.String),
    'studentsCount': fields.Integer,
})

token_model = api.model('Token', {
    'token': fields.String(required=True, description='The token required for authentication'),
})

# token is missing error: I put security='apikey' in the api object declaration!!!!!


@api.route('/login')
@api.doc(params={'username': 'username', 'password': 'password'})
class Login(Resource):
    def post(self):
        request.authorization
        username = request.args.get('username')
        password = request.args.get('password')

        if(password == 'secret'):
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@api.route('/courses')
class List(Resource):
    @api.doc(security='apikey')
    @header_auth
    def get(self, auth: Union[str, int], grade: Optional[int], allgrades: enum,  filter: str, name: str = 'Unknown') -> dict:
        return jsonify({'courses': courses})


# --------------------------------------------------------------------------------
# getting the return type
# return_type = inspect.signature(List.get)
# ans = return_type.return_annotation
# ans = str(ans)
# ans = ans.split(" ")[1]
# ans = ans.replace("'", "")
# ans = ans.replace(">", "")
# print(ans)

python2restplus = {
    'str': fields.String,
    'datetime': fields.DateTime,
    'time': fields.String,
    'bool': fields.Boolean,
    'int': fields.Integer,
    'float': fields.Float,
    'relation': fields.Nested,
    'list': fields.List,
    'dict': Any,
    'enum': Enum,
}


def create_model(types) -> dict:
    modeltemp = dict()
    for type in types:
        ans = types[type]
        modeltemp[type] = python2restplus[ans]

    return modeltemp


# types = get_type_hints(List.get)
# types = dict(types)
# print("teadfadas")
# print(types)

# for type in types:
#     ans = str(types[type])

#     if ans.find('typing') == -1:
#         ans = ans.split(" ")[1]
#         ans = ans.replace("'", "")
#         ans = ans.replace(">", "")
#         k = str(type)
#         if k != 'return':
#             modeltemp[k] = python2restplus[ans]

#     else:
#         k = str(type)
#         if k != 'return':
#             # for typing module stuff (optional, union, ....) which is not in the types dict
#             modeltemp[k] = ans
# print("----------------------------------------------------------")
# print(modeltemp)
# print("----------------------------------------------------------")
# -------------------------------------------------------------------
parser = api.parser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('duration')
parser.add_argument('teachers')
parser.add_argument('studentsCount')


@api.route('/courses/add')
class Add(Resource):
    @api.doc(security='apikey')
    @api.expect(course)
    @header_auth
    def post(self):
        args = parser.parse_args()  # api.payload = args
        courses.append(args)
        return jsonify({'Updated Courses': courses})


@api.route('/courses/edit/<int:course_id>')
class Edit(Resource):
    @api.expect(editedCourse)
    def put(self, course_id):
        args = parser.parse_args()
        #args['id'] = int(args['id'])
        course = [course for course in courses if course['id'] == course_id]
        if (args['title'] != None):
            course[0]['title'] = args['title']

        if (args['duration'] != None):
            course[0]['duration'] = args['duration']

        if (args['teachers'] != None):
            course[0]['teachers'] = args['teachers']

        if (args['studentsCount'] != None):
            course[0]['studentsCount'] = args['studentsCount']

        return jsonify({'course': course[0]})


@api.route('/courses/delete/<int:course_id>')
class Delete(Resource):
    def delete(self, course_id):
        course = [course for course in courses if course['id'] == course_id]
        course_name = course[0]['title']
        courses.remove(course[0])
        return jsonify({'Done': course_name + ' Was Deleted Successfully!'})


@api.route('/query')
class Query(Resource):
    def get(self):
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
            course = [
                course for course in courses if course['duration'] == duration]
            result.append(course)

        if 'teachers' in args:
            teacher = request.args.get("teachers")
            for course in courses:
                for name in course['teachers']:
                    if name == teacher:
                        result.append(course)

        if (len(result) != 0):
            return jsonify({'courses': result})
        else:
            return jsonify({'message': 'Query Not Found'})


if __name__ == '__main__':
    app.run(debug=True)
