from courses.domain.course import Course
import uuid

class CourseUseCases:
    def __init__(self, course_repo, teacher_repo=None):
        self.course_repo = course_repo
        self.teacher_repo = teacher_repo
    
    def create_course(self, username, course_name, course_price, course_duration, students_count):
        course_id = str(uuid.uuid4())
        new_course = Course(course_id, course_name, course_price, course_duration, students_count)
        self.course_repo.add_course_for_teacher(username, new_course)
        return new_course

    def get_course_list(self, username, filters=None):
        return self.course_repo.get_courses_by_username(username, filters)
    
    def edit_course(self, username, course_id, course_name, course_price, course_duration):
        return self.course_repo.edit_course(username, course_id, course_name, course_price, course_duration)
    
    def enroll_course(self, username, course_id):
        return self.course_repo.enroll_in_course(username, course_id)

    def delete_course(self, username, course_id):
        return self.course_repo(username, course_id)
    
