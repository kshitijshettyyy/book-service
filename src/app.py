# src/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory storage
books = [
    {"id": 1, "title": "Book One", "author": "kshitij"},
    {"id": 2, "title": "Book Two", "author": "Author Two"}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": books})

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if book is None:
        return jsonify({"message": "Book not found"}), 404
    return jsonify({"book": book})

@app.route('/books', methods=['POST'])
def add_book():
    new_book = {
        "id": len(books) + 1,
        "title": request.json["title"],
        "author": request.json["author"]
    }
    books.append(new_book)
    return jsonify({"book": new_book}), 201

if __name__ == '__main__':
    app.run(debug=True)