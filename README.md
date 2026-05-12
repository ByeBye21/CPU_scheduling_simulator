# Stock Prediction

Stock Prediction is a professional-grade Decision Support System (DSS) designed to predict financial market trends using machine learning. Moving away from traditional price regression, this system utilizes **probabilistic direction classification** to determine the likelihood of a stock finishing "Up" or "Down" over a specific time horizon.

## Overview
Financial time series are inherently noisy, making exact price predictions often unreliable. This project implements a robust classification framework that evaluates technical indicators, market context, and macro volatility to provide actionable insights rather than static price targets.

## Key Features
- **Classification Engine:** Includes Logistic Regression, Random Forest, XGBoost, and LightGBM models.
- **Dynamic Horizons:** Supports 1, 5, 10, and 20-day business day predictive horizons.
- **Deep Analysis Module:** An automated benchmark engine that scans 96 unique configurations (horizons, training windows, and factor sets) to find the optimal setup for any ticker.
- **Advanced Feature Engineering:** Over 50+ contextual and technical features (RSI, MACD, Bollinger Bands, ATR, OBV, etc.) calculated manually using Pandas and NumPy.
- **Contextual Data Integration:** Incorporates external factors like the VIX (Fear Index), Market Benchmarks, and Sector ETFs.
- **Interactive Dashboard:** A comprehensive UI built with Streamlit and Plotly for visual data exploration.

## Tech Stack
- **Language:** Python
- **Interface:** Streamlit, Plotly
- **Data:** Pandas, NumPy, yfinance
- **Machine Learning:** Scikit-learn, XGBoost, LightGBM
- **Statistical Analysis:** SciPy (Confidence Intervals)

## Installation and Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone [https://github.com/ByeBye21/stock_prediction.git](https://github.com/ByeBye21/stock_prediction.git)
cd stock_prediction

```

### 2. Install Dependencies

It is highly recommended to use a virtual environment.

```bash
pip install -r requirements.txt

```

### 3. Launch the Application

Run the following command to start the Streamlit server:

```bash
streamlit run app.py

```

The application will typically be available at `http://localhost:8501`.

## How to Use

1. **Select Stock:** Use the sidebar to pick a popular stock from the list or enter a custom Yahoo Finance ticker (e.g., AAPL, THYAO.IS).
2. **Configure Parameters:** Set the historical `Date Range` and choose your `Target Horizon` (e.g., 20 days for medium-term outlook).
3. **External Factors:** Optionally enable Market Benchmark, VIX, or Sector ETF data to give the model more context.
4. **Run Analysis:** Select the models you wish to compare and click `Run Analysis`. Alternatively, use `Deep Analyze Best Setup` for an exhaustive search of the best parameters.
5. **Analyze Results:**
* **Data Overview:** Review raw prices and statistical summaries.
* **Technical Analysis:** Explore indicators and feature correlation matrices.
* **Model Results:** Compare metrics like AUC-ROC, MCC, and Accuracy.
* **Future Projection:** View the probability-based price path scenario and confidence bands.



## Methodology and Validation

* **Leakage Prevention:** Implements `TimeSeriesSplit` with a target-specific `gap` to ensure training data never contains information from the future.
* **Threshold Optimization:** Dynamically tunes decision thresholds to balance precision and recall based on the specific asset's characteristics.

## Disclaimer

This software is for educational and research purposes only. The predictions and projections generated are based on statistical probabilities and do not constitute financial advice.

```

```
