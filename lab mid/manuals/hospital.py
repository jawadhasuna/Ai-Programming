import re

class Patient:
    def __init__(self, name, email, phone):
        if not re.fullmatch(r'[A-Za-z ]+', name):
            raise ValueError("Invalid name")
        if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
            raise ValueError("Invalid email")
        if not re.fullmatch(r'\+?\d{10,15}', phone):  # simple phone validation
            raise ValueError("Invalid phone number")
        self.name = name
        self.email = email
        self.phone = phone

class Hospital:
    def __init__(self):
        self.patients = []  # list of tuples (name, phone)

    def add_patient(self, patient):
        self.patients.append((patient.name, patient.phone))
        print(f"Patient {patient.name} added")

# Example
try:
    hospital = Hospital()
    p1 = Patient("Ali Rehman", "ali@hospital.com", "+923001234567")
    p2 = Patient("Sara Khan", "sara@hospital.com", "+923001112233")
    hospital.add_patient(p1)
    hospital.add_patient(p2)
    print("All patients:", hospital.patients)
except ValueError as e:
    print(e)
