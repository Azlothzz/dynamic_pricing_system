import pandas as pd
import joblib

# Load Data
product_catalog = pd.read_csv("data/product_catalog.csv")
competitor_prices = pd.read_csv("data/competitor_prices.csv")
sales_data = pd.read_csv("data/sales_data.csv")

# Merge Competitor Prices with Product Data
product_catalog = product_catalog.merge(competitor_prices, on="product_id", how="left")
product_catalog["competitor_price"] = product_catalog["competitor_price"].fillna(product_catalog["base_price"])

# Feature Engineering
product_catalog["price_elasticity"] = product_catalog["sales_last_30_days"] / product_catalog["base_price"]

# Calculate Historical Sales Trends
sales_data["date"] = pd.to_datetime(sales_data["date"])
sales_summary = sales_data.groupby("product_id")["units_sold"].mean().reset_index()
sales_summary.rename(columns={"units_sold": "avg_units_sold"}, inplace=True)

# Merge Historical Trends with Product Data
product_catalog = product_catalog.merge(sales_summary, on="product_id", how="left")

# Select Features for Prediction
features = ["base_price", "inventory", "price_elasticity", "average_rating", "competitor_price", "avg_units_sold"]

# Load Trained Model
price_model = joblib.load("data/price_model.pkl")

# Predict Prices
product_catalog["predicted_price"] = price_model.predict(product_catalog[features])

# Apply Business Rules
def apply_business_rules(row):
    predicted_price = row["predicted_price"]

    # Adjust based on inventory levels
    if row["inventory"] < 10:
        predicted_price += predicted_price * 0.3  # Increase by 30%

    # Adjust based on competitor pricing
    if row["competitor_price"] < predicted_price:
        predicted_price = max(row["competitor_price"] * 0.95, row["base_price"] * 1.1)  # Undercut by 5%

    # Ensure the price is within bounds
    min_price = row["base_price"] * 1.1  # Minimum price is 10% above base price
    max_price = row["base_price"] * 1.5  # Maximum price is 50% above base price
    final_price = max(min(predicted_price, max_price), min_price)

    return final_price

product_catalog["adjusted_price"] = product_catalog.apply(apply_business_rules, axis=1)

# Save Adjusted Prices
product_catalog[["product_id", "base_price", "predicted_price", "adjusted_price"]].to_csv("data/adjusted_prices.csv", index=False)

print("Adjusted prices saved to data/adjusted_prices.csv!")