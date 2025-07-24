# 📊 Statistical Arbitrage: Cointegration-Based Pairs Trading Strategy

This project implements a statistical arbitrage strategy using cointegrated stock pairs. It detects mean-reverting spreads, simulates trades based on z-score signals, and evaluates strategy performance using common risk metrics.

---

## 📁 Project Structure

```
.
├── data.py         # Collect 5 years of daily closing price data for all S&P 100 companies using yfinance.
├── notebook.py     # Identifies cointegrated pairs and OU process parameters
├── backtest.py     # Runs trading simulation and plots signals
├── report.py       # Computes Sharpe, drawdown, and performance summary

```

---

## ⚙️ How It Works

### 1. **Data Collection (`data.py`)**

* Utilizes pandas, numpy, and yfinance for data collection and processing.
*  Computes the natural logarithm of stock prices to prepare for time-series analysis.
* Saves the log-transformed stock prices as a CSV file named log_prices.csv.
  
### 2. **Cointegration Detection (`notebook.py`)**

* Applies the Engle-Granger test to find cointegrated pairs of stocks.
* Estimates spread using linear regression and hedge ratio.
* Fits an Ornstein-Uhlenbeck process to model mean reversion.
* Returns pair list sorted by half-life of reversion.

### 3. **Strategy Backtest (`backtest.py`)**

* Computes rolling z-scores of the spread.
* Generates long/short/exit signals based on z-score thresholds.
* Simulates PnL with transaction costs.
* Visualizes z-score and positions.

### 4. **Performance Reporting (`report.py`)**

* Calculates:

  * Cumulative Return
  * Daily Return
  * Volatility
  * Sharpe Ratio
  * Maximum Drawdown
* Displays performance table sorted by Sharpe Ratio.

---

## 🚀 Usage

1. Ensure `collect_data()` in `data.py` returns log-transformed price data as a DataFrame.
2. Run the full pipeline and print performance:

```bash
python report.py
```

This will run cointegration detection, simulate trades, and print performance metrics for each pair.

---

## 📞 Example Output (printed by `report.py`)

| Pair   | Sharpe Ratio | Max Drawdown | Cumulative Return |
| ------ | ------------ | ------------ | ----------------- |
| (A, B) | 1.23         | -0.05        | 0.18              |
| (C, D) | 0.94         | -0.07        | 0.12              |

---

## 📌 Notes

* Z-score entry/exit thresholds and window length are configurable in `backtest.py`.
* Strategy assumes daily data and 252 trading days per year for Sharpe calculation.

---

## 👤 Author

**Nitesh Jaiswal**
