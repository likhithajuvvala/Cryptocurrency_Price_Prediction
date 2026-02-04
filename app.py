import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import date, timedelta

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

# ---------------- Demo Data ----------------
def load_demo_data(symbol):
    dates = pd.date_range(end=date.today(), periods=730)
    np.random.seed(42)

    if symbol == "bitcoin":
        prices = np.cumsum(np.random.normal(50, 200, 730)) + 30000
    elif symbol == "ethereum":
        prices = np.cumsum(np.random.normal(5, 40, 730)) + 2000
    else:
        prices = np.cumsum(np.random.normal(2, 20, 730)) + 300

    return pd.DataFrame({"Date": dates, "Close": prices})

# ---------------- Live Data (CoinGecko) ----------------
def load_live_data(coin_id):
    try:
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

        if "prices" not in data:
            return None

        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "Close"])
        df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df[["Date", "Close"]]

        return df

    except:
        return None

# ---------------- Prediction ----------------
if st.button("Predict"):
    coin_id = crypto_map[choice]

    data = load_live_data(coin_id)

    if data is None or data.empty:
        st.warning(
            "Live market data unavailable due to API limits. "
            "Using historical demo data instead."
        )
        data = load_demo_data(coin_id)
    else:
        st.success("Live market data loaded successfully.")

    # Historical Prices
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

    # Forecast Output
    st.subheader("📊 30-Day Price Forecast")
    st.line_chart(forecast)
    st.dataframe(forecast.style.format("{:.2f}"))

    # Metrics
    st.subheader("📌 Summary")
    st.metric("Last Known Price", f"${data['Close'].iloc[-1]:.2f}")
    st.metric("Predicted Price (Day 30)", f"${forecast.iloc[-1, 0]:.2f}")
