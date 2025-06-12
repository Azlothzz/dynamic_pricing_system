import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import os
import logging

logging.basicConfig(level=logging.ERROR)

def forecast_demand(historical_sales, forecast_steps=7):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import numpy as np
    import logging

    logging.basicConfig(level=logging.ERROR)

    try:
        # Validate input
        if historical_sales.empty:
            print("Historical sales data is empty. Returning zeros.")
            return np.zeros(forecast_steps)

        print(f"Input to SARIMA model for forecasting:\n{historical_sales}")

        # Fit SARIMA model
        model = SARIMAX(historical_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
        model_fit = model.fit(disp=False)

        # Forecast future demand
        forecast = model_fit.forecast(forecast_steps)
        print(f"Forecasted demand: {forecast}")
        return forecast

    except Exception as e:
        logging.error(f"Error in forecasting: {e}")
        return np.zeros(forecast_steps)

def fetch_historical_sales(product_id):

    try:
        # Get the absolute path to the sales_data.csv file
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Path to `forecasting.py`
        sales_data_path = os.path.join(base_dir, '../../ml/data/sales_data.csv')

        if not os.path.exists(sales_data_path):
            raise FileNotFoundError(f"The file '{sales_data_path}' does not exist.")

        # Read the sales data from the CSV file
        sales_data = pd.read_csv(sales_data_path)

        # Filter the rows corresponding to the given product_id
        product_data = sales_data[sales_data['product_id'] == product_id]

        # Check if data exists for the product_id
        if product_data.empty:
            print(f"No historical sales data found for product_id {product_id}.")
            return pd.Series(dtype=float)

        # Convert to a time-series indexed by date
        product_series = pd.Series(
            product_data['units_sold'].values,
            index=pd.to_datetime(product_data['date'])
        )
        product_series.index = product_series.index.to_period('D').to_timestamp()  # Set frequency

        print(f"Fetched data for {product_id}:\n{product_series}")
        return product_series

    except Exception as e:
        print(f"Error fetching sales data for product_id {product_id}: {e}")
        return pd.Series(dtype=float)