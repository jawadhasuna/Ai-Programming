import re

class Customer:
    def __init__(self, name, email, balance=0):
        if not re.fullmatch(r'[A-Za-z ]+', name):
            raise ValueError("Invalid name")
        if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
            raise ValueError("Invalid email")
        self.name = name
        self.email = email
        self.balance = balance

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Deposit must be positive")
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        except ValueError as e:
            print("Error:", e)

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Withdrawal must be positive")
            if amount > self.balance:
                raise ValueError("Insufficient balance")
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        except ValueError as e:
            print("Error:", e)

# Example usage
try:
    c1 = Customer("Jawad Hassan", "jawad@example.com", 1000)
    c1.deposit(500)
    c1.withdraw(200)
except ValueError as e:
    print(e)
