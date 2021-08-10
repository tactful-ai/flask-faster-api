==============
Flask RESTY
==============

.. image:: https://img.shields.io/github/license/tactful-ai/flask-faster-api   
    :alt: License
    
.. image:: https://img.shields.io/github/stars/tactful-ai/flask-faster-api?style=social   :alt: GitHub Repo stars


Flask-RESTY is a Fast API style support for Flask. It Gives you MyPy types with the flexibility of flask.



Compatibility
=============

Flask-RESTY requires Python 2.7 or 3.4+. 





Installation
============

You can install Flask-RESTY with pip:

.. code-block:: console

    $ pip install flask-resty
    

Quick start
===========

With Flask-RESTY and the autowire decorator feature, parsing path parameters and creating api models is done using only one decorator! 

.. code-block:: console

    from flask import Flask
    from flask_restx import Api, Resource, fields
    from flaskresty import *

    app = Flask(__name__)
    api = Api(app, version='1.0', title='Courses API')

    courses_ns = api.namespace('courses', description='Courses Endpoints')

    course_Model = dict({
        'id': int,
        'title': str,
        'duration': int,
        'teachers': List[str]

    })

    class CourseDAO(object):
        counter = 0
        courses = [{
            'id': 1,
            'title': 'Python',
            'duration': 300,
            'teachers': ['seif', 'nada', 'ahmed']
        }]

        def get(id):
            for course in CourseDAO.courses:
                if course['id'] == id:
                    return course
            api.abort(404, "Course {} doesn't exist".format(id))

        def create(data):
            course = data
            course['id'] = CourseDAO.counter = CourseDAO.counter + 1
            CourseDAO.courses.append(course)
            return course

        def update(id, data):
            course = CourseDAO.get(id)
            course.update(data)
            return course

        def delete(id):
            course = CourseDAO.get(id)
            CourseDAO.courses.remove(course)


    @ courses_ns.route('/<int:id>')
    class Course(Resource):
        @courses_ns.doc('get_course')
        @autowire_decorator('/<int:id>')
        def get(self, id) -> course_Model:
            course_data = CourseDAO.get(id)
            return course_data


    if __name__ == '__main__':
        app.run(debug=True)




Contributors
============

Flask-RESTY is brought to you by @seifashraf1, @ahmedihabb2, @nadaabdelmaboud, @omargamal253




Contribution
============
Want to contribute? That's awesome! (Details Soon) 
