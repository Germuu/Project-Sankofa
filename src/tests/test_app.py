import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Project Sankofa' in response.data

def test_artifact_page(client):
    response = client.get('/artifact/1')  # Assuming an artifact with ID 1 exists
    assert response.status_code == 200
    assert b'Artifact Details' in response.data

def test_non_existent_artifact(client):
    response = client.get('/artifact/9999')  # Assuming no artifact with this ID exists
    assert response.status_code == 404

def test_interactive_map(client):
    response = client.get('/map')
    assert response.status_code == 200
    assert b'Interactive Map' in response.data