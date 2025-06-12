# Dynamic Pricing System

The **Dynamic Pricing System** is an end-to-end solution for real-time price optimization in an eCommerce platform. This system integrates advanced AI-driven decision-making, front-end and back-end development, and real-world business logic to dynamically adjust product prices based on historical sales, inventory levels, competitor pricing, and customer ratings.

---

## **Features**
1. **Dynamic Pricing Algorithm**
   - Adjust prices based on:
     - Historical sales trends (demand forecasting).
     - Inventory levels.
     - Competitor pricing.
     - Customer ratings and reviews.
   - Optimized to:
     - Maximize revenue.
     - Maintain competitive pricing.
     - Minimize excess inventory.

2. **Machine Learning Integration**
   - Uses SARIMA (Seasonal AutoRegressive Integrated Moving Average) for demand forecasting.
   - Considers seasonal trends and demand elasticity.

3. **Business Logic**
   - Overrides AI predictions when:
     - Inventory is critically low (prices increase).
     - Competitors undercut pricing (prices decrease while maintaining profit margins).
     - Customer ratings indicate high or low product popularity.

4. **Front-End Dashboard**
   - User-friendly interface for visualizing:
     - Product catalog, base prices, adjusted prices, and competitor prices.
     - Trends in sales, inventory, and pricing adjustments.

5. **Back-End API**
   - RESTful API for:
     - Fetching and updating product data.
     - Processing pricing adjustments.

6. **Scalability**
   - Designed to handle datasets with over 100,000 products efficiently.

---

## **System Architecture**
The system consists of the following components:

1. **Machine Learning (SARIMA)**
   - Trains a time-series model to predict future demand based on historical sales data.

2. **Back-End (Flask)**
   - Processes data and applies business rules to adjust prices dynamically.
   - Integrates competitor pricing via an API (or mock data).

3. **Front-End (React)**
   - Displays product pricing insights with interactive charts and tables.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or later
- Node.js v14 or later
- npm (Node Package Manager)
- pip (Python Package Manager)
- A modern web browser

---

### **2. Clone the Repository**
```bash
git clone https://github.com/your-repo/dynamic-pricing-system.git
cd dynamic-pricing-system
```

Backend setup:
1. Navigate to the backend directory
2. Create a virtual environment and activate it: python -m venv venv
.\venv\Scripts\activate
3. Install dependencies: pip install -r requirements.txt
4. Start the Flask server: python app.py

Frontend setup:
1. Navigate to the frontend directory
2. Install dependencies: npm install
3. Start the React development server: npm start

## **Testing**

Use tools like pytest for automated testing of the back-end logic
Front-end testing can be conducted using tools like React Testing Library or Jest.

1. **Back-End Testing**:
   - Run unit tests using `pytest`:
     ```bash
     pytest
     ```
   - Example tests:
     - Verify price adjustments based on inventory, demand, and competitor prices.
     - Ensure prices respect constraints (`cost price + 10%`, `base price + 50%`).

2. **Front-End Testing**:
   - Use React Testing Library or Jest:
     ```bash
     npm test
     ```
   - Example tests:
     - Ensure the dashboard renders correctly.
     - Validate API integration for data fetching.

## **API**

Endpoint: /adjust-prices-with-forecast
Method: POST
Description: Processes product data and returns adjusted prices based on demand forecasting, inventory, competitor pricing, and customer ratings.
Request Body
Example payload: [
  { "product_id": "P001", "base_price": 100.0, "inventory": 8, "average_rating": 4.6 },
  { "product_id": "P002", "base_price": 200.0, "inventory": 50, "average_rating": 4.0 },
  { "product_id": "P003", "base_price": 50.0, "inventory": 5, "average_rating": 2.8 }
]
Response: [
  {
    "product_id": "P001",
    "base_price": 100.0,
    "adjusted_price": 108.90,
    "competitor_price": 90.0,
    "forecasted_demand": 10,
    "inventory": 8,
    "average_rating": 4.6
  },
  {
    "product_id": "P002",
    "base_price": 200.0,
    "adjusted_price": 214.50,
    "competitor_price": 195.0,
    "forecasted_demand": 3,
    "inventory": 50,
    "average_rating": 4.0
  },
  {
    "product_id": "P003",
    "base_price": 50.0,
    "adjusted_price": 47.52,
    "competitor_price": 48.0,
    "forecasted_demand": 1,
    "inventory": 5,
    "average_rating": 2.8
  }
]

## **Error Handling**

- The API returns appropriate status codes for errors:
  - `400 Bad Request`: Invalid input data.
  - `500 Internal Server Error`: Server-side issues.
- Example Error Response:
  ```json
  {
    "error": "Invalid product data. Please check the input format."
  }

## **Machine Learning Pipeline**
Input:
Historical sales data (product_id, date, units_sold, price).
Model:
SARIMA (Seasonal AutoRegressive Integrated Moving Average) is trained on time-series sales data.
Output:
Forecasted demand for each product.