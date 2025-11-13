try:
    num = int(input("Enter a number: "))
    print("100 divided by your number is", 100 / num)
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
except ValueError:
    print("Error: Please enter a valid integer!")

#Custom Exception Example
try:
    age = int(input("Enter your age: "))
    if age < 0:
        raise ValueError("Age cannot be negative")
except ValueError as e:
    print("Error:", e)

#Handling Dictionary KeyError
try:
    student = {"name": "Ali", "age": 21}
    print(student["grade"])   # key does not exist
except KeyError:
    print("Error: Key not found in dictionary")

#Validate a Strong Password
import re

password = "mypass@123"
pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

if re.match(pattern, password):
    print("Strong Password")
else:
    print("Weak Password")

#Split a String by Multiple Delimiters
import re

text = "apple,banana;orange|grape"
pattern = r"[;,\|]"   # split by ; , or |

fruits = re.split(pattern, text)
print("Fruits:", fruits)

#Extract Hashtags from a Tweet
import re

tweet = "Loving #Python #AI #11AI and #MachineLearning #Machine_Learning"
pattern = r"#\w+"

hashtags = re.findall(pattern, tweet)
print("Hashtags:", hashtags)

#Remove Extra Spaces
import re

text = "Python    is   awesome"
pattern = r"\s+"   # one or more spaces

cleaned = re.sub(pattern, ":", text)
print("Cleaned:", cleaned)

#Find All Words Starting with Capital Letters
import re

text = "Python is Fun and Powerful AA A22 222A"
pattern = r"\b[A-Z0-9][a-zA-Z0-9]*\b"

words = re.findall(pattern, text)
print("Capitalized words:", words)

#Extract All Phone Numbers
import re

text = "Call me at 123-456-7890 or 987-654-3210"
pattern = r"\d{3}-\d{3}-\d{4}"

phones = re.findall(pattern, text)
print("Phone Numbers:", phones)

email_pattern = r'\w+@\w+\.\w+'
text = 'Contact us at support@example.com or admin@test.org'

emails = re.findall(email_pattern, text)
print("Found emails:", emails)

#Check if a string contains digits

text = "Python@3777a7770"
pattern = r"\b\w+\b"   # one or more digits

match = re.findall(pattern, text)
print(match)
#if match:
#    print("Digits found:", match.group())

import re

pattern = r'\d{3}-\d{2}-\d{4}'
text = 'My SSN is 123-45-6789.'

match = re.search(pattern, text)
#print(match)
if match:
    print("Found SSN:", match.group())

import re

text="""
User: John Doe
Email: john.doe@gmail.com
Backup Email: johnd123@company.org
IP: 192.168.0.1
Invalid IP: 999.888.77.666
Date Joined: 12-05-2023
Website: https://www.example.com/profile
Contact: +92-300-1234567 or (051) 6543210
"""

emails=re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',text)
ips=[ip for ip in re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b',text) if all(0<=int(x)<=255 for x in ip.split('.'))]
dates=re.findall(r'\b(?:\d{2}[-/]\d{2}[-/]\d{4}|\d{4}-\d{2}-\d{2})\b',text)
phones=re.findall(r'\+?\d{1,3}-\d{3,4}-\d{7}|\(\d{3,4}\)\s?\d{6,7}|0\d{3}-\d{7}',text)
urls=re.findall(r'https?://[^\s]+',text)

results={
 "emails":emails,
 "ips":ips,
 "dates":dates,
 "phones":phones,
 "urls":urls
}

print(results)

text='jawad@gmail.com'
pattern=r'\w+@\w+.\w+'
match=re.search(pattern,text)
if match:
  print(match.group())

text='jawad@gmail.com ali@gmail.com subhan@gmail.com'
pattern=r'\w+@\w+.\w+'
match=re.findall(pattern,text)
if match:
  print(match)



class Library:
    def __init__(self, librarian, books=None):
        self.librarian = librarian
        self.books = books if books else []

    def add_book(self, title):
        self.books.append(title)
        print(f"Book '{title}' added to the library.")

    def display_books(self):
        print(f"Librarian: {self.librarian}")
        print("Books Available:")
        for book in self.books:
            print(f" {book}")

    def __del__(self):
        print(f"Library managed by {self.librarian} is now closed.")
email_re = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        print(f"Employee {self.name} created.")

    def show(self):
        print(f"Name: {self.name}, Salary: {self.salary}")

    def __del__(self):
        print(f"Destructor called. Employee {self.name} deleted.")

class BankAccount:
    def __init__(self, name, balance, account_type):
        self.name = name
        self.balance = float(balance)
        self.account_type = account_type

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New Balance: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn {amount}. Remaining Balance: {self.balance}")
        else:
            print("Insufficient funds!")
class ShoppingCart:
    def __init__(self, owner):
        self.owner = owner
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"'{item}' added to {self.owner}'s cart.")

    def show_items(self):
        print(f"{self.owner}'s Cart: {', '.join(self.items)}")