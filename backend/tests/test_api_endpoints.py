import unittest
import json
from app import app 

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_adjust_prices_endpoint(self):
        payload = [
            {
                "product_id": "P001",
                "base_price": 100.0,
                "inventory": 5,
                "cost_price": 80.0,
                "competitor_price": 90.0,
            }
        ]
        response = self.client.post(
            "/adjust-prices", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("adjusted_price", response.json[0])

    def test_predict_price_endpoint(self):
        payload = [
            {
                "base_price": 100.0,
                "inventory": 15,
                "sales_last_30_days": 120,
                "average_rating": 4.5,
                "competitor_price": 95.0,
                "avg_units_sold": 10.0
            }
        ]
        response = self.client.post(
            "/predict-price", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("predicted_price", response.json[0])

if __name__ == "__main__":
    unittest.main()