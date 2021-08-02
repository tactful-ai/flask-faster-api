class Course:
    def __init__(self, id, name, price, duration, students_count = 0):
        self.id = id
        self.name = name
        self.price= price
        self.duration = duration
        self.students_count = students_count
    
    def __repr__(self):
        return f'<ID: {self.id}, NAME: {self.name}, PRICE: {self.price}, DURATION: {self.duration}, STUDENTS COUNT: {self.students_count}'
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            "duration": self.duration,
            "students": self.students_count
        }