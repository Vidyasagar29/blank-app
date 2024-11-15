import yfinance as yf
import pandas as pd
import streamlit as st
import numpy as np

# Function to fetch Nifty data using yfinance
def fetch_nifty_data():
    nifty = yf.Ticker('^NSEI')
    data = nifty.history(period='10y', interval='1d')  # Fetch 1 year of daily data
    return data

# Function to calculate rolling return
def calculate_rolling_return(data, window=365):
    # Calculate daily returns
    data['Daily_Return'] = data['Close'].pct_change()

    # Calculate rolling return (Cumulative return over the rolling window)
    data['Rolling_Return'] = data['Close'].pct_change(periods=window)*100
    return data

# Streamlit Application Title
st.title('Rolling Return Calculation for Nifty Index')

# Sidebar for selecting the window period (in days)
st.sidebar.header("Rolling Return Parameters")
window = st.sidebar.slider("Rolling Window (Days)", min_value=50, max_value=750, value=365)

# Fetch Nifty Data
data_nifty = fetch_nifty_data()

# Calculate Rolling Return for Nifty
data_nifty = calculate_rolling_return(data_nifty, window)

# Display the data and Rolling Return
st.subheader(f"Rolling Return for Nifty Index (Window = {window} days)")
st.write(data_nifty[['Close', 'Rolling_Return']])

# Plot the Rolling Return
st.subheader(f"Rolling Return Plot (Window = {window} days)")
st.line_chart(data_nifty['Rolling_Return'])

# Display some insights
st.write(f"Rolling return is calculated over the past {window} days.")
