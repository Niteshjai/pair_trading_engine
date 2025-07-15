import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
from itertools import combinations
import statsmodels.api as sm
from data import collect_data  # custom function to collect log price data

class Pair:
    def __init__(self, log_prices, significance_level):
        self.log_prices = log_prices  # DataFrame of log-transformed prices
        self.sign = significance_level  # significance level for cointegration test

    # Step 1: Apply Engle-Granger Cointegration Test on all possible pairs
    def find_cointegrated_pairs(self):
        scores = []
        pvalues = []
        pairs = []

        # Iterate over all unique pairs of stocks
        for i, j in combinations(self.log_prices.columns, 2):
            series1 = self.log_prices[i]
            series2 = self.log_prices[j]
            score, pvalue, _ = coint(series1, series2)

            # If p-value is below significance level, consider the pair cointegrated
            if pvalue < self.sign:
                pairs.append((i, j))
                scores.append(score)
                pvalues.append(pvalue)

        return pairs, scores, pvalues

    # Step 2: Estimate the spread and hedge ratio via linear regression
    def estimate_spread(self, y, x):
        x = sm.add_constant(x)  # add intercept
        model = sm.OLS(y, x).fit()
        hedge_ratio = model.params[1]  # slope (beta)
        spread = y - hedge_ratio * x.iloc[:, 1]
        return spread, hedge_ratio

    # Step 3: Fit an Ornstein-Uhlenbeck process to the spread
    def fit_ou_process(self, spread):
        dt = 1  # daily time step
        spread = np.array(spread)
        y = spread[1:]
        x = spread[:-1]
        delta = y - x

        # Linear regression to estimate mean-reversion parameters
        A = np.vstack([x, np.ones(len(x))]).T
        params = np.linalg.lstsq(A, delta, rcond=None)[0]
        theta = params[0]  # speed of mean reversion
        mu = -params[1] / theta  # long-term mean
        sigma = np.std(delta - theta * x - params[1])  # standard deviation of noise

        return theta, mu, sigma

    # Main workflow to find cointegrated pairs and OU parameters
    def main(self):
        pairs_info = []
        pairs, scores, pvalues = self.find_cointegrated_pairs()

        for (A, B) in pairs:
            y = self.log_prices[A]
            x = self.log_prices[B]
            spread, hedge = self.estimate_spread(y, x)
            theta, mu, sigma = self.fit_ou_process(spread)

            # Store all relevant info for each pair
            pairs_info.append({
                'pair': (A, B),
                'hedge_ratio': hedge,
                'theta': theta,
                'mu': mu,
                'sigma': sigma,
                'half_life': np.log(2) / theta  # time to revert halfway to mean
            })

        # Return sorted pairs by half-life (shorter = quicker mean reversion)
        pairs_df = pd.DataFrame(pairs_info).sort_values("half_life")
        return pairs_df, spread, hedge

# Entry point: calls the pipeline and returns best pairs
def cointegrated_pairs():
    log_prices = collect_data()  # fetch log price data
    find_pair = Pair(log_prices, significance_level=0.05)
    pairs_df, spread, hedge_ratio = find_pair.main()
    return pairs_df, spread, hedge_ratio
