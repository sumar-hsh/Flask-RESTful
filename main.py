from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Sample data for books
books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

# Helper function to find book by ID
def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)

# Book Resource with CRUD operations
class Book(Resource):
    # Read a single book by ID
    def get(self, book_id):
        book = find_book(book_id)
        return book if book else ({"message": "Book not found"}, 404)

    # Update a book by ID
    def put(self, book_id):
        book = find_book(book_id)
        if book:
            data = request.get_json()
            book.update({"title": data["title"], "author": data["author"]})
            return book, 200
        return {"message": "Book not found"}, 404

    # Delete a book by ID
    def delete(self, book_id):
        global books
        books = [book for book in books if book["id"] != book_id]
        return {"message": "Book deleted"}, 200

class BookList(Resource):
    # Get all books
    def get(self):
        return books, 200

    # Create a new book
    def post(self):
        data = request.get_json()
        new_book = {
            "id": len(books) + 1,
            "title": data["title"],
            "author": data["author"]
        }
        books.append(new_book)
        return new_book, 201

# Route setup
api.add_resource(BookList, "/books")
api.add_resource(Book, "/books/<int:book_id>")

if __name__ == "__main__":
    app.run()
