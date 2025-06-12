import React, { useEffect, useState } from "react";
import { fetchAdjustedPrices } from "../services/api"; // Import the API function

const ProductTable = () => {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getPrices = async () => {
      try {
        const data = await fetchAdjustedPrices(); // Call the API function
        setProducts(data); // Update the state with the adjusted prices
      } catch (err) {
        setError("Failed to fetch adjusted prices.");
      }
    };

    getPrices();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Product Prices</h1>
      <table>
        <thead>
          <tr>
            <th>Product ID</th>
            <th>Base Price</th>
            <th>Adjusted Price</th>
            <th>Inventory</th>
            <th>Sales Last 30 Days</th>
            <th>Average Rating</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.product_id}>
              <td>{product.product_id}</td>
              <td>{product.base_price}</td>
              <td>{product.adjusted_price}</td>
              <td>{product.inventory}</td>
              <td>{product.sales_last_30_days}</td>
              <td>{product.average_rating}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProductTable;