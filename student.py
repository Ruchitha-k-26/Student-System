class Student:
    def __init__(self, student_id, name, age, grade):
        self.id = student_id
        self.name = name
        self.age = int(age)
        self.grade = grade

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age, "grade": self.grade}

    @staticmethod
    def from_dict(data):
        return Student(data["id"], data["name"], data["age"], data["grade"])

    def _str_(self):
        return f"{self.id}, {self.name}, {self.age}, {self.grade}"
