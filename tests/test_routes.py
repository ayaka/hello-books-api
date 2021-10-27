
def test_get_all_books_with_no_records(client):
    response = client.get("/books")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_books_with_two_records(client, two_saved_books):
    response = client.get("/books")
    response_body = response.get_json()

    assert len(response_body) == 2


def test_get_one_book_with_no_record(client):
    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body is None


def test_get_one_book_with_id(client, two_saved_books):
    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }


def test_create_one_book(client):
    book = {
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

    response = client.post("/books", json=book)

    assert response.status_code == 201
