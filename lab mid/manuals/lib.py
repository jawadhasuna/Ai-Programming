import re

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        if not re.fullmatch(r'\d{3}-\d{10}', isbn):  # simple ISBN pattern
            raise ValueError("Invalid ISBN")
        self.isbn = isbn

class Library:
    def __init__(self):
        self.books = []  # list of Book objects

    def add_book(self, book):
        self.books.append(book)
        print(f"Book '{book.title}' added")

    def list_books(self):
        for b in self.books:
            print(f"{b.title} by {b.author} (ISBN: {b.isbn})")

# Example
try:
    lib = Library()
    b1 = Book("Python 101", "John Doe", "123-1234567890")
    b2 = Book("AI Basics", "Jane Doe", "123-0987654321")
    lib.add_book(b1)
    lib.add_book(b2)
    lib.list_books()
except ValueError as e:
    print(e)
