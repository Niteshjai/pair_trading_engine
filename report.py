import numpy as np
import pandas as pd
from backtest import result  # imports the result() function that runs the trading strategy

# Evaluate performance metrics for a given PnL time series
def evaluate_performance(pnl_series):
    cumulative_return = pnl_series.cumsum()  # running sum of returns
    daily_return = pnl_series.mean()         # average daily return
    volatility = pnl_series.std()            # standard deviation of returns

    # Annualized Sharpe Ratio assuming 252 trading days
    sharpe_ratio = daily_return / volatility * np.sqrt(252)

    # Drawdown: difference from historical peak
    drawdown = cumulative_return - cumulative_return.cummax()
    max_drawdown = drawdown.min()

    return {
        'Cumulative Return': cumulative_return[-1],
        'Daily Return': daily_return,
        'Volatility': volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_drawdown
    }

# Apply performance evaluation across all trading pairs
def report_all_pairs(results):
    metrics = {}
    for pair, data in results.items():
        metrics[pair] = evaluate_performance(data['pnl'])
    return pd.DataFrame(metrics).T.sort_values(by='Sharpe Ratio', ascending=False)

# Run backtest and evaluate all pairs
results = result()
performance_df = report_all_pairs(results)
print(performance_df)
