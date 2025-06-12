from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import joblib
import os
from utils.pricing_rules import apply_business_rules

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../ml/price_prediction_model.pkl")
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please train the model first.")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Root route
@app.route('/')
def index():
    return jsonify({"message": "Dynamic Pricing API is running!"})

# Adjust prices endpoint
@app.route('/adjust-prices', methods=['POST'])
def adjust_prices():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        adjusted_products = []
        for product in data:
            if not all(key in product for key in ["base_price", "inventory", "cost_price"]):
                return jsonify({"error": "Invalid input. Missing required fields."}), 400

            adjusted_price = apply_business_rules(
                base_price=product["base_price"],
                competitor_price=product.get("competitor_price"),
                inventory=product["inventory"],
                cost_price=product["cost_price"]
            )
            product["adjusted_price"] = adjusted_price
            product["sales_last_30_days"] = product.get("sales_last_30_days", 10)
            adjusted_products.append(product)

        return jsonify(adjusted_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Predict prices endpoint
@app.route('/predict-price', methods=['POST'])
def predict_price():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        df = pd.DataFrame(data)
        if "category" in df.columns:
            df["category"] = df["category"].astype("category").cat.codes
        else:
            return jsonify({"error": "Missing 'category' field in input data."}), 400

        features = df[["base_price", "inventory", "sales_last_30_days", "average_rating", "category"]]
        df["predicted_price"] = model.predict(features)

        return jsonify(df.to_dict(orient="records")), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)