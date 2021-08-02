
class Teacher:
    def __init__(self, username):
        self.username = username
        self.course_id = 0

    @property
    def course_id(self):
        return self.course_id

    @course_id.setter
    def course_id(self, id):
        self.course_id = id


    def __repr__(self):
        return f"<Teacher: USERNAME: {self.username}, COURSE ID: {self.course_id}>"