
import streamlit as st
import pandas as pd
import datetime
from datetime import date
import time
from plotly import graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
from sklearn.metrics import mean_absolute_error, mean_squared_error
from streamlit_option_menu import option_menu
import numpy as np

st.set_page_config(page_title="StockWise", layout="wide", initial_sidebar_state="expanded")

# Sidebar
st.sidebar.image("Images/StockWiseLogo1.png", width=250, use_column_width=False)  # logo

st.sidebar.title("StockStreamApplication")

with st.sidebar:
    selected_option = option_menu(
        "Utilities", ["Stocks Performance Comparison", "Real-Time Stock Price", "Stock Prediction", 'About']
    )

    start = st.date_input('Start', datetime.date(2022, 1, 1))
    end = st.date_input('End', datetime.date.today())

# Load CSV
df = pd.read_csv("historical_stock_data.csv", parse_dates=["Date"])
companies = sorted(df["Company"].unique())

# Utility function
def get_filtered_data(company):
    filtered = df[
        (df["Company"] == company) &
        (df["Date"] >= pd.to_datetime(start)) &
        (df["Date"] <= pd.to_datetime(end))
    ]
    return filtered

# Stocks Performance Comparison
if selected_option == "Stocks Performance Comparison":
    st.subheader("Stocks Performance Comparison")
    selected_companies = st.multiselect("Select Companies", companies)

    if not selected_companies:
        st.warning("Please select at least one company.")
    else:
        st.write("Relative Return Chart")
        chart_type = st.selectbox("Select chart type", ["Line", "Area", "Bar"])

        df_filtered = df[df["Company"].isin(selected_companies)]
        pivot_data = df_filtered.pivot(index="Date", columns="Company", values="Close")
        rel_ret = pivot_data.pct_change().fillna(0)
        cum_ret = (1 + rel_ret).cumprod()

        if chart_type == "Line":
            st.line_chart(cum_ret)
        elif chart_type == "Area":
            st.area_chart(cum_ret)
        else:
            st.bar_chart(cum_ret)

# Real-Time Stock Price
elif selected_option == "Real-Time Stock Price":
    st.subheader("Real-Time Stock Price")
    selected_company = st.selectbox("Select a Company", companies)

    if selected_company:
        data = get_filtered_data(selected_company)

        if data.empty:
            st.warning("No data found for selected date range.")
        else:
            st.write("Raw Data")
            st.dataframe(data)

            chart_type = st.selectbox("Select chart type", ["Line Chart", "Candlestick Chart"])

            if chart_type == "Line Chart":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="Open"))
                fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Close"))
                fig.update_layout(title=f"{selected_company} Price Chart", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(fig, use_container_width=True)

            else:
                fig = go.Figure(data=[
                    go.Candlestick(
                        x=data['Date'],
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close']
                    )
                ])
                fig.update_layout(title=f"Candlestick Chart of {selected_company}", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(fig, use_container_width=True)

            st.write(f"### Closing Price of {selected_company}")
            st.line_chart(data.set_index("Date")["Close"])

# Stock Prediction
elif selected_option == "Stock Prediction":
    st.subheader("Stock Prediction")
    selected_company = st.selectbox("Pick a Company for Prediction", companies)

    filtered = get_filtered_data(selected_company)

    if filtered.empty:
        st.warning("No data found for prediction.")
    else:
        st.write("Raw Data")
        st.dataframe(filtered)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered["Date"], y=filtered["Close"], name="Close"))
        fig.update_layout(title=f"{selected_company} Close Price", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

        df_train = filtered[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})

        n_years = st.slider("Years of Prediction", 1, 4)
        period = n_years * 365

        model = Prophet()
        model.fit(df_train)

        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)

        st.subheader("Forecast Data")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

        st.subheader(f"Forecast plot for {n_years} year(s)")
        fig_forecast = plot_plotly(model, forecast)
        st.plotly_chart(fig_forecast, use_container_width=True)

        st.subheader("Forecast Components")
        fig_components = model.plot_components(forecast)
        st.write(fig_components)

        overlap = pd.merge(df_train, forecast, on="ds", how="inner")
        mae = mean_absolute_error(overlap['y'], overlap['yhat'])
        mse = mean_squared_error(overlap['y'], overlap['yhat'])
        rmse = np.sqrt(mse)

        st.subheader("Model Accuracy Metrics")
        st.write(f"**MAE:** {mae:.2f}")
        st.write(f"**MSE:** {mse:.2f}")
        st.write(f"**RMSE:** {rmse:.2f}")

# About
elif selected_option == "About":
    st.subheader("About StockStream")
    st.markdown("""
**StockStream** is a user-friendly web app for stock analysis and forecasting.

- 📊 Visualize historical performance.
- 💹 View real-time stock trends.
- 🔮 Forecast future prices using Facebook Prophet.

Built with Streamlit, Plotly, and Prophet.

Contact: [support@StockStream.com](mailto:support@StockStream.com)
""")
