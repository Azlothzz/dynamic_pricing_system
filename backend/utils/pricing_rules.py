def apply_business_rules(base_price, competitor_price, inventory, cost_price, critical_inventory=10):

    adjusted_price = base_price

    # Rule 1: Low Inventory - Increase price up to 30%
    if inventory < critical_inventory:
        adjusted_price = min(adjusted_price * 1.3, base_price * 1.5)

    # Rule 2: Competitor Undercuts Pricing - Reduce price up to 20%
    if competitor_price and competitor_price < adjusted_price:
        adjusted_price = max(adjusted_price * 0.8, competitor_price)

    # Rule 3: Profit Margin Constraints
    min_price = cost_price * 1.1  # Cost price + 10%
    max_price = base_price * 1.5  # Base price + 50%
    adjusted_price = max(adjusted_price, min_price)  # Enforce minimum profit margin
    adjusted_price = min(adjusted_price, max_price)  # Enforce maximum price limit

    return round(adjusted_price, 2)