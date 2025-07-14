import numpy as np
import pandas as pd
from backtest import result as rs

def evaluate_performance(pnl_series):
    cumulative_return = pnl_series.cumsum()
    daily_return = pnl_series.mean()
    volatility = pnl_series.std()
    sharpe_ratio = daily_return / volatility * np.sqrt(252)
    drawdown = cumulative_return - cumulative_return.cummax()
    max_drawdown = drawdown.min()
    return {
        'Cumulative Return': cumulative_return[-1],
        'Daily Return': daily_return,
        'Volatility': volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_drawdown
    }

def report_all_pairs(results):
    metrics = {}
    for pair, data in results.items():
        metrics[pair] = evaluate_performance(data['pnl'])
    return pd.DataFrame(metrics).T.sort_values(by='Sharpe Ratio', ascending=False)

performance_df = report_all_pairs(rs.results)
print(performance_df)