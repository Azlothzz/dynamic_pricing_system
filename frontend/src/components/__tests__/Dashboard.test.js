import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import Dashboard from '../Dashboard';

const mock = new MockAdapter(axios);

describe('Dashboard Component', () => {
  beforeEach(() => {
    mock.reset();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('fetches and displays product data', async () => {
    const mockResponse = [
      { product_id: 'P001', base_price: 100.0, adjusted_price: 108.9, competitor_price: 90.0, inventory: 8, forecasted_demand: 10, average_rating: 4.6 },
      { product_id: 'P002', base_price: 200.0, adjusted_price: 214.5, competitor_price: 195.0, inventory: 50, forecasted_demand: 3, average_rating: 4.0 },
      { product_id: 'P003', base_price: 50.0, adjusted_price: 47.5, competitor_price: 48.0, inventory: 5, forecasted_demand: 1, average_rating: 2.8 },
    ];

    mock.onPost('http://127.0.0.1:5000/adjust-prices-with-forecast').reply(200, mockResponse);

    await act(async () => {
      render(<Dashboard />);
    });

    await waitFor(() => {
      expect(screen.getByText('P001')).toBeInTheDocument();
      expect(screen.getByText('$108.90')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    mock.onPost('http://127.0.0.1:5000/adjust-prices-with-forecast').reply(500);

    await act(async () => {
      render(<Dashboard />);
    });

    await waitFor(() => {
      expect(screen.getByText('Error fetching data')).toBeInTheDocument();
    });
  });

  test('displays loading state initially', async () => {
    mock.onPost('http://127.0.0.1:5000/adjust-prices-with-forecast').reply(200, []);

    await act(async () => {
      render(<Dashboard />);
    });

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('handles empty response', async () => {
    mock.onPost('http://127.0.0.1:5000/adjust-prices-with-forecast').reply(200, []);

    await act(async () => {
      render(<Dashboard />);
    });

    await waitFor(() => {
      expect(screen.getByText('No data available')).toBeInTheDocument();
    });
  });
});