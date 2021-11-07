from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")
genre_bp = Blueprint("genre", __name__, url_prefix="/genres")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        new_book = Book(
            title = request_body["title"],
            description = request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} created", 201)

    elif request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()
        books_response = []
        for book in books:
            if book.author:
                author = book.author.name
            else:
                author = ""
            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description,
                    "author": author
                }
            )
        return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)

    if book is None:
        return make_response(f"Book #{book_id} not found", 404)

    if request.method == "PUT":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        book.title = request_body["title"]
        book.description = request_body["description"]

        db.session.commit()

        return make_response(f"Book #{book_id} successfully updated", 200)

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()

        return make_response(f"Book #{book_id} successfully deleted")

    elif request.method == "GET":
        return book.to_dict()

@books_bp.route("/<book_id>/assign_genres", methods=["PATCH"])
def handle_book_genres(book_id):
    book = Book.query.get(book_id)
    if not book:
        return make_response(f"Book #{book_id} not found", 404)

    request_body = request.get_json()
    if "genres" not in request_body:
        return make_response("Invalid Request", 400)

    for id in request_body["genres"]:
        book.genres.append(Genre.query.get(id))

    db.session.commit()

    return make_response("Genres successfully added", 200)


@authors_bp.route("", methods=["GET", "POST"])
def handle_authors():
    if request.method == "GET":
        authors = Author.query.all()
        response_body = [author.to_dict() for author in authors]
        return jsonify(response_body), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "name" not in request_body:
            return make_response("Invalid Request", 400)

        new_author = Author.from_dict(request_body)

        db.session.add(new_author)
        db.session.commit()

        return make_response(f"Author {new_author.name} created", 201)

@authors_bp.route("/<author_id>/books", methods=["GET", "POST"])
def handle_authors_books(author_id):
    author = Author.query.get(author_id)

    if author is None:
        return make_response("Author not found", 404)

    if request.method == "GET":
        response_body = [book.to_dict() for book in author.books]
        return jsonify(response_body), 200

    elif request.method == "POST":
        request_body = request.get_json()

        new_book = Book(title=request_body["title"], description=request_body["description"], author=author)

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)


@genre_bp.route("", methods=["GET", "POST"])
def handle_genres():
    if request.method == "GET":
        genres = Genre.query.all()
        response_body = [genre.to_dict() for genre in genres]
        return jsonify(response_body)

    elif request.method == "POST":
        request_body = request.get_json()

        if not request_body.get("name"):
            return jsonify("Invalid input"), 404

        new_genre = Genre.from_dict(request_body)

        db.session.add(new_genre)
        db.session.commit()

        return make_response(f"Genre {new_genre.name} created", 201)
