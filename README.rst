==============
Flask-RESTX-Squared
==============



.. image:: https://codecov.io/gh/tactful-ai/flask-faster-api/branch/main/graph/badge.svg?token=FZJANN69LH
    :target: https://codecov.io/gh/tactful-ai/flask-faster-api
    

.. image:: https://github.com/tactful-ai/flask-faster-api/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/tactful-ai/flask-faster-api/actions/workflows/python-package.yml


.. image:: https://img.shields.io/github/license/tactful-ai/flask-faster-api   
    :alt: License
    
.. image:: https://img.shields.io/github/stars/tactful-ai/flask-faster-api?style=social   :alt: GitHub Repo stars

.. image:: https://img.shields.io/pypi/pyversions/flaskresty   
    :target: https://pypi.org/project/flaskresty
    :alt: Supported Python versions



Flask-RESTX-Squared is a Fast API style support for Flask. It Gives you MyPy types with the flexibility of flask.



Compatibility
=============

Flask-RESTX-Squared requires Python 2.7 or 3.4+. 



Installation
============

You can install Flask-RESTX-Squared with pip:

.. code-block:: console

    $ pip install flask-restx-square
    

Quick start
===========

With Flask-RESTX-Squared and the autowire decorator feature, parsing path parameters and creating api models is done using only one decorator! 

.. code-block:: python

    from flask import Flask, jsonify, request
    from flask_restx import Api, Resource, fields, marshal_with, reqparse
    from typing import Dict, List, Optional, OrderedDict, get_type_hints
    from flaskresty import autowire_decorator

    app = Flask(__name__)


    api = Api(app, version='1.0', title='Courses API')

    autowire_decorator.register_api(api)


    courses_ns = api.namespace('courses', description='Courses Endpoints')
    course = api.model('Course', {})

    course_Model = dict({
        'id': int,
        'title': str,
        'duration': int
    })


    class CourseDAO(object):
        counter = 0
        courses = [{
            'id': 1,
            'title': 'Python',
            'duration': 300}]

        @ staticmethod
        def get(id):
            for course in CourseDAO.courses:
                if course['id'] == id:
                    return course
            api.abort(404, "Course {} doesn't exist".format(id))

        @ staticmethod
        def create(data):
            course = data
            course['id'] = CourseDAO.counter = CourseDAO.counter + 1
            CourseDAO.courses.append(course)
            return course

        @ staticmethod
        def update(id, data):
            course = CourseDAO.get(id)
            course.update(data)
            return course

        @ staticmethod
        def delete(id):
            course = CourseDAO.get(id)
            CourseDAO.courses.remove(course)


        @ courses_ns.route('/<int:id>')
        class Course(Resource):
            @ courses_ns.doc('get_course')
            @ autowire_decorator.autowire_decorator('/<int:id>')
            def get(self, id) -> course_Model:
                course_data = CourseDAO.get(id)
                return course_data



        if __name__ == '__main__':
            app.run(debug=True)




Before Using Flask-RESTX-Squared
================================

.. image:: https://user-images.githubusercontent.com/63073172/129478541-496f4bb5-014f-4e29-a3b9-b61572a99c65.png


After Using Flask-RESTX-Squared
================================

.. image:: https://user-images.githubusercontent.com/63073172/129478647-41a13312-653b-4cc8-81ef-c5bb29c69614.png




Contributors
============

Flask-RESTX-Squared is brought to you by @seifashraf1, @ahmedihabb2, @nadaabdelmaboud, @omargamal253




Contribution
============
Want to contribute? That's awesome! (Details Soon) 
