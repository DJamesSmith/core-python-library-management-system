# Library Management System

A console-based Library Management System built using Python. The application allows librarians to manage book inventories, issue and return books, track borrowing history, identify overdue books, analyze genre statistics, and demonstrate shallow vs deep copy behavior. Data is stored persistently using JSON files.

## Features

### Book Management

* Add new books to the library inventory.
* Automatically increase available copies when an existing book is added again.
* Store book details including:

  * ID
  * Title
  * Author
  * Genre
  * Availability Status
  * Available Copies
  * Book Type

### Book Types

The system supports three types of books:

* **NORMAL**
* **RARE**
* **REFERENCE**

Rare and Reference books are protected and:

* Cannot be issued.
* Cannot be modified through inventory updates.

### Borrowing System

* Issue books to borrowers.
* Prevent a borrower from borrowing the same book multiple times before returning it.
* Validate issue and due dates.
* Prevent future issue dates.
* Track borrowing count for each book.

### Return Books

* Return previously issued books.
* Automatically update available copies.
* Restore availability status.

### Borrowing History

Maintain complete borrowing records including:

* Borrower Name
* Issue Date
* Due Date
* Return Date

### Overdue Book Detection

Identify books that:

* Have not been returned.
* Have crossed their due date.

### Search Functionality

Search books using:

* Full title
* Partial title

### Genre Analysis

Analyze the inventory and determine:

* Number of books per genre.
* Most common genre.

### Most Borrowed Book

Determine the book with the highest borrowing count.

### Shallow vs Deep Copy Demonstration

Demonstrates:

* Memory addresses of original, shallow copy, and deep copy objects.
* How modifications affect shallow copies.
* Why deep copies remain independent.

### Persistent Storage

Data is stored in JSON files, allowing records to persist across program executions.

---

## Technologies Used

* Python 3
* JSON
* datetime
* copy module

---

## Project Structure

```text
library_management_system/
│
├── library_management_system.py
├── db_config.py
├── books.json
└── README.md
```

---

## Data Structure

### Book Record

```python
{
    "id": 1,
    "book_name": "Atomic Habits",
    "author": "James Clear",
    "genre": "Self-Help",
    "availability_status": True,
    "available_copies": 3,
    "book_type": "NORMAL",
    "borrow_count": 5,
    "borrowing_history": []
}
```

### Borrowing History Record

```python
{
    "borrower_name": "Dion",
    "issue_date": "04-06-2026",
    "due_date": "18-06-2026",
    "return_date": None
}
```

---

## Menu Options

```text
1. Add Book
2. Display All Books
3. Retrieve Borrowing History
4. Issue Book
5. Return Book
6. Check Books Overdue
7. Search Book
8. Update Inventory
9. Analyze Genre Count
10. Show Most Borrowed Book
11. Copy Demonstration
12. Terminate
```

---

## Key Concepts Demonstrated

* Lists
* Dictionaries
* Nested Data Structures
* File Handling
* JSON Serialization
* Functions
* Classes and Objects
* Date Validation
* Exception Handling
* Shallow Copy
* Deep Copy
* Searching
* Aggregation and Analytics

---

## Future Improvements

* Database integration (PostgreSQL / MySQL)
* User authentication
* Fine calculation for overdue books
* Book reservation system
* ISBN support
* Advanced reporting
* GUI using Tkinter or PyQt
* REST API using Django REST Framework

---

## Author

Dion James Smith

Python-based Library Management System developed as a case study to practice data structures, file handling, object-oriented programming, and real-world business logic implementation.
