import pandas as pd
import datetime as dt
from fyers_apiv3 import fyersModel
import credentials as cd
import time
import logging

# Credentials from credentials file
client_id = cd.client_id
secret_key = cd.secret_key
redirect_uri = cd.redirect_uri
user_name = cd.user_name
totp_key = cd.totp_key
auth_code = cd.auth_code

# Read access token from file
with open('access.txt', 'r') as a:
    access_token = a.read().strip()

# Initialize the FyersModel instance
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

# Function to fetch OHLC data for today
def fetchOHLC_today(ticker, interval):
    """Fetch historical data for today only and return as a DataFrame."""
    instrument = ticker
    today = dt.date.today() - dt.timedelta(days=2)
    data = {
        "symbol": instrument,
        "resolution": interval,
        "date_format": "1",
        "range_from": str(today),  # Fetching data from today's date
        "range_to": str(today),    # to today's date
        "cont_flag": "1"
    }

    # Fetch data from API
    response = fyers.history(data)

    # Convert response to DataFrame
    if 'candles' not in response:
        raise Exception(f"Error fetching data: {response}")

    df = pd.DataFrame(response['candles'], columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    df.set_index('date', inplace=True)
    return df

# Function to calculate short-term and long-term moving averages
def calculate_moving_averages(df, short_window=50, long_window=200):
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    return df

# Function to generate buy/sell signals based on moving average crossover
def generate_signals(df):
    df['signal'] = 0
    df['signal'][df['short_ma'] > df['long_ma']] = 1  # Buy signal
    df['signal'][df['short_ma'] < df['long_ma']] = -1  # Sell signal
    return df

# Main execution to fetch today's data
ticker = 'NSE:RVNL-EQ'
interval = '5'  # 5-minute interval

# Fetch OHLC data for today
df = fetchOHLC_today(ticker, interval)

# Calculate moving averages (adjust windows as needed)
df = calculate_moving_averages(df, short_window=5, long_window=20)

# Generate buy and sell signals
df = generate_signals(df)

# Display the DataFrame with moving averages and signals
print(df[['open', 'high', 'low', 'close', 'short_ma', 'long_ma', 'signal']])

# (Your existing code above)

# Step 5: Function to place orders
def place_order(signal, ticker):
    if signal == 1:
        # Buy order
        order_data = {
            "symbol": ticker,
            "qty": 1,  # Number of shares to buy
            "side": "buy",
            "type": "market",
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "GFD",
        }
        response = fyers.place_order(order_data)
        return response
    elif signal == -1:
        # Sell order
        order_data = {
            "symbol": ticker,
            "qty": 1,  # Number of shares to sell
            "side": "sell",
            "type": "market",
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "GFD",
        }
        response = fyers.place_order(order_data)
        return response

# Step 6: Implement the Bot Loop


# Set up logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO)

while True:
    # Fetch today's data
    df = fetchOHLC_today(ticker, interval)

    # Calculate moving averages
    df = calculate_moving_averages(df, short_window=5, long_window=20)

    # Generate signals
    df = generate_signals(df)

    # Get the latest signal
    latest_signal = df['signal'].iloc[-1]

    # Place order based on the latest signal
    if latest_signal != 0:  # Only execute if there's a buy or sell signal
        response = place_order(latest_signal, ticker)
        logging.info(f"Order placed: {response}")

    # Sleep for a defined interval (e.g., 5 minutes)
    time.sleep(10)  # 300 seconds
