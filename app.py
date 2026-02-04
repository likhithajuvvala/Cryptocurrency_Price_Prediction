import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta

st.set_page_config(page_title="Crypto Price Prediction")

st.title("📈 Cryptocurrency Price Prediction")
st.write("Predict next 30 days using historical trends")

crypto_map = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD"
}

choice = st.selectbox("Select Cryptocurrency", crypto_map.keys())

if st.button("Predict"):
    symbol = crypto_map[choice]

    end_date = date.today()
    start_date = end_date - timedelta(days=730)

    data = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        progress=False
    )

    # SAFETY CHECK (this is what was missing earlier)
    if data.empty:
        st.error("Failed to fetch data. Yahoo Finance may be blocked.")
        st.stop()

    data = data.reset_index()[["Date", "Close"]].dropna()

    # Convert to numeric trend
    y = data["Close"].values
    x = np.arange(len(y))

    # Simple linear trend (stable everywhere)
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)

    # Predict next 30 days
    future_x = np.arange(len(y), len(y) + 30)
    future_y = trend(future_x)

    future_dates = pd.date_range(
        start=data["Date"].iloc[-1] + pd.Timedelta(days=1),
        periods=30
    )

    forecast = pd.DataFrame(
        {"Predicted Price": future_y},
        index=future_dates
    )

    st.success("Prediction Complete")
    st.line_chart(forecast)
    st.dataframe(forecast)
