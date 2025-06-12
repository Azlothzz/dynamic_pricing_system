import React from 'react';
import { Line } from 'react-chartjs-2';

function SalesChart({ salesData }) {
  const data = {
    labels: salesData.map((data) => data.date),
    datasets: [
      {
        label: 'Units Sold',
        data: salesData.map((data) => data.units_sold),
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 2,
        fill: false,
      },
    ],
  };

  return <Line data={data} />;
}

export default SalesChart;