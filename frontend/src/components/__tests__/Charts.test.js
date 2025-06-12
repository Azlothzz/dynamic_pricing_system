import React from 'react';
import { render, screen } from '@testing-library/react';
import Charts from '../Charts';

test('renders sales trends chart', () => {
  const salesData = [
    { date: '2023-01-01', sales: 100 },
    { date: '2023-01-02', sales: 120 },
  ];
  const competitorData = [
    { product_id: 'P001', competitor_price: 90 },
    { product_id: 'P002', competitor_price: 110 },
  ];

  render(<Charts salesData={salesData} competitorData={competitorData} />);

  expect(screen.getByText('Sales Trends')).toBeInTheDocument();
  expect(screen.getByText('Competitor Pricing Comparison')).toBeInTheDocument();
});