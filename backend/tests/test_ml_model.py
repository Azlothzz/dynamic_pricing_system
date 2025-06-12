import os
import unittest
import pickle
import pandas as pd  # Import pandas

class TestMLModel(unittest.TestCase):
    def setUp(self):
        # Adjust the path to the correct location of the model file
        model_path = os.path.join(os.path.dirname(__file__), "../../ml/price_prediction_model.pkl")
        print("Resolved model path:", model_path)  # Debugging: Print the resolved path

        # Load the model
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def test_model_prediction(self):
    # Mock input data with the exact features used during training
        input_data = pd.DataFrame(
            [
                {
                    "base_price": 100.0,
                    "inventory": 15,
                    "sales_last_30_days": 120,
                    "average_rating": 4.5,
                    "category": 0,  # Example numerical encoding for "Electronics"
                }
            ]
        )
        # Predict using the trained model
        prediction = self.model.predict(input_data)
        self.assertGreater(prediction[0], 0)  # Ensure positive price prediction