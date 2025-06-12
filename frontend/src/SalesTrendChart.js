import React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

const salesData = [
    { date: '2024-10-01', units_sold: 5 },
    { date: '2024-10-02', units_sold: 10 },
    { date: '2024-10-03', units_sold: 8 },
];

const SalesTrendChart = () => (
    <div>
        <h2>Sales Trend</h2>
        <LineChart width={600} height={300} data={salesData}>
            <Line type="monotone" dataKey="units_sold" stroke="#8884d8" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
        </LineChart>
    </div>
);

export default SalesTrendChart;