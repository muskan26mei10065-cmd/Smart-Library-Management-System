# Smart Library Management System

A menu-driven Library Management System built in Python.

## Features
- Add, list and search books
- Register and list members
- Issue and return books
- Automatic due-date calculation
- Library summary
- JSON-based persistent storage
- Input validation and error handling
- Unit tests

## Project Structure
```text
Smart_Library_Management_System/
├── main.py
├── library_data.json        # created automatically after data is added
├── README.md
├── Project_Report.pdf
├── Project_Documentation.pdf
└── tests/
    └── test_library.py
```

## Requirements
- Python 3.9 or later
- No external Python packages are required

## Run the Application
Open Terminal / Command Prompt in this folder:

```bash
python main.py
```

Then use the menu:
1. Add Book
2. List Books
3. Search Books
4. Add Member
5. List Members
6. Issue Book
7. Return Book
8. Library Summary
9. Exit

## Run Unit Tests
From the project folder:

```bash
python -m unittest discover -s tests -v
```

## Notes
`library_data.json` is created/updated automatically when books or members are added and when issue/return operations change records.
