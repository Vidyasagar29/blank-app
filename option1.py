import streamlit as st
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """Calculate Black-Scholes option price."""
    if S <= 0 or K <= 0 or sigma <= 0 or T < 0:
        return 0  # Handle invalid inputs gracefully

    try:
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == "call":
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == "put":
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type. Use 'call' or 'put'.")
    except Exception as e:
        return 0  # Default to 0 if calculation fails

# Streamlit app
st.title("Black-Scholes Option Pricing and Portfolio Management")

# Fixed inputs for Black-Scholes model
strike_price_put = 24000
strike_price_call = 28000
interest_rate = 0.10
iv_put = 0.18
iv_call = 0.14  # Updated implied volatility for call

# User inputs
spot_price = 24000  # Fixed spot price for initial portfolio calculation
months_to_expiry = st.slider("Months to Expiry", 1, 12, 12)
time_to_expiry = months_to_expiry / 12

# Calculate option prices based on fixed spot price
put_price = max(black_scholes(spot_price, strike_price_put, 1, interest_rate, iv_put, "put"), 0)
call_price = max(black_scholes(spot_price, strike_price_call, 1, interest_rate, iv_call, "call"), 0)

# Portfolio details
qty = 2500
future_buy_price = 24000
initial_put_cost = put_price * qty
initial_call_revenue = call_price * qty
initial_future_cost = future_buy_price * qty

initial_portfolio_value = initial_future_cost + initial_put_cost - initial_call_revenue

st.subheader("Initial Portfolio")
st.write(f"Put Option Price: {put_price:.2f}")
st.write(f"Call Option Price: {call_price:.2f}")
st.write(f"Initial Portfolio Value: {initial_portfolio_value:.2f}")

# Calculate profit/loss at the selected month
spot_price_dynamic = st.slider("Dynamic Spot Price", 20000, 28000, 24000, 1000)
put_price_current = max(black_scholes(spot_price_dynamic, strike_price_put, time_to_expiry, interest_rate, iv_put, "put"), 0)
call_price_current = max(black_scholes(spot_price_dynamic, strike_price_call, time_to_expiry, interest_rate, iv_call, "call"), 0)

future_pnl = (spot_price_dynamic - future_buy_price) * qty
put_pnl = (put_price_current - put_price) * qty
call_pnl = (call_price - call_price_current) * qty

total_pnl = future_pnl + put_pnl + call_pnl

st.subheader("Profit and Loss at Selected Month")
st.write(f"Future P&L: {future_pnl:.2f}")
st.write(f"Put Option P&L: {put_pnl:.2f}")
st.write(f"Call Option P&L: {call_pnl:.2f}")
st.write(f"Total P&L: {total_pnl:.2f}")
