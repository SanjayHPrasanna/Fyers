import pandas as pd
import numpy as np
import datetime as dt
from fyers_apiv3 import fyersModel
import credentials as cd
client_id = cd.client_id
secret_key = cd.secret_key
redirect_uri =cd.redirect_uri
user_name=cd.user_name
totp_key=cd.totp_key
auth_code=cd.auth_code

# Read access token from file
with open('access.txt', 'r') as a:
    access_token = a.read().strip()

# Initialize the FyersModel instance
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")


# Function to fetch OHLC data from Fyers API
def fetchOHLC(ticker, interval, duration):
    """Fetch historical data and output in the form of a DataFrame."""
    instrument = ticker
    data = {
        "symbol": instrument,
        "resolution": interval,
        "date_format": "1",
        "range_from": str(dt.date.today() - dt.timedelta(days=duration)),
        "range_to": str(dt.date.today()),
        "cont_flag": "1"
    }
    
    # Fetch data from API
    response = fyers.history(data)
    df = pd.DataFrame(response['candles'], columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
    df.set_index('date', inplace=True)
    return df

# Main Execution
ticker = 'NSE:RVNL-EQ'
interval = '60'  # 5-minute interval
duration = 7  # Past 1 day

# Fetch OHLC data
df = fetchOHLC(ticker, interval, duration)

# print(df)

# Function to calculate support and resistance

def find_support_resistance(df, lookback=24*7):
    """
    Calculate support and resistance using swing highs and swing lows.
    
    :param df: DataFrame containing OHLC data.
    :param lookback: Lookback period in hours to calculate swing highs and lows.
    :return: DataFrame with support and resistance columns.
    """
    if len(df) < lookback:
        print(f"Warning: Dataset length ({len(df)}) is shorter than lookback period ({lookback}).")
        lookback = len(df)  # Adjust lookback to dataset length

    df['support'] = df['low'].rolling(window=lookback, min_periods=1).min()
    df['resistance'] = df['high'].rolling(window=lookback, min_periods=1).max()
    
    return df

# Define the lookback period (e.g., 1 week of hourly data)
lookback_period = 24 * 7

# Calculate support and resistance
df_with_sr = find_support_resistance(df, lookback=lookback_period)

# Display the DataFrame with support and resistance levels
print(df_with_sr[['open', 'high', 'low', 'close', 'support', 'resistance']])

