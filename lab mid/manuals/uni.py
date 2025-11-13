import re

class Student:
    def __init__(self, name, email, courses=[]):
        if not re.fullmatch(r'[A-Za-z ]+', name):
            raise ValueError("Invalid name")
        if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
            raise ValueError("Invalid email")
        self.name = name
        self.email = email
        self.courses = courses  # list of course names

    def enroll(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} enrolled in {course}")
        else:
            print(f"{self.name} is already enrolled in {course}")

# Example
try:
    s1 = Student("Ali Khan", "ali.khan@uni.com")
    s1.enroll("AI")
    s1.enroll("Machine Learning")
except ValueError as e:
    print(e)
