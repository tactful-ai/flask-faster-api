from typing import List
from flask import Flask, request, Blueprint
from flask_restx import Api, Resource
from flask_fastx import autowire, register_api
from flask_fastx.params import Query, Path, Body
from pydantic import BaseModel

app = Flask(__name__)
api = Api(app, version="1.0", title="Courses API", description="A simple API")
courses_ns = api.namespace("courses", description="Courses operations")

register_api(api)


class Course(BaseModel):
    '''
    id : the course unique identifier
    title : the course title
    duration : the course duration
    teachers : the enrolled teachers of the course
    studentsCount : the number of students enrolled in the course
    '''
    id: int
    title: str
    duration: str
    teachers: List[str]
    studentsCount: int


courses: List[Course] = []


@courses_ns.route('/')
class CourseListApi(Resource):
    @autowire
    def get(self) -> List[dict]:
        dict_courses = []
        for course in courses:
            dict_courses.append(dict(course))
        return dict_courses

    @autowire
    def post(self, title: str = Body(None), duration: int = Body(None)) -> Course:
        course = Course(id=len(courses)+1, title=title,
                        duration=duration, teachers=[], studentsCount=0)
        courses.append(course)
        return course


@courses_ns.route('/<int:id>')
class CourseApi(Resource):
    @autowire
    def get(self, id: int = Path(None)) -> Course:
        course = [course for course in courses if course.id == id][0]
        return course

    @autowire
    def put(self, id: int = Path(None), title: str = Query(None), teachers: List[str] = Query(None)) -> Course:
        course = [course for course in courses if course.id == id][0]
        if title is not None:
            course.title = title
        if teachers is not None:
            course.teachers = teachers
        return course

    @autowire
    def delete(self, id: int = Path(None)) -> str:
        course = [course for course in courses if course.id == id][0]
        courses.remove(course)
        return "course is removed succisfully", 200


if __name__ == '__main__':
    app.run(debug=True)
