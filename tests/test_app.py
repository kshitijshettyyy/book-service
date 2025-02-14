# tests/test_app.py
import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert isinstance(response.json['books'], list)

def test_add_book(client):
    data = {'title': 'New Book', 'author': 'New Author'}
    response = client.post('/books', json=data)
    assert response.status_code == 201
    assert response.json['book']['title'] == 'New Book'