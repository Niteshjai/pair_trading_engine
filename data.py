import pandas as pd
import numpy as np
import yfinance as yf

# List of tickers in the S&P 100 index
sp100_tickers = [
    'AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'AIG', 'AMD', 'AMGN', 'AMT', 'AMZN',
    'AVGO', 'AXP', 'BA', 'BAC', 'BIIB', 'BK', 'BKNG', 'BLK', 'BMY', 'BRK-B',
    'C', 'CAT', 'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CRM', 'CSCO',
    'CVS', 'CVX', 'DHR', 'DIS', 'DOW', 'DUK', 'EMR', 'EXC', 'F', 'FDX',
    'GD', 'GE', 'GILD', 'GM', 'GOOG', 'GOOGL', 'GS', 'HD', 'HON', 'IBM',
    'INTC', 'INTU', 'ISRG', 'JNJ', 'JPM', 'KHC', 'KMI', 'KO', 'LIN', 'LLY',
    'LMT', 'LOW', 'MA', 'MCD', 'MDLZ', 'MDT', 'MET', 'META', 'MMM', 'MO',
    'MRK', 'MS', 'MSFT', 'NEE', 'NFLX', 'NKE', 'NVDA', 'ORCL', 'PEP', 'PFE',
    'PG', 'PM', 'PYPL', 'QCOM', 'RTX', 'SBUX', 'SCHW', 'SO', 'SPG', 'T',
    'TGT', 'TMO', 'TMUS', 'TSLA', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V',
    'VZ', 'WBA', 'WFC', 'WMT', 'XOM'
]

def collect_data():
    period = '5Y'  # Download 5 years of daily data

    # Download daily closing prices for all SP100 tickers
    stock_data = yf.download(sp100_tickers, period=period, interval='1d')['Close']

    # Compute log prices (useful for many financial time series models)
    log_prices = np.log(stock_data)

    # Save to CSV for later use
    log_prices.to_csv('log_prices.csv')

    return log_prices
