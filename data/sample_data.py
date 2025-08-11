"""
Sample data generation for the Streamlit AgGrid demo
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records=1000):
    """Generate sample sales data for demonstration"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define sample data options
    products = [
        'Laptop Pro', 'Desktop Elite', 'Monitor 4K', 'Wireless Mouse', 'Mechanical Keyboard',
        'Tablet Air', 'Smartphone X', 'Headphones Premium', 'Webcam HD', 'Speaker Set',
        'Router WiFi 6', 'External SSD', 'USB Hub', 'Cable HDMI', 'Power Bank',
        'Smart Watch', 'Fitness Tracker', 'Gaming Chair', 'Desk Lamp LED', 'Document Scanner'
    ]
    
    categories = [
        'Computers', 'Peripherals', 'Mobile Devices', 'Audio/Video', 
        'Networking', 'Storage', 'Accessories', 'Wearables', 'Furniture', 'Office Equipment'
    ]
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    sales_reps = [
        'Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown',
        'Frank Miller', 'Grace Lee', 'Henry Taylor', 'Iris Chen', 'Jack Anderson'
    ]
    
    # Product to category mapping
    product_category_map = {
        'Laptop Pro': 'Computers', 'Desktop Elite': 'Computers',
        'Monitor 4K': 'Peripherals', 'Wireless Mouse': 'Peripherals', 'Mechanical Keyboard': 'Peripherals',
        'Tablet Air': 'Mobile Devices', 'Smartphone X': 'Mobile Devices',
        'Headphones Premium': 'Audio/Video', 'Webcam HD': 'Audio/Video', 'Speaker Set': 'Audio/Video',
        'Router WiFi 6': 'Networking',
        'External SSD': 'Storage', 'USB Hub': 'Accessories', 'Cable HDMI': 'Accessories', 'Power Bank': 'Accessories',
        'Smart Watch': 'Wearables', 'Fitness Tracker': 'Wearables',
        'Gaming Chair': 'Furniture', 'Desk Lamp LED': 'Furniture',
        'Document Scanner': 'Office Equipment'
    }
    
    # Generate data
    data = []
    start_date = datetime.now() - timedelta(days=365)
    
    for _ in range(num_records):
        # Random date within the last year
        random_days = random.randint(0, 365)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Random product
        product = random.choice(products)
        category = product_category_map[product]
        
        # Random quantity (weighted towards smaller quantities)
        quantity = np.random.choice([1, 2, 3, 4, 5, 10, 20], p=[0.4, 0.25, 0.15, 0.1, 0.05, 0.03, 0.02])
        
        # Unit price based on product type
        if category == 'Computers':
            unit_price = np.random.uniform(500, 2000)
        elif category == 'Mobile Devices':
            unit_price = np.random.uniform(200, 1200)
        elif category == 'Audio/Video':
            unit_price = np.random.uniform(50, 500)
        elif category == 'Networking':
            unit_price = np.random.uniform(100, 400)
        elif category == 'Storage':
            unit_price = np.random.uniform(80, 300)
        elif category == 'Wearables':
            unit_price = np.random.uniform(100, 600)
        elif category == 'Furniture':
            unit_price = np.random.uniform(200, 800)
        else:  # Peripherals, Accessories, Office Equipment
            unit_price = np.random.uniform(20, 200)
        
        unit_price = round(unit_price, 2)
        total_amount = round(quantity * unit_price, 2)
        
        # Profit margin (higher for certain categories)
        if category in ['Computers', 'Mobile Devices']:
            profit_margin = np.random.uniform(0.15, 0.35)
        elif category in ['Audio/Video', 'Wearables']:
            profit_margin = np.random.uniform(0.25, 0.45)
        else:
            profit_margin = np.random.uniform(0.30, 0.60)
        
        profit_margin = round(profit_margin * 100, 1)  # Convert to percentage
        
        data.append({
            'Date': transaction_date.strftime('%Y-%m-%d'),
            'Product': product,
            'Category': category,
            'Region': random.choice(regions),
            'Sales Rep': random.choice(sales_reps),
            'Quantity': quantity,
            'Unit Price': unit_price,
            'Total Amount': total_amount,
            'Profit Margin': profit_margin
        })
    
    return pd.DataFrame(data)

def get_aggregation_demo_data():
    """Generate a smaller dataset perfect for aggregation demonstrations"""
    return generate_sample_data(500)

def generate_finance_data(num_stocks=50):
    """Generate sample financial market data for demonstration"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define stock data
    stock_symbols = [
        'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ADBE', 'CRM',
        'ORCL', 'IBM', 'INTC', 'AMD', 'QCOM', 'UBER', 'LYFT', 'SNAP', 'TWTR', 'SQ',
        'PYPL', 'V', 'MA', 'JPM', 'GS', 'MS', 'BAC', 'WFC', 'C', 'AXP',
        'KO', 'PEP', 'MCD', 'SBUX', 'NKE', 'DIS', 'CMCSA', 'VZ', 'T', 'TMUS',
        'JNJ', 'PFE', 'MRK', 'ABBV', 'BMY', 'LLY', 'UNH', 'CVS', 'WMT', 'TGT'
    ]
    
    company_names = [
        'Apple Inc.', 'Alphabet Inc.', 'Microsoft Corp.', 'Amazon.com Inc.', 'Tesla Inc.',
        'Meta Platforms', 'NVIDIA Corp.', 'Netflix Inc.', 'Adobe Inc.', 'Salesforce Inc.',
        'Oracle Corp.', 'IBM Corp.', 'Intel Corp.', 'AMD Inc.', 'Qualcomm Inc.',
        'Uber Technologies', 'Lyft Inc.', 'Snap Inc.', 'Twitter Inc.', 'Block Inc.',
        'PayPal Holdings', 'Visa Inc.', 'Mastercard Inc.', 'JPMorgan Chase', 'Goldman Sachs',
        'Morgan Stanley', 'Bank of America', 'Wells Fargo', 'Citigroup Inc.', 'American Express',
        'Coca-Cola Co.', 'PepsiCo Inc.', 'McDonald\'s Corp.', 'Starbucks Corp.', 'Nike Inc.',
        'Walt Disney Co.', 'Comcast Corp.', 'Verizon Comm.', 'AT&T Inc.', 'T-Mobile US',
        'Johnson & Johnson', 'Pfizer Inc.', 'Merck & Co.', 'AbbVie Inc.', 'Bristol Myers',
        'Eli Lilly', 'UnitedHealth', 'CVS Health', 'Walmart Inc.', 'Target Corp.'
    ]
    
    sectors = [
        'Technology', 'Technology', 'Technology', 'Consumer Discretionary', 'Consumer Discretionary',
        'Technology', 'Technology', 'Communication Services', 'Technology', 'Technology',
        'Technology', 'Technology', 'Technology', 'Technology', 'Technology',
        'Technology', 'Technology', 'Communication Services', 'Communication Services', 'Financial Services',
        'Financial Services', 'Financial Services', 'Financial Services', 'Financial Services', 'Financial Services',
        'Financial Services', 'Financial Services', 'Financial Services', 'Financial Services', 'Financial Services',
        'Consumer Staples', 'Consumer Staples', 'Consumer Discretionary', 'Consumer Discretionary', 'Consumer Discretionary',
        'Communication Services', 'Communication Services', 'Communication Services', 'Communication Services', 'Communication Services',
        'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare',
        'Healthcare', 'Healthcare', 'Healthcare', 'Consumer Staples', 'Consumer Discretionary'
    ]
    
    # Generate base prices (realistic ranges)
    base_prices = [
        150, 2800, 300, 3200, 200, 320, 450, 400, 500, 180,
        80, 130, 50, 90, 150, 40, 15, 25, 45, 80,
        90, 220, 350, 140, 350, 85, 35, 45, 50, 160,
        60, 170, 250, 100, 120, 100, 45, 40, 20, 120,
        170, 50, 90, 140, 65, 310, 480, 95, 150, 220
    ]
    
    data = []
    current_time = datetime.now()
    
    for i in range(min(num_stocks, len(stock_symbols))):
        symbol = stock_symbols[i]
        company = company_names[i]
        sector = sectors[i]
        base_price = base_prices[i]
        
        # Generate price change (-10% to +10%)
        price_change_pct = np.random.uniform(-10, 10)
        price_change = base_price * price_change_pct / 100
        current_price = base_price + price_change
        
        # Generate volume (100K to 10M shares)
        volume = np.random.randint(100000, 10000000)
        
        # Market cap calculation (billions)
        shares_outstanding = np.random.randint(1000, 5000) * 1000000  # 1B-5B shares
        market_cap = (current_price * shares_outstanding) / 1000000000  # in billions
        
        # Generate 52-week range
        week_52_low = base_price * np.random.uniform(0.7, 0.9)
        week_52_high = base_price * np.random.uniform(1.1, 1.5)
        
        # Generate P/E ratio
        pe_ratio = np.random.uniform(10, 35) if sector != 'Technology' else np.random.uniform(20, 80)
        
        # Generate dividend yield (some stocks don't pay dividends)
        dividend_yield = np.random.uniform(0, 4) if np.random.random() > 0.3 else 0
        
        # Generate sparkline data (last 30 days)
        sparkline_data = []
        temp_price = base_price
        for day in range(30):
            daily_change = np.random.uniform(-0.05, 0.05)  # ±5% daily change
            temp_price *= (1 + daily_change)
            sparkline_data.append(round(temp_price, 2))
        
        data.append({
            'Symbol': symbol,
            'Company': company,
            'Sector': sector,
            'Price': round(current_price, 2),
            'Change': round(price_change, 2),
            'Change%': round(price_change_pct, 2),
            'Volume': volume,
            'Market Cap (B)': round(market_cap, 2),
            '52W Low': round(week_52_low, 2),
            '52W High': round(week_52_high, 2),
            'P/E Ratio': round(pe_ratio, 2) if pe_ratio > 0 else None,
            'Dividend Yield%': round(dividend_yield, 2) if dividend_yield > 0 else 0,
            'Sparkline': sparkline_data,
            'Last Updated': current_time.strftime("%H:%M:%S")
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate and display sample data
    df = generate_sample_data(100)
    print("Sample data preview:")
    print(df.head(10))
    print(f"\nDataset shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nSummary statistics:\n{df.describe()}")
