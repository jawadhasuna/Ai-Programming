import re

class Employee:
    def __init__(self, name, email, position):
        if not re.fullmatch(r'[A-Za-z ]+', name):
            raise ValueError("Invalid name")
        if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
            raise ValueError("Invalid email")
        self.name = name
        self.email = email
        self.position = position

class Office:
    def __init__(self):
        self.employees = []  # list of tuples (name, position)

    def add_employee(self, emp):
        self.employees.append((emp.name, emp.position))
        print(f"Employee {emp.name} added as {emp.position}")

# Example
try:
    office = Office()
    e1 = Employee("Sara Ali", "sara@office.com", "Manager")
    e2 = Employee("Ali Khan", "ali@office.com", "Developer")
    office.add_employee(e1)
    office.add_employee(e2)
    print("All employees:", office.employees)
except ValueError as e:
    print(e)
