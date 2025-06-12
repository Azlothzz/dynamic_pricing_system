import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line, Bar } from "react-chartjs-2";

// Register required Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Charts = ({ salesData, competitorData }) => {
  // Line Chart: Sales Trends
  const salesTrendsData = {
    labels: salesData.map((entry) => entry.date),
    datasets: [
      {
        label: "Units Sold",
        data: salesData.map((entry) => entry.units_sold),
        borderColor: "rgba(75,192,192,1)",
        backgroundColor: "rgba(75,192,192,0.2)", // Area fill color
        fill: true,
        tension: 0.4, // Smooth curve
      },
    ],
  };

  const salesTrendsOptions = {
    responsive: true,
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: (context) => `Units Sold: ${context.raw.toFixed(0)}`,
        },
      },
      legend: {
        display: true,
        position: "top",
      },
    },
    interaction: {
      mode: "nearest", // Focus on nearest point
      intersect: true, // Only highlight the hovered point
    },
  };

  // Bar Chart: Competitor Pricing Comparison
  const competitorComparisonData = {
    labels: competitorData.map((entry) => entry.product_id),
    datasets: [
      {
        label: "Base Price",
        data: competitorData.map((entry) => entry.base_price),
        backgroundColor: "rgba(54,162,235,0.6)",
      },
      {
        label: "Adjusted Price",
        data: competitorData.map((entry) => entry.adjusted_price),
        backgroundColor: "rgba(75,192,192,0.6)",
      },
      {
        label: "Competitor Price",
        data: competitorData.map((entry) => entry.competitor_price),
        backgroundColor: "rgba(255,99,132,0.6)",
      },
    ],
  };

  const competitorComparisonOptions = {
    responsive: true,
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: (context) =>
            `${context.dataset.label}: $${context.raw.toFixed(2)}`,
        },
      },
      legend: {
        display: true,
        position: "top",
      },
    },
    interaction: {
      mode: "nearest", // Focus on nearest point
      intersect: true, // Only highlight the hovered point
    },
  };

  return (
    <div>
      {/* Sales Trends Chart */}
      <div style={{ marginBottom: "30px" }}>
        <h3>Sales Trends</h3>
        <Line data={salesTrendsData} options={salesTrendsOptions} />
      </div>

      {/* Competitor Pricing Comparison Chart */}
      <div style={{ marginBottom: "30px" }}>
        <h3>Competitor Pricing Comparison</h3>
        <Bar data={competitorComparisonData} options={competitorComparisonOptions} />
      </div>
    </div>
  );
};

export default Charts;