# Pairs Trading Backtest

## Description
This repository contains a pair trading engine implemented in Python. Pair trading is a market-neutral trading strategy that matches a long position with a short position in two highly correlated instruments, aiming to profit from the relative price movements between the two. This pair trading engine automates the process of identifying suitable pairs, generating trading signals, and executing trades.

## Key Features and Highlights

-Automated pair selection based on correlation analysis

-Signal generation using statistical measures

## Installation

To use this project, you'll need to have the following dependencies installed:

- Python 3.x
- `matplotlib`
- `pandas`
- `numpy`
- `statsmodels`
- `yfinance`

You can install these dependencies using `pip`:

```
pip install matplotlib pandas numpy statsmodels yfinance
```

## Usage

The main entry point for the project is the `backtest.py` file. This file contains the `Strategy` class, which implements the pairs trading strategy. The `notebook.py` file contains the `Pair` class, which is responsible for finding cointegrated pairs and estimating the necessary parameters for the strategy.

To run the backtest, simply execute the `backtest.py` file:

```
python backtest.py
```

This will run the strategy on all the cointegrated pairs found in the data and display a plot of the trading signals and positions for the first pair.

## API

The `backtest.py` file defines the following classes and methods:

- `Strategy` class:
  - `compute_zscore()`: Computes the rolling z-score of the spread.
  - `generate_signals()`: Generates long, short, and exit signals based on the z-score thresholds.
  - `simulate_pnl()`: Simulates the P&L with transaction costs.
  - `run_pair_strategy()`: Runs the full strategy pipeline for a single pair.

The `notebook.py` file defines the following classes and methods:

- `Pair` class:
  - `find_cointegrated_pairs()`: Applies the Engle-Granger cointegration test to find cointegrated pairs.
  - `estimate_spread()`: Estimates the spread and hedge ratio via linear regression.
  - `fit_ou_process()`: Fits an Ornstein-Uhlenbeck process to the spread.
  - `main()`: Runs the main workflow to find cointegrated pairs and estimate the necessary parameters.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

## Testing

This project does not currently have any automated tests. However, you can manually test the functionality by running the `backtest.py` file and verifying the output.
