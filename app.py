import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

st.set_page_config(page_title="Crypto Price Prediction")

st.title("📈 Cryptocurrency Price Prediction")
st.write("Predict next 30 days using historical trends")

crypto_map = {
    "Bitcoin (BTC)": "BTC",
    "Ethereum (ETH)": "ETH",
    "Binance Coin (BNB)": "BNB"
}

choice = st.selectbox("Select Cryptocurrency", crypto_map.keys())

# --- fallback demo data ---
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


if st.button("Predict"):
    symbol = crypto_map[choice]

    st.info("Live market data unavailable on corporate networks. Using historical demo data.")

    data = load_demo_data(symbol)

    # Trend model (stable everywhere)
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

    st.success("Prediction Complete")
    st.line_chart(forecast)
    st.dataframe(forecast)
