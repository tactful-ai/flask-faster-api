from imports import *

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
