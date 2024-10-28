import pytest

def test_equal_ornot_equal():
    assert 3==3
    


class Student:
    def __init__(self, first_name: str, last_name:str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
        

@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'Comp Sci',3) 


def test_person_initialisation (default_student):
    assert default_student.first_name == 'John', 'First name should be John'
    assert default_student.last_name == 'Doe', 'Last name should be Doe'
    assert default_student.major == 'Comp Sci'
    assert default_student.years == 3
    