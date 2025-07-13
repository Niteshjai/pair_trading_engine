import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from data import collect_data 
from notebook import cointegrated_pairs 

class Strategy:
  def __init__(self,spread,window):
    self.spread=spread
    self.window=window

  def compute_zscore(self):
    mean=self.spread.rolling(self.window).mean()
    std=self.spread.rolling(self.window).std()
    zscore=(self.spread-mean)/std
    return zscore

  def generate_signals(self):
    entry_z=2
    exit_z=0.5
    zscore=self.compute_zscore()

    long_signal = (zscore < -entry_z).astype(int)
    short_signal = (zscore > entry_z).astype(int)
    exit_signal = (abs(zscore) < exit_z).astype(int)

    position = np.zeros(len(zscore))

    for i in range(1, len(zscore)):
        if long_signal[i] and position[i-1] == 0:
            position[i] = 1
        elif short_signal[i] and position[i-1] == 0:
            position[i] = -1
        elif exit_signal[i]:
            position[i] = 0
        else:
            position[i] = position[i-1]

    return pd.Series(position, index=zscore.index)

  def simulate_pnl(self,position, y, x, hedge_ratio, cost=0.001):
    spread = y - hedge_ratio * x
    spread_returns = spread.diff().fillna(0)
    position = position.shift(1).fillna(0)  # Use yesterday’s position

    raw_pnl = position * spread_returns
    trades = position.diff().abs()
    costs = trades * cost  # transaction cost per unit change
    net_pnl = raw_pnl - costs

    return net_pnl

  def run_pair_strategy(self,log_prices, A, B, hedge_ratio):
      y = log_prices[A]
      x = log_prices[B]
      spread=self.spread
      zscore = self.compute_zscore()
      position =self.generate_signals()
      pnl =self. simulate_pnl(position, y, x, hedge_ratio)

      return pnl, position, zscore

pairs_df, spread, hedge_ratio = cointegrated_pairs()
st=Strategy(spread,21)
cointegrated_pairs=pairs_df['pair'].tolist()
results = {}

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


for A, B in cointegrated_pairs:
    log_prices=collect_data()
    pnl, position, zscore = st.run_pair_strategy(log_prices, A, B,hedge_ratio)
    #plot_signals(zscore, position, A, B)
    results[(A, B)] = {
        'pnl': pnl,
        'position': position,
        'zscore': zscore,
        'cumulative_pnl': pnl.cumsum()
    }
first_pair = next(iter(results))
plot_signals(results[first_pair]['zscore'], results[first_pair]['position'], *first_pair)

