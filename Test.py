class Book:
    def __init__(self, title, author, year, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    def is_available(self):
        return self.copies > 0

    def borrow(self):
        if self.is_available():
            self.copies -= 1
            return True
        return False

    def return_book(self):
        self.copies += 1

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) - Copies: {self.copies}"


class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.borrow():
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed '{book.title}'")
        else:
            print(f"'{book.title}' is not available")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            print(f"{self.name} returned '{book.title}'")
        else:
            print(f"{self.name} did not borrow '{book.title}'")

    def list_books(self):
        if not self.borrowed_books:
            print(f"{self.name} has no borrowed books.")
        else:
            print(f"{self.name} has borrowed:")
            for book in self.borrowed_books:
                print(f" - {book.title}")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def show_books(self):
        print("Library Catalog:")
        for book in self.books:
            print(f" - {book}")

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None


# Sample usage
if __name__ == "__main__":
    lib = Library()
    lib.add_book(Book("1984", "George Orwell", 1949, 2))
    lib.add_book(Book("The Hobbit", "J.R.R. Tolkien", 1937))
    lib.add_book(Book("Python 101", "John Doe", 2020, 3))

    lib.show_books()

    alice = Member("Alice")
    bob = Member("Bob")

    book1 = lib.find_book("1984")
    book2 = lib.find_book("The Hobbit")

    alice.borrow_book(book1)
    alice.borrow_book(book2)
    bob.borrow_book(book1)  # Only 2 copies available

    alice.list_books()
    bob.list_books()

    alice.return_book(book1)
    bob.borrow_book(book1)

    lib.show_books()
