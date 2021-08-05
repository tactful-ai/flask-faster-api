from auth import *
# auth has import all the packages

app = FastAPI()


class Course(BaseModel):
    id: int
    title: str
    duration: int
    teachers: List
    students: List
    studentsCount: int


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if(password == 'secret'):
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=15)}, secretkey)

        return {'token': token.decode('UTF-8')}

    return {'Error': 'Password Incorrect'}, 401


@app.get("/courses")
def list_courses(token: str = Depends(authenticate)):
    return {'Courses List': courses}


@app.post("/courses/add")
def add_course(course: Course):
    course.id = courses[-1]['id']+1
    courses.append(course)
    return {'Updated Courses List': courses}


@app.put("/courses/edit/{course_id}")
def update_course(course_id: int, title: str = None, duration: int = None, teacher: str = None, student: str = None, studentsCount: int = None):
    course = [course for course in courses if course['id'] == course_id]
    if (title != None):
        course[0]['title'] = title

    if (duration != None):
        course[0]['duration'] = duration

    if (teacher != None):
        course[0]['teachers'].append(teacher)

    if (student != None):
        course[0]['students'].append(student)

    if (studentsCount != None):
        course[0]['studentsCount'] = studentsCount

    return {'Edited Course': course}


@app.delete("/courses/delete/{course_id}")
def delete_course(course_id: int):
    course = [course for course in courses if course['id'] == course_id]
    course_name = course[0]['title']
    courses.remove(course[0])
    return {'Done': course_name + ' Was Deleted Successfully!'}


@app.get('/query')
def query_course(id: int = None, title: str = None, duration: int = None, teacher: str = None, student: str = None, studentsCount: int = None):
    result = []

    if (id != None):
        course = [course for course in courses if course['id'] == id]
        result.append(course)

    if (title != None):
        course = [course for course in courses if course['title'] == title]
        result.append(course)

    if (duration != None):
        course = [course for course in courses if course['duration'] == duration]
        result.append(course)

    if (teacher != None):
        for course in courses:
            for name in course['teachers']:
                if name == teacher:
                    result.append(course)

    if (student != None):
        for course in courses:
            for name in course['students']:
                if name == student:
                    result.append(course)

    if (len(result) != 0):
        return {'courses': result}
    else:
        return {'message': 'Query Not Found'}


@app.put("/courses/enroll")
def enroll_course(course_id: int = Form(...), student: str = Form(...)):
    course = [course for course in courses if course['id'] == course_id]

    if (course == None):
        return {'Error': 'Course Not Found. Please Enter a Valid Course ID'}

    else:
        course[0]['studentsCount'] = course[0]['studentsCount']+1
        course[0]['students'].append(student)
        return {'Course Now': course}
