import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle

# Load the dataset
product_catalog = [
    {"product_id": "P001", "base_price": 100.0, "inventory": 15, "sales_last_30_days": 120, "average_rating": 4.5, "category": "Electronics"},
    {"product_id": "P002", "base_price": 200.0, "inventory": 50, "sales_last_30_days": 40, "average_rating": 4.0, "category": "Apparel"},
    {"product_id": "P003", "base_price": 50.0, "inventory": 5, "sales_last_30_days": 10, "average_rating": 3.8, "category": "Home"}
]

sales_data = [
    {"product_id": "P001", "date": "2024-10-01", "units_sold": 5, "price": 95.0},
    {"product_id": "P001", "date": "2024-10-02", "units_sold": 10, "price": 90.0},
    {"product_id": "P002", "date": "2024-10-01", "units_sold": 3, "price": 190.0},
    {"product_id": "P003", "date": "2024-10-01", "units_sold": 1, "price": 48.0}
]

# Convert product catalog and sales data to DataFrames
catalog_df = pd.DataFrame(product_catalog)
sales_df = pd.DataFrame(sales_data)

# Merge datasets
merged_df = pd.merge(sales_df, catalog_df, on="product_id")

# Encode categories numerically
merged_df["category"] = merged_df["category"].astype("category").cat.codes

# Features and target
X = merged_df[["base_price", "inventory", "sales_last_30_days", "average_rating", "category"]]
y = merged_df["price"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model
with open("price_prediction_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved as price_prediction_model.pkl")