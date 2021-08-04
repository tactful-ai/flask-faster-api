from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List
from data.Courses_ import courses
from data.Models import Course, Student, AuthDetails
from data.Students_ import students
from data.Users_ import users

from helper.auth_v3 import AuthHandler

app = FastAPI()

auth_handler = AuthHandler()


@app.get("/courses")
async def get_courses(username=Depends(auth_handler.auth_wrapper)):
    return {"Courses ": courses}, 200


@app.post("/courses")
async def post_course(course: Course, username=Depends(auth_handler.auth_wrapper)):
    new_course = {
        "name": course.name,
        "course_id": len(courses),
        "duration": course.duration,
        "teachers": course.teachers
    }
    courses.append(new_course)
    return {"message": "Successful added ", "Course ": new_course}, 200


@app.delete("/courses/{course_id}")
async def delete_course(course_id: int, username=Depends(auth_handler.auth_wrapper)):
    if course_id <= len(courses):
        courses.remove(courses[course_id])
        return {"message": "Successful deleted "}, 200
    else:
        return {"message": "Course ID Not found "}, 404


@app.put("/courses/{course_id}")
async def update_course(course_id: int, course: Course, username=Depends(auth_handler.auth_wrapper)):
    if course_id <= len(courses):
        updated_course = {
            "name": course.name,
            "course_id": course_id,
            "duration": course.duration,
            "teachers": course.teachers
        }
        courses[course_id] = updated_course
        return {"message": "Successful updated ", "Course": updated_course}, 200
    else:
        return {"message": "Course ID Not found "}, 404


@app.post("/courses/enroll")
async def enroll_course(name: str, course_id: int, username=Depends(auth_handler.auth_wrapper)):
    try:
        student = {
            "name": name,
            "course_id": course_id
        }
        students.append(student)
        return {"Message:": "Successfully Enrolled", "Students": students}, 200
    except Exception as e:
        return {"Error": ": {}, status 400 Bad request".format(e)}, 500


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password
    })
    return {"message": "successful register"}, 200


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token}


@app.get("/")
async def root():
    return {"message": "Courses API Using FastAPI"}









