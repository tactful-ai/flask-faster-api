from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, version='2.0', title='Courses API',
          description='A simple Coureses API',
          )

ns = api.namespace('Courses', description='Courses operations')

course = api.model('Course', {
    'id': fields.Integer(readonly=True, description='The task course identifier'),
    'title': fields.String(required=True, description='The course title'),
    'duration': fields.Integer(readonly=True, description='The course duration'),
    'teachers': fields.List(required=True, description='The course teachers list'),
    'studentsCount': fields.Integer(readonly=True, description='The course students count'),
})


class CourseDAO(object):
    def __init__(self):
        self.courses = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = CourseDAO()
DAO.create({'id': 0,
            'title': 'CS106',
            'duration': '30',
            'teachers': ['Seif', 'Ahmed', 'Hammad'],
            'studentsCount': 0,
            })

DAO.create({'id': 1,
            'title': 'CS110',
            'duration': '45',
            'teachers': ['Mohamed', 'Ahmed', 'Hammad'],
            'studentsCount': 0,
            })

DAO.create({'id': 2,
            'title': 'CS321',
            'duration': '60',
            'teachers': ['Seif', 'Ashraf', 'Hammad'],
            'studentsCount': 0,
            })


@ns.route('/')
class CoursesList(Resource):
    @ns.doc('list_courses')
    @ns.marshal_list_with(course)
    def get(self):
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
