import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import timedelta

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Crypto Price Prediction",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Cryptocurrency Price Prediction")
st.write("Predict cryptocurrency prices for the next 30 days using historical trends")

# ---------------- Crypto Options ----------------
crypto_map = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Binance Coin (BNB)": "binancecoin"
}

choice = st.selectbox("Select Cryptocurrency", crypto_map.keys())

# ---------------- Load Data (CoinGecko Safe) ----------------
def load_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    params = {
        "vs_currency": "usd",
        "days": 730,
        "interval": "daily"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    # Safety check
    if "prices" not in data:
        return None

    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "Close"])
    df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["Date", "Close"]]

    return df

# ---------------- Prediction ----------------
if st.button("Predict"):
    coin_id = crypto_map[choice]
    data = load_data(coin_id)

    if data is None or data.empty:
        st.error(
            "Live market data temporarily unavailable due to API limits. "
            "Please try again after some time."
        )
        st.stop()

    st.success("Live market data loaded successfully.")

    # Historical chart
    st.subheader("📉 Historical Prices")
    st.line_chart(data.set_index("Date")["Close"])

    # -------- Linear Regression Trend --------
    y = data["Close"].values
    x = np.arange(len(y))

    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)

    future_x = np.arange(len(y), len(y) + 30)
    future_y = trend(future_x)

    future_dates = pd.date_range(
        start=data["Date"].iloc[-1] + timedelta(days=1),
        periods=30
    )

    forecast = pd.DataFrame(
        {"Predicted Price": future_y},
        index=future_dates
    )

    # Forecast
    st.subheader("📊 30-Day Price Forecast")
    st.line_chart(forecast)
    st.dataframe(forecast.style.format("{:.2f}"))

    # Metrics
    st.subheader("📌 Summary")
    st.metric("Last Known Price", f"${data['Close'].iloc[-1]:.2f}")
    st.metric("Predicted Price (Day 30)", f"${forecast.iloc[-1, 0]:.2f}")
