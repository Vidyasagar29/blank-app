import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Set up Streamlit page config
st.set_page_config(page_title="Aprameya Investment Portfolio", layout="wide")

# Add custom branding for the company
st.markdown("""
<div style="background-color:#00274d;padding:20px;border-radius:10px">
    <h1 style="color:#ffffff;text-align:center;">aprameya Investments and Analytics</h1>
</div>
""", unsafe_allow_html=True)

# Define the stocks and start/end dates
stocks = ["HDFCBANK.NS", "WIPRO.NS", "KOTAKBANK.NS", "RELIANCE.NS", "BANKBEES.NS", 
          "MOM100.NS", "ICICIMCAP.NS", "ITBEES.NS", "MID150BEES.NS"]
start_date = "2024-04-01"
end_date = pd.to_datetime("today").strftime("%Y-%m-%d")

# Initialize an empty DataFrame for portfolio values
portfolio_values = pd.DataFrame()

# Define portfolio details
portfolio_info = [
    {'Symbol': 'HDFCBANK', 'Ticker': 'HDFCBANK.NS', 'Qty': 849, 'Buy Price': 1661.73, 'Buy Value': 1410809},
    {'Symbol': 'WIPRO', 'Ticker': 'WIPRO.NS', 'Qty': 973, 'Buy Price': 441.65, 'Buy Value': 429725},
    {'Symbol': 'KOTAKBANK', 'Ticker': 'KOTAKBANK.NS', 'Qty': 103, 'Buy Price': 1581.3, 'Buy Value': 162874},
    {'Symbol': 'RELIANCE', 'Ticker': 'RELIANCE.NS', 'Qty': 1515, 'Buy Price': 1350, 'Buy Value': 2045250},
    {'Symbol': 'NIPPON INDIA BANKNIFTY ETF', 'Ticker': 'BANKBEES.NS', 'Qty': 17024, 'Buy Price': 516.67, 'Buy Value': 8795790},
    {'Symbol': 'MOTILAL OSWAL M100ETF', 'Ticker': 'MOM100.NS', 'Qty': 2681, 'Buy Price': 61.04, 'Buy Value': 163648},
    {'Symbol': 'ICICI PRUD BSE Mcap Select ETF', 'Ticker': 'MIDSELIETF.NS', 'Qty': 10633, 'Buy Price': 15.39, 'Buy Value': 163642},
    {'Symbol': 'Nippon India ETF IT', 'Ticker': 'ITBEES.NS', 'Qty': 71129, 'Buy Price': 40.26, 'Buy Value': 2863654},
    {'Symbol': 'Nippon India ETF Nifty Midcap 150', 'Ticker': 'MID150BEES.NS', 'Qty': 30197, 'Buy Price': 214.05, 'Buy Value': 6463668}
]

# Create an empty list to hold stock data
for stock in portfolio_info:
    ticker = yf.Ticker(stock['Ticker'])
    data = ticker.history(start=start_date, end=end_date)
    
    # Add investment value for the stock with 100 shares
    data['Investment Value'] = data['Close'] * stock['Qty']
    data['Symbol'] = stock['Symbol']  # Add symbol to the data for clarity
    portfolio_values[stock['Symbol']] = data['Investment Value']  # Add to portfolio data
    stock['Close Price'] = data['Close'].iloc[-1]  # Get the latest close price

# Fill missing data using forward fill
portfolio_values.ffill(inplace=True)


# Calculate the total portfolio value for each day
portfolio_values['Total Portfolio Value'] = portfolio_values.sum(axis=1)

# Total Investment Value: sum of all buy values
total_investment_value = sum([stock['Buy Value'] for stock in portfolio_info])

# Present Value: sum of the latest investment values
present_value = portfolio_values['Total Portfolio Value'].iloc[-1]

# Calculate Percentage Change
percentage_change = ((present_value - total_investment_value) / total_investment_value) * 100

# Create two columns: one for the portfolio information and one for the chart
col1, col2 = st.columns([2, 3])

# Column 1: Portfolio Information with Table and Additional Data
with col1:
    st.markdown("""
    <div style="background-color:#2e3b4e;padding:10px;margin-top:20px;border-radius:10px">
        <h2 style="color:#ffffff;">Portfolio Information</h2>
    </div>
    """, unsafe_allow_html=True)

    # Create a DataFrame for portfolio table (remove "Ticker" column)
    portfolio_df = pd.DataFrame(portfolio_info)
    portfolio_df['Symbol'] = portfolio_df['Symbol'].str.replace('.NS', '', regex=False)  # Remove .NS
    portfolio_df = portfolio_df.drop(columns=["Ticker"])  # Remove the Ticker column

    # Add Close Price to the table
    portfolio_df['Close Price'] = [stock['Close Price'] for stock in portfolio_info]
    
    # Display the table
    st.dataframe(portfolio_df)

    # Display Total Investment Value, Present Value, and Percentage Change
    st.markdown(f"**Total Investment Value: ₹{total_investment_value:,.2f}**")
    st.markdown(f"**Present Value: ₹{present_value:,.2f}**")
    st.markdown(f"**Percentage Change: {percentage_change:.2f}%**")

# Column 2: Portfolio Value Chart
with col2:
    # Plot the total portfolio value over time
    fig = go.Figure()

    # Add the total portfolio value as a line on the plot
    fig.add_trace(go.Scatter(
        x=portfolio_values.index,  # Date
        y=portfolio_values['Total Portfolio Value'],  # Total portfolio value
        mode='lines+markers',
        name='Total Portfolio Value',
        line=dict(color='orange', width=4),
    ))

    # Customize layout
    fig.update_layout(
        title="Portfolio Value ",
        xaxis_title="Date",
        yaxis_title="Total Portfolio Value (₹)",
        template="plotly_dark",
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True
    )

    # Show the chart
    st.plotly_chart(fig, use_container_width=True)

# Footer section: Line and copyright
st.markdown("""
<div style="text-align:center;padding-top:20px;">
    <hr>
    <p style="font-size:12px;color:#777;">@2024 Aprameya Investments and Analytics - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
