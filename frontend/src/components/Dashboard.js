import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch product data from the back-end API
    const fetchData = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/adjust-prices-with-forecast', [
                { product_id: 'P001', base_price: 100.0, inventory: 8, average_rating: 4.6 },
                { product_id: 'P002', base_price: 200.0, inventory: 50, average_rating: 4.0 },
                { product_id: 'P003', base_price: 50.0, inventory: 5, average_rating: 2.8 },
            ]);
            setProducts(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);  // Log error
        }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  // Prepare data for the bar chart
  const chartData = {
    labels: products.map((product) => product.product_id),
    datasets: [
      {
        label: 'Base Price',
        data: products.map((product) => product.base_price),
        backgroundColor: 'rgba(75,192,192,0.6)',
      },
      {
        label: 'Adjusted Price',
        data: products.map((product) => product.adjusted_price),
        backgroundColor: 'rgba(153,102,255,0.6)',
      },
      {
        label: 'Competitor Price',
        data: products.map((product) => product.competitor_price || 0),
        backgroundColor: 'rgba(255,99,132,0.6)',
      },
    ],
  };

  return (
    <div>
      <h1>Dynamic Pricing Dashboard</h1>
      {/* Bar Chart */}
      <Bar data={chartData} />

      {/* Product Table */}
      <table>
        <thead>
            <tr>
                <th>Product ID</th>
                <th>Base Price</th>
                <th>Adjusted Price</th>
                <th>Competitor Price</th>
                <th>Forecasted Demand</th>
                <th>Inventory</th>
                <th>Average Rating</th>
            </tr>
        </thead>
        <tbody>
            {products.map((product) => (
                <tr key={product.product_id}>
                    <td>{product.product_id}</td>
                    <td>${product.base_price.toFixed(2)}</td>
                    <td>${product.adjusted_price.toFixed(2)}</td>
                    <td>{product.competitor_price === "N/A" ? "N/A" : `$${product.competitor_price.toFixed(2)}`}</td>
                    <td>{product.forecasted_demand}</td>
                    <td>{product.inventory}</td>
                    <td>{product.average_rating}</td>
                </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;