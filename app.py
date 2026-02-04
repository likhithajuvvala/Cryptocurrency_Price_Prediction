import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import date, timedelta

st.set_page_config(page_title="Crypto Price Prediction")

st.title("📈 Cryptocurrency Price Prediction")
st.write("Predict next 30 days using Machine Learning")

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

    data = data.reset_index()
    data = data[["Date", "Close"]].dropna()

    # Feature engineering
    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data["Close"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 30 days
    future_days = np.arange(len(data), len(data) + 30).reshape(-1, 1)
    future_prices = model.predict(future_days)

    future_dates = pd.date_range(
        start=data["Date"].iloc[-1]()
