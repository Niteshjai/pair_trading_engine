import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
from itertools import combinations
import statsmodels.api as sm
from data import collect_data as dt

class Pair:
  def __init__(self,log_prices,significance_level):
    self.log_prices=log_prices
    self.sign=significance_level

  #Engle-Granger Cointegration Test
  def find_cointegrated_pairs(self):
    scores=[]
    pvalues=[]
    pairs=[]

    for i,j in combinations(self.log_prices.columns,2):
        series1=self.log_prices[i]
        series2=self.log_prices[j]
        score,pvalue,_=coint(series1,series2)
        if pvalue<self.sign:
            pairs.append((i,j))
            scores.append(score)
            pvalues.append(pvalue)

    return pairs,scores,pvalues

  def estimate_spread(self,y, x):
      x = sm.add_constant(x)
      model = sm.OLS(y, x).fit()
      hedge_ratio = model.params[1]
      spread = y - hedge_ratio * x.values[:, 1]
      return spread, hedge_ratio

  def fit_ou_process(self,spread):
      dt = 1  # daily frequency
      spread = np.array(spread)
      y = spread[1:]
      x = spread[:-1]
      delta = y - x

      A = np.vstack([x, np.ones(len(x))]).T
      params = np.linalg.lstsq(A, delta, rcond=None)[0]
      theta = params[0]
      mu = -params[1] / theta
      sigma = np.std(delta - theta * x - params[1])

      return theta, mu, sigma

  def main(self):
    pairs_info = []
    pairs,scores,pvalues=self.find_cointegrated_pairs()
    for (A, B) in pairs:
        y = self.log_prices[A]
        x = self.log_prices[B]
        spread, hedge = self.estimate_spread(y, x)
        theta, mu, sigma = self.fit_ou_process(spread)

        pairs_info.append({
            'pair': (A, B),
            'hedge_ratio': hedge,
            'theta': theta,
            'mu': mu,
            'sigma': sigma,
            'half_life': np.log(2) / theta
        })

    pairs_df = pd.DataFrame(pairs_info).sort_values("half_life")
    return pairs_df,spread,hedge

def cointegrated_pairs():
    find_pair=Pair(dt.log_prices, significance_level=0.05)
    pairs_df,spread,hedge_ratio=find_pair.main()
