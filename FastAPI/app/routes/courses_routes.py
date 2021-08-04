from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Optional
from ..schemas import courses_schema as schema
from ..services.auth_service import get_current_user
router = APIRouter(
    tags=['Courses'],
    prefix='/courses'
)

courses = []


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Course)
def createCourse(request: schema.Course, current_user=Depends(get_current_user)):
    for course in courses:
        if(course.id == request.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Course already exists")
    courses.append(request)
    return request


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.Course])
def getCourses(current_user=Depends(get_current_user)):
    return courses


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Course)
def getCourse(id: int, current_user=Depends(get_current_user)):
    for course in courses:
        if(course.id == id):
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Course not found")


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Course)
def updateCourse(id: int, name: Optional[str] = None, duration: Optional[int] = None, teachers: Optional[List[str]] = None, current_user=Depends(get_current_user)):
    for course in courses:
        if(course.id == id):
            if name:
                course.name = name
            if duration:
                course.duration = duration
            if teachers:
                course.teachers = teachers
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Course not found")


router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,
              response_model=None)


def deleteCourses(id: int, current_user=Depends(get_current_user)):
    for course in courses:
        if(course.id == id):
            courses.remove(course)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Course not found")
