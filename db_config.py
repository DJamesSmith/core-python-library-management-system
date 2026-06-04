import json
import os

FILE_NAME = "my_library.json"

def load_books():
        if not os.path.exists(FILE_NAME):
            return []
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

def save_books(book: list[dict]):
        with open(FILE_NAME, "w") as file:
            json.dump(book, file, indent = 4)