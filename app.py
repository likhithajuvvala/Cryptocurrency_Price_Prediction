import streamlit as st
import yfinance as yf
from autots import AutoTS
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

    data["Date"] = data.index
    data = data[["Date", "Close"]]
    data.reset_index(drop=True, inplace=True)

    model = AutoTS(
        forecast_length=30,
        frequency="infer",
        ensemble="simple"
    )

    model = model.fit(
        data,
        date_col="Date",
        value_col="Close"
    )

    forecast = model.predict().forecast

    st.success("Prediction Complete")
    st.line_chart(forecast)
    st.dataframe(forecast)
