
from app import app

def client():
    with app.test_client() as client:
        yield client

def test_adjust_prices(client):
    response = client.post('/adjust-prices')
    assert response.status_code == 200
    assert isinstance(response.json, list)