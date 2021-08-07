import flask
from flask_restx import Api, Resource, fields, marshal_with, reqparse
from typing import List
from functools import wraps


def autowire_decorator(path):
    def decorator(func):
        params = func.__annotations__

        return_params=params['return']
        #model = get_model(return_params)
        params.pop('return', None)

        #path_params = get_path_params(path)
        # for param in path_params:
        #    params.pop(param, None)

        #parser = get_parser(params)

        # test_example
        model = api.model('Course', {
            'name': fields.String(required=True, description='The course name'),
            'duration': fields.Integer(required=True, description='The course duration'),
            'teachers': fields.List(fields.String, description='The course teachers'),
        })
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='The course name')
        parser.add_argument('duration', type=int, help='The course duration')
        parser.add_argument(
            'teachers', type=List[str], help='The course teachers')

        @wraps(func)
        @api.expect(parser)
        @api.marshal_with(model)
        def wrapper(*args, **kwargs):
            args_parser = parser.parse_args()
            return func(*args, *args_parser.values(), **kwargs)
        return wrapper
    return decorator