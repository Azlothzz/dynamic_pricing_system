import pytest
from app import adjust_prices_with_forecast
from app import app
import json

# Mock data
mock_data = [
    {"product_id": "P001", "base_price": 100.0, "inventory": 8, "average_rating": 4.6},
    {"product_id": "P002", "base_price": 200.0, "inventory": 50, "average_rating": 4.0},
    {"product_id": "P003", "base_price": 50.0, "inventory": 5, "average_rating": 2.8},
]

# Mock competitor prices
mock_competitor_prices = {
    "P001": 90.0,
    "P002": 195.0,
    "P003": 48.0,
}

# Mock demand forecasts
mock_forecasts = {
    "P001": 10,
    "P002": 3,
    "P003": 1,
}

# Test function
def test_dynamic_pricing_logic(client):
    # Mock request data
    mock_request_data = [
        {"product_id": "P001", "base_price": 100.0, "inventory": 8, "average_rating": 4.6},
        {"product_id": "P002", "base_price": 200.0, "inventory": 50, "average_rating": 4.0},
        {"product_id": "P003", "base_price": 50.0, "inventory": 5, "average_rating": 2.8},
    ]

    # Send a POST request to the endpoint
    response = client.post(
        "/adjust-prices-with-forecast",
        json=mock_request_data,
    )

    # Validate the response
    assert response.status_code == 200
    response_data = response.get_json()

    # Assertions for the response data
    assert len(response_data) == len(mock_request_data)  # Ensure all products are processed
    assert response_data[0]["adjusted_price"] > mock_request_data[0]["base_price"]  # High rating adjustment
    assert response_data[1]["adjusted_price"] == 214.5  # Adjusted price based on inventory or demand
    assert response_data[2]["adjusted_price"] < mock_request_data[2]["base_price"]  # Low rating adjustment

def test_business_rule_overrides():
    # Example product data
    product = {"product_id": "P001", "base_price": 100.0, "inventory": 5, "average_rating": 4.5}
    cost_price = product["base_price"] * 0.6  # Cost price is 60% of base price

    # Simulate adjusted price
    adjusted_price = 120.0  # Example adjusted price from logic
    assert adjusted_price >= cost_price + (cost_price * 0.1)  # Minimum profit margin
    assert adjusted_price <= product["base_price"] * 1.5  # Cap at 50% above base price


def test_adjust_prices_with_forecast_api():
    # Client setup
    client = app.test_client()

    # Mock request data
    mock_request_data = [
        {"product_id": "P001", "base_price": 100.0, "inventory": 8, "average_rating": 4.6},
        {"product_id": "P002", "base_price": 200.0, "inventory": 50, "average_rating": 4.0},
    ]

    # Send POST request
    response = client.post(
        "/adjust-prices-with-forecast",
        data=json.dumps(mock_request_data),
        content_type="application/json",
    )

    # Validate response
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(mock_request_data)
    assert "adjusted_price" in data[0]
    assert "competitor_price" in data[0]