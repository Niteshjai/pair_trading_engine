import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from data import collect_data  # fetches log-transformed price data
from notebook import cointegrated_pairs  # performs cointegration analysis

class Strategy:
    def __init__(self, spread, window):
        self.spread = spread
        self.window = window  # rolling window for z-score

    # Step 1: Compute rolling z-score of the spread
    def compute_zscore(self):
        mean = self.spread.rolling(self.window).mean()
        std = self.spread.rolling(self.window).std()
        zscore = (self.spread - mean) / std
        return zscore

    # Step 2: Generate long/short/exit signals based on z-score thresholds
    def generate_signals(self):
        entry_z = 2    # entry threshold
        exit_z = 0.5   # exit threshold
        zscore = self.compute_zscore()

        long_signal = (zscore < -entry_z).astype(int)
        short_signal = (zscore > entry_z).astype(int)
        exit_signal = (abs(zscore) < exit_z).astype(int)

        position = np.zeros(len(zscore))  # 1 for long, -1 for short, 0 for flat

        for i in range(1, len(zscore)):
            if long_signal[i] and position[i-1] == 0:
                position[i] = 1
            elif short_signal[i] and position[i-1] == 0:
                position[i] = -1
            elif exit_signal[i]:
                position[i] = 0
            else:
                position[i] = position[i-1]  # hold previous position

        return pd.Series(position, index=zscore.index)

    # Step 3: Simulate PnL with transaction costs
    def simulate_pnl(self, position, y, x, hedge_ratio, cost=0.001):
        spread = y - hedge_ratio * x
        spread_returns = spread.diff().fillna(0)
        position = position.shift(1).fillna(0)  # use previous day’s position

        raw_pnl = position * spread_returns
        trades = position.diff().abs()
        costs = trades * cost  # cost per unit position change
        net_pnl = raw_pnl - costs

        return net_pnl

    # Full strategy pipeline for one pair
    def run_pair_strategy(self, log_prices, A, B, hedge_ratio):
        y = log_prices[A]
        x = log_prices[B]
        spread = self.spread
        zscore = self.compute_zscore()
        position = self.generate_signals()
        pnl = self.simulate_pnl(position, y, x, hedge_ratio)

        return pnl, position, zscore

# Step 4: Initialize with cointegrated pair info
pairs_df, spread, hedge_ratio = cointegrated_pairs()
st = Strategy(spread, 21)  # 21-day rolling window
cointegrated_pairs = pairs_df['pair'].tolist()  # list of pairs
results = {}

# Utility: Plot signals and positions
def plot_signals(zscore, position, A, B):
    plt.figure(figsize=(12, 5))
    plt.plot(zscore, label='Z-score')
    plt.plot(position * 2, label='Position (scaled)', alpha=0.5)
    plt.axhline(2, color='red', linestyle='--')
    plt.axhline(-2, color='green', linestyle='--')
    plt.axhline(0.5, color='gray', linestyle=':')
    plt.axhline(-0.5, color='gray', linestyle=':')
    plt.title(f'Trading Signals for {A}/{B}')
    plt.legend()
    plt.show()

# Step 5: Apply strategy to all cointegrated pairs
def result():
    for A, B in cointegrated_pairs:
        log_prices = collect_data()
        pnl, position, zscore = st.run_pair_strategy(log_prices, A, B, hedge_ratio)
        results[(A, B)] = {
            'pnl': pnl,
            'position': position,
            'zscore': zscore,
            'cumulative_pnl': pnl.cumsum()
        }

    # Plot result for the first pair
    first_pair = next(iter(results))
    plot_signals(results[first_pair]['zscore'], results[first_pair]['position'], *first_pair)
    return results

# Script entry point (fixing typo in __name__ check)
if __name__ == "__main__":
    result()
