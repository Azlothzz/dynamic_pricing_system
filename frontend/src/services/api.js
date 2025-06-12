import axios from 'axios';

// Define the base URL for your Flask back-end
const API_BASE_URL = 'http://127.0.0.1:5000'; // Adjust if the back-end is hosted elsewhere

// Function to fetch adjusted prices
const fetchAdjustedPrices = async () => {
    try {
        const payload = [
            { product_id: 'P001', base_price: 100.0, inventory: 15, cost_price: 80.0, competitor_price: 90.0 },
            { product_id: 'P002', base_price: 200.0, inventory: 5, cost_price: 150.0, competitor_price: 195.0 },
            { product_id: 'P003', base_price: 50.0, inventory: 3, cost_price: 30.0, competitor_price: 48.0 },
        ];
        console.log('Payload:', payload); // Log the payload
        const response = await axios.post(`${API_BASE_URL}/adjust-prices`, payload);
        return response.data;
    } catch (error) {
        console.error('Error fetching adjusted prices:', error);
        throw error;
    }
};

export default fetchAdjustedPrices;