from flask import Flask, jsonify, request
import joblib
import pandas as pd
from flask_cors import CORS
from utils.pricing_rules import apply_business_rules  # Import the business rules function
from utils.forecasting import fetch_historical_sales, forecast_demand

app = Flask(__name__)
CORS(app)

# In-memory database for products
products_db = [
    {"product_id": "P001", "base_price": 100.0, "inventory": 15, "sales_last_30_days": 120, "average_rating": 4.5, "category": "Electronics"},
    {"product_id": "P002", "base_price": 200.0, "inventory": 50, "sales_last_30_days": 40, "average_rating": 4.0, "category": "Apparel"},
    {"product_id": "P003", "base_price": 50.0, "inventory": 5, "sales_last_30_days": 10, "average_rating": 3.8, "category": "Home"},
]

# Load the trained model
model = joblib.load('../ml/data/price_model.pkl')

@app.route('/')
def home():
    return "Welcome to the Dynamic Pricing System API!"

# Predict price endpoint
@app.route('/predict-price', methods=['POST'])
def predict_price():
    try:
        # Parse input JSON
        data = request.json
        print("Received data:", data)  # Debugging input payload

        df = pd.DataFrame(data)

        # Add missing calculated features
        df['price_elasticity'] = df['sales_last_30_days'] / df['base_price']
        print("DataFrame after adding price_elasticity:", df)

        # Define feature columns
        features = ['base_price', 'inventory', 'price_elasticity', 'average_rating', 'competitor_price', 'avg_units_sold']
        print("Features used for prediction:", features)

        # Predict prices
        predictions = model.predict(df[features])
        df['predicted_price'] = predictions

        print("Predicted prices:", df['predicted_price'])
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        print("Error occurred:", str(e))  # Debugging error
        return jsonify({"error": str(e)}), 400

# Adjust prices endpoint
@app.route('/adjust-prices', methods=['POST'])
def adjust_prices():
    """
    Processes pricing adjustments for a list of products.
    """
    try:
        # Get product data from the request
        data = request.get_json()  # Expecting a list of products
        adjusted_products = []

        for product in data:
            # Apply business rules to calculate adjusted price
            adjusted_price = apply_business_rules(
                base_price=product["base_price"],
                competitor_price=product.get("competitor_price"),
                inventory=product["inventory"],
                cost_price=product["cost_price"]
            )
            # Add the adjusted price to the product dictionary
            product["adjusted_price"] = adjusted_price
            adjusted_products.append(product)

        # Return the adjusted product data
        return jsonify(adjusted_products), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def apply_business_rules(base_price, competitor_price, inventory, cost_price, critical_inventory=10):
    """
    Adjusts the price of a product based on business rules.

    Args:
        base_price (float): The original price of the product.
        competitor_price (float): The price of the same product offered by a competitor.
        inventory (int): The current inventory level of the product.
        cost_price (float): The cost of the product.
        critical_inventory (int): The threshold below which inventory is considered low.

    Returns:
        float: The adjusted price after applying business rules.
    """
    # Start with the base price
    adjusted_price = base_price

    # Rule 1: Low Inventory - Increase price up to 30%
    if inventory < critical_inventory:
        adjusted_price = min(adjusted_price * 1.3, base_price * 1.5)
        print(f"Low inventory detected. Price increased to {adjusted_price:.2f}")

    # Rule 2: Competitor Undercuts Pricing - Reduce price up to 20%
    if competitor_price and competitor_price < adjusted_price:
        adjusted_price = max(adjusted_price * 0.8, competitor_price)
        print(f"Competitor undercut detected. Price reduced to {adjusted_price:.2f}")

    # Rule 3: Profit Margin Constraints
    min_price = cost_price * 1.1  # Cost price + 10%
    max_price = base_price * 1.5  # Base price + 50%
    adjusted_price = max(adjusted_price, min_price)
    adjusted_price = min(adjusted_price, max_price)

    print(f"Final adjusted price: {adjusted_price:.2f}")
    return adjusted_price

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Validate required fields
    required_fields = ["product_id", "base_price", "inventory", "sales_last_30_days", "average_rating", "category"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required."}), 400

    # Check if the product already exists
    for product in products_db:
        if product["product_id"] == data["product_id"]:
            return jsonify({"error": "Product with this product_id already exists."}), 400

    # Add the product to the in-memory database
    products_db.append(data)
    return jsonify({"message": "Product created successfully!", "product": data}), 201

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products_db}), 200

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    for product in products_db:
        if product["product_id"] == product_id:
            return jsonify({"product": product}), 200
    return jsonify({"error": "Product not found."}), 404

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()

    for product in products_db:
        if product["product_id"] == product_id:
            # Update only the fields provided
            product.update(data)
            return jsonify({"message": "Product updated successfully!", "product": product}), 200

    return jsonify({"error": "Product not found."}), 404

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    for product in products_db:
        if product["product_id"] == product_id:
            products_db.remove(product)
            return jsonify({"message": "Product deleted successfully!"}), 200
    return jsonify({"error": "Product not found."}), 404

import requests

@app.route('/adjust-prices-with-forecast', methods=['POST'])
def adjust_prices_with_forecast():
    """
    Adjust prices dynamically based on forecasted demand, inventory levels, competitor prices, and customer ratings.
    """
    try:
        # Receive product data from the request
        data = request.get_json()
        print("Received data:", data)  # Debug: Log incoming data
        adjusted_products = []
        critical_inventory_threshold = 10  # Example threshold
        profit_margin = 10 / 100  # Minimum profit margin (10%)

        # Simulate competitor prices (mock data)
        competitor_prices = {
            "P001": 90.0,
            "P002": 195.0,
            "P003": 48.0
        }

        # Process each product
        for product in data:
            product_id = product['product_id']
            base_price = product['base_price']
            inventory = product.get('inventory', 0)
            average_rating = product.get('average_rating', 0)  # Default to 0 if not provided
            cost_price = base_price * 0.6  # Assume cost price is 60% of base price

            # Fetch historical sales data
            historical_sales = fetch_historical_sales(product_id)

            # Forecast demand
            forecasted_demand = forecast_demand(historical_sales, forecast_steps=1).iloc[0]

            # Default adjusted price
            adjusted_price = base_price

            # Adjust for low inventory
            if inventory < critical_inventory_threshold:
                adjusted_price = base_price * 1.3

            # Adjust for high demand
            elif forecasted_demand > 10:
                adjusted_price = base_price * 1.2

            # Adjust for competitor prices
            competitor_price = competitor_prices.get(product_id)
            if competitor_price and competitor_price < base_price:
                adjusted_price = max(competitor_price + (competitor_price * profit_margin), cost_price + (cost_price * profit_margin))

            # Adjust for customer ratings
            if average_rating >= 4.5:  # Highly rated product
                adjusted_price *= 1.1  # Increase price by 10%
            elif average_rating < 3.0:  # Poorly rated product
                adjusted_price *= 0.9  # Decrease price by 10%

            # Add product adjustments
            product['forecasted_demand'] = forecasted_demand
            product['adjusted_price'] = round(adjusted_price, 2)  # Round to 2 decimal places
            product['competitor_price'] = competitor_price if competitor_price else "N/A"
            adjusted_products.append(product)

        return jsonify(adjusted_products), 200

    except Exception as e:
        import traceback
        print("Error occurred:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)