# 📊 StockWise - Stock Analysis & Forecasting App

StockWise is an interactive web application built using **Streamlit** that allows users to:

* 📈 Compare stock performance
* 💹 Visualize real-time stock data
* 🔮 Predict future stock prices using Facebook Prophet
* 📊 Analyze trends with interactive charts

---

## 🚀 Features

### 🔹 Stocks Performance Comparison

* Compare multiple companies
* View cumulative returns
* Multiple chart types (Line, Area, Bar)

### 🔹 Real-Time Stock Price

* Interactive charts (Line & Candlestick)
* Historical price visualization

### 🔹 Stock Prediction

* Forecast stock prices up to 4 years
* Uses Facebook Prophet
* Displays:

  * Forecast graph
  * Trend components
  * Accuracy metrics (MAE, MSE, RMSE)

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* Facebook Prophet
* Scikit-learn
* NumPy

---

## 📂 Dataset

The dataset used:
`historical_stock_data.csv`

Contains:

* Date
* Company
* Open, Close, High, Low prices

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/StockWise.git
cd StockWise
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📊 Model Details

* Model Used: Prophet
* Evaluation Metrics:

  * MAE
  * MSE
  * RMSE

---
## 📌 Future Improvements

* Live stock API integration (Yahoo Finance)
* User authentication
* Portfolio tracking
* Deployment on Streamlit Cloud

---

## ⭐ If you like this project, give it a star!
