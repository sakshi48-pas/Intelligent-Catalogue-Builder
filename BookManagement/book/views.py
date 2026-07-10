import json
import os

from flask import Blueprint, jsonify, request

mod = Blueprint('book', __name__, url_prefix='/book')

@mod.route('/', methods=['GET'])
def home():
    return "Book API Working"


from flask import Blueprint, jsonify, request

mod = Blueprint('book', __name__, url_prefix='/book')

# file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "data.json")

# load data
with open(file_path, 'r') as f:
    data = json.load(f)


# 📖 GET ALL BOOKS
@mod.route('/', methods=['GET'])
def get_books():
    return jsonify(data)


# ➕ ADD BOOK
@mod.route('/create/', methods=['POST'])
def add_book():
    book_data = request.get_json()

    if len(data) == 0:
        new_id = 1
    else:
        new_id = data[-1]['id'] + 1

    book = book_data.copy()
    book['id'] = new_id

    data.append(book)

    with open(file_path, 'w') as f:
        json.dump(data, f)

    return jsonify(book)


# 🔍 GET BOOK BY ID
@mod.route('/<int:id>/', methods=['GET'])
def get_book(id):
    for book in data:
        if book['id'] == id:
            return jsonify(book)

    return jsonify({"message": "Book not found"}), 404


# ✏️ UPDATE BOOK
@mod.route('/update/<int:id>/', methods=['PUT'])
def update_book(id):
    book_data = request.get_json()

    for book in data:
        if book['id'] == id:
            book["title"] = book_data.get("title", book["title"])
            book["author"] = book_data.get("author", book["author"])

            with open(file_path, 'w') as f:
                json.dump(data, f)

            return jsonify(book)

    return jsonify({"message": "Book not found"}), 404


# ❌ DELETE BOOK
@mod.route('/delete/<int:id>/', methods=['DELETE'])
def delete_book(id):
    for book in data:
        if book['id'] == id:
            data.remove(book)

            with open(file_path, 'w') as f:
                json.dump(data, f)

            return jsonify({"message": "Book deleted"})

    return jsonify({"message": "Book not found"}), 404