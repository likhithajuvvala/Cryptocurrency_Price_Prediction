import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

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

# ---------------- Demo Data ----------------
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

# ---------------- Yahoo Finance Data ----------------
def load_data(symbol):
    try:
        data = yf.download(
            tickers=symbol,
            period="2y",
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False
        )

        if data is None or data.empty:
            raise ValueError("Empty data")

        data = data.reset_index()
        data = data[["Date", "Close"]]
        return data, False

    except:
        fallback_symbol = symbol.split("-")[0]
        return load_demo_data(fallback_symbol), True

# ---------------- Prediction ----------------
if st.button("Predict"):
    symbol = crypto_map[choice]

    data, fallback_used = load_data(symbol)

    if fallback_used:
        st.warning("Live Yahoo Finance data unavailable. Using demo historical data.")
    else:
        st.success("Live Yahoo Finance data loaded successfully.")

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
        start=data["Date"].iloc[-1] + pd.Timedelta(days=1),
        periods=30
    )

    forecast = pd.DataFrame(
        {"Predicted Price": future_y},
        index=future_dates
    )

    # Forecast results
    st.subheader("📊 30-Day Price Forecast")
    st.line_chart(forecast)
    st.dataframe(forecast.style.format("{:.2f}"))

    # Metrics
    st.subheader("📌 Summary")
    st.metric(
        label="Last Known Price",
        value=f"${data['Close'].iloc[-1]:.2f}"
    )
    st.metric(
        label="Predicted Price (Day 30)",
        value=f"${forecast.iloc[-1, 0]:.2f}"
    )

st.caption("⚠️ Educational purpose only. Not financial advice.")
