from datetime import datetime
from copy import copy, deepcopy
from db_config import load_books, save_books

def parse(date_str: str):
    return datetime.strptime(date_str, "%d-%m-%Y").date()

class LibraryManagementSystem:
    def __init__(self):
        pass

    def add_book(self):
        books: list[dict] = load_books()
        title = input("Book title: ")

        for book in books:
            if book["book_name"].lower() == title.lower():
                book["available_copies"] += 1
                save_books(books)
                print("Book already exists. Added one more copy.")
                return

        author = input("Author: ")
        genre = input("Genre: ")

        print("\nBook Type\n1. Normal\n2. Rare\n3. Reference")
        ch = int(input("Choice: "))

        book_type = "NORMAL"
        if ch == 2:
            book_type = "RARE"
        elif ch == 3:
            book_type = "REFERENCE"

        new_id = 1
        if books:
            new_id = max(book["id"] for book in books) + 1

        new_book = {
            "id": new_id,
            "book_name": title,
            "author": author,
            "genre": genre,
            "availability_status": True,
            "available_copies": 1,
            "book_type": book_type,
            "borrow_count": 0,
            "borrowing_history": []
        }

        books.append(new_book)
        save_books(books)
        print("Book added successfully.")

    def display_inventory(self):
        books: list[dict] = load_books()

        if not books:
            print("No books available.")
            return
        print("-" * 20)

        for book in books:
            print(f"ID\t\t: {book['id']}")
            print(f"Title\t\t: {book['book_name']}")
            print(f"Author\t\t: {book['author']}")
            print(f"Genre\t\t: {book['genre']}")
            print(f"Type\t\t: {book['book_type']}")
            print(f"Copies\t\t: {book['available_copies']}")
            print(f"Borrowed\t: {book['borrow_count']}")
            print(f"Available\t: {book['availability_status']}")
            print("-" * 20)

    def retrieve_borrowing_history(self):
        books: list[dict] = load_books()
        title = input("Book title: ")

        for book in books:
            if book["book_name"].lower() == title.lower():
                history = book["borrowing_history"]

                if not history:
                    print("No borrowing history found.")
                    return

                for record in history:
                    print("-" * 20)
                    print(f"borrower_name: {record['borrower_name']}\nissue_date: {record['issue_date']}\ndue_date: {record['due_date']}\nreturn_date: {record['due_date']}")

                return

        print("Book not found.")

    def issue_book(self):
        books: list[dict] = load_books()
        title = input("Book title: ")
        # 1. if borrower has returned the book they must be return the book before borrowing again, they cannot borrow multiple copies of the same book.
        # 2. checks if due date is after issue date, it should not allow to enter wrong dates.
        #    because it does not make sense that you borrow today and due date is 5 months ago. it should be future date.

        for book in books:
            if book["book_name"].lower() == title.lower():
                if book["book_type"] in ["RARE", "REFERENCE"]:
                    print("This book is protected and cannot be issued.")
                    return

                if book["available_copies"] <= 0:
                    print("No copies available.")
                    return

                borrower_name = input("Borrower name: ")
                for borrower in book["borrowing_history"]:
                    if borrower["borrower_name"] == borrower_name and borrower["return_date"] is None:
                        print(f"{borrower_name} already has 1 copy. Due date: {borrower['due_date']}")
                        return

                try:
                    issue_date = parse(input("Issue date (DD-MM-YYYY): "))
                    due_date = parse(input("Due date (DD-MM-YYYY): "))
                except ValueError:
                    print("Invalid date format.")
                    return

                today = datetime.today().date()
                if issue_date > today:
                    print("Issue date cannot be in the future.")
                    return

                if due_date <= issue_date:
                    print("Due date must be after issue date.")
                    return

                history_record = {
                    "borrower_name": borrower_name,
                    "issue_date": issue_date.strftime("%d-%m-%Y"),
                    "due_date": due_date.strftime("%d-%m-%Y"),
                    "return_date": None
                }

                book["borrowing_history"].append(history_record)
                book["available_copies"] -= 1
                book["borrow_count"] += 1
                if book["available_copies"] == 0:
                    book["availability_status"] = False

                save_books(books)
                print("Book issued successfully.")
                return

        print("Book not found.")

    def return_book(self):
        books: list[dict] = load_books()
        title = input("Book title: ")
        borrower_name = input("Borrower name: ")

        for book in books:
            if book["book_name"].lower() == title.lower():
                for history in book["borrowing_history"]:
                    if (history["borrower_name"] == borrower_name and history["return_date"] is None):
                        history["return_date"] = datetime.today().strftime("%d-%m-%Y")
                        book["available_copies"] += 1
                        book["availability_status"] = True

                        save_books(books)
                        print("Book returned.")
                        return

        print("Record not found.")

    def check_books_overdue(self):
        books: list[dict] = load_books()
        today = datetime.today().date()
        found: bool = False

        for book in books:
            for history in book["borrowing_history"]:
                if history["return_date"] is not None:
                    continue

                try:
                    due_date = parse(history["due_date"])
                except ValueError:
                    print(f"Invalid due date found for {book['book_name']}")
                    continue

                if today > due_date:
                    found = True

                    print(f"Book: {book['book_name']}\nBorrower: {history['borrower_name']}\nDue Date: {history['due_date']}\n")

        if not found:
            print("No overdue books.")

    def search_book(self):
        books: list[dict] = load_books()
        search_text = input("Enter title to search: ").lower()
        found: bool = False

        for book in books:
            if search_text in book["book_name"].lower():
                found = True
                print(f"{book['book_name']} | {book['author']} | {book['genre']}")

        if not found:
            print("Book not found.")

    def update_inventory(self):
        books: list[dict] = load_books()
        title = input("Book title to update: ")

        for book in books:
            if book["book_name"].lower() == title.lower():
                if book["book_type"] in ["RARE", "REFERENCE"]:
                    print("Protected book. Cannot modify.")
                    return

                book["author"] = input("New author: ")
                book["genre"] = input("New genre: ")

                save_books(books)
                print("Inventory updated.")
                return

        print("Book not found.")

    def analyze_genre_count(self):
        books: list[dict] = load_books()

        if not books:
            print("No books available.")
            return

        genre_counter: dict = {}
        for book in books:
            genre = book["genre"]
            genre_counter[genre] = (genre_counter.get(genre, 0) + 1)

        highest_genre = max(genre_counter, key = genre_counter.get)
        print("\nGenre Counts")
        for genre, count in genre_counter.items():
            print(f"{genre}: {count}")

        print(f"\nMost common genre: {highest_genre}")

    def show_most_borrowed_book(self):
        books: list[dict] = load_books()

        if not books:
            print("No books available.")
            return

        most_borrowed = max(books, key = lambda book: book["borrow_count"])
        print("\nMost Borrowed Book")
        print(f"{most_borrowed['book_name']} ({most_borrowed['borrow_count']} times)")

    def copy_demonstration(self):
        books: list[dict] = load_books()

        if not books:
            print("Add books first.")
            return

        shallow_copy: list[dict] = copy(books)
        deep_copy: list[dict] = deepcopy(books)

        print("\n----- ADDRESS OF LISTS -----")
        print(f"Original List\t: {id(books)}")
        print(f"Shallow List\t: {id(shallow_copy)}")
        print(f"Deep List\t: {id(deep_copy)}")

        print("\n----- ADDRESS OF FIRST DICTIONARY -----")
        print(f"Original Dict\t: {id(books[0])}")
        print(f"Shallow Dict\t: {id(shallow_copy[0])}")
        print(f"Deep Dict\t: {id(deep_copy[0])}")

        print("\n----- BEFORE MODIFICATION -----")
        print(f"Original\t: {books[0]['book_name']}")
        print(f"Shallow\t\t: {shallow_copy[0]['book_name']}")
        print(f"Deep\t\t: {deep_copy[0]['book_name']}")

        books[0]["book_name"] = "MODIFIED BY ORIGINAL"

        print("\n----- AFTER MODIFICATION -----")
        print(f"Original\t: {books[0]['book_name']}")
        print(f"Shallow\t\t: {shallow_copy[0]['book_name']}")
        print(f"Deep\t\t: {deep_copy[0]['book_name']}")

        print("\n----- OBSERVATION -----")
        print("Shallow copy address changed because both lists refer to the same dictionary object.")
        print("Deep copy address did not change because it contains independent dictionary objects.")

if __name__ == "__main__":
    obj: LibraryManagementSystem = LibraryManagementSystem()

    while True:
        print("\n------ Library Management System ------\n")
        print("1. Add book\n" \
        "2. Display all books\n" \
        "3. Retrieve borrowing history\n" \
        "4. Issue book\n" \
        "5. Return book\n" \
        "6. Check books overdue\n" \
        "7. Search book (partial title allowed)\n" \
        "8. Update inventory\n" \
        "9. Analyze genre count\n" \
        "10. Show most borrowed book\n" \
        "11. Copy demonstrate\n" \
        "12. Terminate")

        try:
            ch: int = int(input("Enter choice: "))
        except ValueError:
            print("Enter valid choice")
            continue

        match ch:
            case 1: obj.add_book()
            case 2: obj.display_inventory()
            case 3: obj.retrieve_borrowing_history()
            case 4: obj.issue_book()
            case 5: obj.return_book()
            case 6: obj.check_books_overdue()
            case 7: obj.search_book()
            case 8: obj.update_inventory()
            case 9: obj.analyze_genre_count()
            case 10: obj.show_most_borrowed_book()
            case 11: obj.copy_demonstration()
            case 12:
                print("\nProgram terminated.")
                break
            case _:
                print("invalid choice. Try choices 1 to 7.")

# NOTE:
# 0. return book - extra feature
# 1. sample data added in JSON file for testing.
# 2. valid dates should work only, cannot be that you borrow today and due date is 5 months ago. doesn't make sense.
# 3. Flaw: Since this is NOT a production system, IDs are auto-generated but for each dict book_name is used as the PRIMARY KEY being unique for each book. Not the ID.

# library list[dict] data-structure:
# [
#     {
#         "book_name": "Atomic Habits",
#         "author": "James Clear",
#         "genre": "Self-Help",
#         "availability_status": true,
#         "available_copies": 1,
#         "book_type": "Paperback",             ------ RARE, REFERENCE, Paperback, Hardcover
#         "borrow_count": 0,
#         "borrowing_history": []
#     },
# ]

# borrowing_history list[dict] data-structure
# "borrowing_history": [
#     {
#         "borrower_name": "Spriha",
#         "issue_date": "2026-06-03",
#         "due_date": "2026-03-04",
#         "return_date": null
#     }
# ]