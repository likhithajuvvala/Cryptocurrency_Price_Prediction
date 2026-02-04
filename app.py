import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
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
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD"
}

choice = st.selectbox("Select Cryptocurrency", crypto_map.keys())

# ---------------- Load Data ----------------
def load_data(symbol):
    try:
        data = yf.download(
            symbol,
            start=date.today() - timedelta(days=730),
            end=date.today(),
            progress=False
        )
        if data.empty:
            raise ValueError("Empty data")
        return data.reset_index(), False
    except:
        return load_demo_data(symbol.split("-")[0]), True


def load_demo_data(symbol):
    dates = pd.date_range(end=date.today(), periods=730)
    np.random.seed(42)

    if symbol == "BTC":
        prices = np.cumsum(np.random.normal(50, 200, 730)) + 30000
    elif symbol == "ETH":
        prices = np.cumsum(np.random.normal(5, 40, 730)) + 2000
    else:
        prices = np.cumsum(np.random.normal(2, 20, 730)) + 300

    return pd.DataFrame({"Date": dates, "Close": prices})


# ---------------- Prediction ----------------
if st.button("Predict"):
    symbol = crypto_map[choice]

    data, fallback_used = load_data(symbol)

    if fallback_used:
        st.warning("Live Yahoo Finance data unavailable. Using demo historical data.")
    else:
        st.success("Live Yahoo Finance data loaded successfully.")

    st.subheader("Historical Price Data")
    st.line_chart(data.set_index("Date")["Close"])

    # Trend-based Linear Regression
    y = data["Close"].values
    x = np.arange(len(y))

    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)

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

    st.subheader("📊 30-Day Price Forecast")
    st.line_chart(forecast)
    st.dataframe(forecast.style.format("{:.2f}"))
