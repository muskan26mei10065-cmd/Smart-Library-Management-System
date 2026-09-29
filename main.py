import json
from pathlib import Path
from datetime import date, timedelta


# ============================================================
# DATA FILE
# ============================================================

DATA_FILE = Path("library_data.json")


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_non_empty(value, field_name):
    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} cannot be empty.")

    return value


def validate_positive_integer(value, field_name):
    try:
        number = int(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a number.")

    if number <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")

    return number


# ============================================================
# BOOK CLASS
# ============================================================

class Book:

    def __init__(
        self,
        book_id,
        title,
        author,
        category,
        status="Available",
        issued_to=None,
        due_date=None
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.status = status
        self.issued_to = issued_to
        self.due_date = due_date

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "status": self.status,
            "issued_to": self.issued_to,
            "due_date": self.due_date
        }


# ============================================================
# MEMBER CLASS
# ============================================================

class Member:

    def __init__(
        self,
        member_id,
        name,
        phone,
        issued_books=None
    ):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.issued_books = issued_books if issued_books is not None else []

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "issued_books": self.issued_books
        }


# ============================================================
# STORAGE FUNCTIONS
# ============================================================

def save_data(books, members):

    data = {
        "books": [
            book.to_dict()
            for book in books.values()
        ],

        "members": [
            member.to_dict()
            for member in members.values()
        ]
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():

    if not DATA_FILE.exists():
        return {}, {}

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        books = {}
        members = {}

        for book_data in data.get("books", []):
            book = Book(
                book_data["book_id"],
                book_data["title"],
                book_data["author"],
                book_data["category"],
                book_data.get("status", "Available"),
                book_data.get("issued_to"),
                book_data.get("due_date")
            )

            books[book.book_id] = book

        for member_data in data.get("members", []):
            member = Member(
                member_data["member_id"],
                member_data["name"],
                member_data["phone"],
                member_data.get("issued_books", [])
            )

            members[member.member_id] = member

        return books, members

    except (json.JSONDecodeError, KeyError, TypeError):
        print("Warning: Data file is corrupted. Starting with empty data.")
        return {}, {}


# ============================================================
# LIBRARY CLASS
# ============================================================

class Library:

    def __init__(self, books=None, members=None):
        self.books = books if books is not None else {}
        self.members = members if members is not None else {}

    def add_book(self, book):

        if book.book_id in self.books:
            raise ValueError("Book ID already exists.")

        self.books[book.book_id] = book

        save_data(self.books, self.members)

        return "Book added successfully."

    def add_member(self, member):

        if member.member_id in self.members:
            raise ValueError("Member ID already exists.")

        self.members[member.member_id] = member

        save_data(self.books, self.members)

        return "Member registered successfully."

    def search_books(self, keyword):

        keyword = keyword.lower()
        result = []

        for book in self.books.values():

            if (
                keyword in book.title.lower()
                or keyword in book.author.lower()
                or keyword in book.category.lower()
            ):
                result.append(book)

        return result

    def issue_book(self, book_id, member_id, days):

        if book_id not in self.books:
            raise ValueError("Book not found.")

        if member_id not in self.members:
            raise ValueError("Member not found.")

        book = self.books[book_id]
        member = self.members[member_id]

        if book.status != "Available":
            raise ValueError("Book is already issued.")

        due_date = date.today() + timedelta(days=days)

        book.status = "Issued"
        book.issued_to = member_id
        book.due_date = str(due_date)

        member.issued_books.append(book_id)

        save_data(self.books, self.members)

        return f"Book issued successfully. Due date: {due_date}"

    def return_book(self, book_id):

        if book_id not in self.books:
            raise ValueError("Book not found.")

        book = self.books[book_id]

        if book.status != "Issued":
            raise ValueError("Book is not issued.")

        member_id = book.issued_to

        if member_id in self.members:

            member = self.members[member_id]

            if book_id in member.issued_books:
                member.issued_books.remove(book_id)

        book.status = "Available"
        book.issued_to = None
        book.due_date = None

        save_data(self.books, self.members)

        return "Book returned successfully."

    def summary(self):

        total = len(self.books)
        available = 0
        issued = 0

        for book in self.books.values():

            if book.status == "Available":
                available += 1
            else:
                issued += 1

        return f"""
===== LIBRARY SUMMARY =====
Total Books     : {total}
Available Books : {available}
Issued Books    : {issued}
Total Members   : {len(self.members)}
============================
"""


# ============================================================
# REPORT FUNCTIONS
# ============================================================

def print_books(books):

    if not books:
        print("No books available.")
        return

    print("\n================ BOOK LIST ================")

    for book in books.values():

        print(f"Book ID   : {book.book_id}")
        print(f"Title     : {book.title}")
        print(f"Author    : {book.author}")
        print(f"Category  : {book.category}")
        print(f"Status    : {book.status}")

        if book.issued_to:
            print(f"Issued To : {book.issued_to}")

        if book.due_date:
            print(f"Due Date  : {book.due_date}")

        print("------------------------------------------")


def print_members(members):

    if not members:
        print("No members available.")
        return

    print("\n=============== MEMBER LIST ===============")

    for member in members.values():

        print(f"Member ID : {member.member_id}")
        print(f"Name      : {member.name}")
        print(f"Phone     : {member.phone}")

        if member.issued_books:
            print(
                f"Issued Books : {', '.join(member.issued_books)}"
            )
        else:
            print("Issued Books : None")

        print("------------------------------------------")


# ============================================================
# MENU
# ============================================================

def show_menu():

    print("""
========================================
     SMART LIBRARY MANAGEMENT SYSTEM
========================================
1. Add Book
2. List Books
3. Search Books
4. Add Member
5. List Members
6. Issue Book
7. Return Book
8. Library Summary
9. Exit
========================================
""")


# ============================================================
# ADD BOOK
# ============================================================

def add_book(library):

    try:

        book_id = validate_non_empty(
            input("Enter Book ID: "),
            "Book ID"
        )

        title = validate_non_empty(
            input("Enter Title: "),
            "Title"
        )

        author = validate_non_empty(
            input("Enter Author: "),
            "Author"
        )

        category = validate_non_empty(
            input("Enter Category: "),
            "Category"
        )

        book = Book(
            book_id,
            title,
            author,
            category
        )

        print(library.add_book(book))

    except ValueError as error:
        print("Error:", error)


# ============================================================
# ADD MEMBER
# ============================================================

def add_member(library):

    try:

        member_id = validate_non_empty(
            input("Enter Member ID: "),
            "Member ID"
        )

        name = validate_non_empty(
            input("Enter Name: "),
            "Name"
        )

        phone = validate_non_empty(
            input("Enter Phone: "),
            "Phone"
        )

        member = Member(
            member_id,
            name,
            phone
        )

        print(library.add_member(member))

    except ValueError as error:
        print("Error:", error)


# ============================================================
# SEARCH BOOKS
# ============================================================

def search_books(library):

    try:

        keyword = validate_non_empty(
            input("Enter title/author/category: "),
            "Keyword"
        )

        result = library.search_books(keyword)

        if result:

            books = {
                book.book_id: book
                for book in result
            }

            print_books(books)

        else:

            print("No matching books found.")

    except ValueError as error:
        print("Error:", error)


# ============================================================
# ISSUE BOOK
# ============================================================

def issue_book(library):

    try:

        book_id = validate_non_empty(
            input("Enter Book ID: "),
            "Book ID"
        )

        member_id = validate_non_empty(
            input("Enter Member ID: "),
            "Member ID"
        )

        days = validate_positive_integer(
            input("Enter loan period in days: "),
            "Loan period"
        )

        print(
            library.issue_book(
                book_id,
                member_id,
                days
            )
        )

    except ValueError as error:
        print("Error:", error)


# ============================================================
# RETURN BOOK
# ============================================================

def return_book(library):

    try:

        book_id = validate_non_empty(
            input("Enter Book ID: "),
            "Book ID"
        )

        print(library.return_book(book_id))

    except ValueError as error:
        print("Error:", error)


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    books, members = load_data()

    library = Library(
        books,
        members
    )

    while True:

        show_menu()

        choice = input(
            "Enter your choice (1-9): "
        ).strip()

        if choice == "1":

            add_book(library)

        elif choice == "2":

            print_books(library.books)

        elif choice == "3":

            search_books(library)

        elif choice == "4":

            add_member(library)

        elif choice == "5":

            print_members(library.members)

        elif choice == "6":

            issue_book(library)

        elif choice == "7":

            return_book(library)

        elif choice == "8":

            print(library.summary())

        elif choice == "9":

            print(
                "Thank you for using "
                "Smart Library Management System."
            )

            break

        else:

            print("Invalid choice! Please enter 1-9.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()