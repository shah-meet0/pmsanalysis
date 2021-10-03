import math

import pandas as pd
import numpy as np
from numpy import transpose as t

# Many of these functions are natively implemented on Pandas, and those should be used
# Instead of the ones written here.


def mean(series: pd.Series):
    n = len(series)
    sum = 0
    for index, value in series.iteritems():
        sum += value
    return 1/n * sum


def variance(series: pd.Series):
    n = len(series)
    series_mean = mean(series)
    sum = 0
    for index, value in series.iteritems():
        sum += (value - series_mean) ** 2
    return 1/(n-1) * sum


def standard_deviation(series: pd.Series):
    return math.sqrt(variance(series))


def skewness(series: pd.Series):
    series_mean = mean(series)
    var_series = variance(series)
    n = len(series)
    third_central_estimate = 0
    for index,value in series.iteritems():
        third_central_estimate += (value - series_mean) ** 3
    return 1/n * third_central_estimate/(var_series ** (3/2))


def kurtosis(series: pd.Series):
    series_mean = mean(series)
    var_series = variance(series)
    n = len(series)
    fourth_central_estimate = 0
    for index, value in series.iteritems():
        fourth_central_estimate += (value - series_mean) ** 4
    return 1 / n * fourth_central_estimate / (var_series ** 2)


def excess_kurtosis(series: pd.Series):
    return kurtosis(series) - 3


# Assumes monthly data

def annualized_return(returns: pd.Series, in_percent=False):
    if in_percent:
        returns_to_use = returns/100
    else:
        returns_to_use = returns/1

    number_months = len(returns)
    money_turned_into = 1
    for index, month_return in returns_to_use.iteritems():
        money_turned_into *= (1+month_return)

    if in_percent:
        return 100 * (money_turned_into ** (12/number_months) - 1)
    else:
        return money_turned_into ** (12/number_months) - 1


# Assumes monthly data
def annualized_volatility(returns: pd.Series):
    std = standard_deviation(returns)
    return std * math.sqrt(12)


def sharpe_ratio(returns: pd.Series, risk_free_rate=0.0624):
    ar = annualized_return(returns)
    std = annualized_volatility(returns)
    return (ar - risk_free_rate)/std


def get_beta_estimate(returns: pd.Series, index_returns: pd.Series, rf, include_intercept=False):
    n = len(returns)
    n2 = len(index_returns)
    index_returns = index_returns - rf
    y = np.array([returns])
    y = y - rf
    if not n == n2:
        raise ValueError('Input same length of returns and index_returns')
    if include_intercept:
        ones = np.array([1 for i in range(n)])
        x = np.array([ones, index_returns])
    else:
        x = np.array([index_returns])
    x = t(x)
    y = t(y)
    xtx = np.matmul(t(x), x)
    xtxinv = np.linalg.inv(xtx)
    xty = np.matmul(t(x), y)
    beta = np.matmul(xtxinv, xty)
    res = y - np.matmul(x, beta)
    return beta, res


def normalize(series: pd.Series):
    norm_series = (series - mean(series))/standard_deviation(series)
    return norm_series
