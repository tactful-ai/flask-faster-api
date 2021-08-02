

class MemoryRepo:
    def __init__(self):
        self.memory = {}
    def add_course_for_teacher(self, username, new_course):
        if username not in self.memory:
            self.memory[username] = []
        self.memory[username].append(new_course)
    
    def get_courses_by_username(self, username, filters):
        if username not in self.memory:
            return []
        else:
            teacher_courses = self.memory[username]
            if filters:
                search_result = list(filter(lambda course : (course.name == filters.get('name') or course.duration == filters.get('duration')), teacher_courses))
                if search_result is None:
                    return []
                return search_result
            else:
                return teacher_courses

    def enroll_in_course(self, username, course_id):
        
        if username not in self.memory:
            return []

        teacher_courses = self.memory[username]
        if any(course.id == course_id for course in teacher_courses):
            for course in teacher_courses:
                if course.id == course_id:
                    course.students_count += 1
                    return course
        return []
    
    def delete_course(self, username, course_id):
        if username not in self.memory:
            return []
        teacher_courses = self.memory[username]

        if any(course.id == course_id for course in teacher_courses):
            teacher_courses[:] = list(filter(lambda course : course.id != course_id, teacher_courses))
            return teacher_courses

        return []
    
    def edit_course(self, username, course_id, course_name, course_price, course_duration):
        if username not in self.memory:
            return []
        
        teacher_courses = self.memory[username]
        if any(course.id == course_id for course in teacher_courses):
            for course in teacher_courses:
                if course.id == course_id:
                    if course_name is not None:
                        course.name = course_name
                    if course_price is not None:
                        course.price = course_price
                    if course_duration is not None:
                        course.duration = course_duration
                    return course
        return []