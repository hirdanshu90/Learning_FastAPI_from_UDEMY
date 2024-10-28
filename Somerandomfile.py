print("Hello workd from this file")

class Student:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
        
instance_student = Student("Hir", 2)
print(instance_student.name)