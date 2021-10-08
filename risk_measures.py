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
    return 1 / n * sum


def variance(series: pd.Series):
    n = len(series)
    series_mean = mean(series)
    sum = 0
    for index, value in series.iteritems():
        sum += (value - series_mean) ** 2
    return 1 / (n - 1) * sum


def standard_deviation(series: pd.Series):
    return math.sqrt(variance(series))


def skewness(series: pd.Series):
    series_mean = mean(series)
    var_series = variance(series)
    n = len(series)
    third_central_estimate = 0
    for index, value in series.iteritems():
        third_central_estimate += (value - series_mean) ** 3
    return 1 / n * third_central_estimate / (var_series ** (3 / 2))


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
        returns_to_use = returns / 100
    else:
        returns_to_use = returns

    number_months = len(returns)
    print(number_months)
    money_turned_into = 1
    for index, month_return in returns_to_use.iteritems():
        money_turned_into *= (1 + month_return)

    if in_percent:
        return 100 * ((money_turned_into ** (12 / number_months)) - 1)
    else:
        return (money_turned_into ** (12 / number_months)) - 1


# Assumes monthly data
def annualized_volatility(returns: pd.Series):
    std = standard_deviation(returns)
    return std * math.sqrt(12)


def sharpe_ratio(returns: pd.Series, risk_free_rate=0.0624):
    ar = annualized_return(returns)
    std = annualized_volatility(returns)
    return (ar - risk_free_rate) / std


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
    norm_series = (series - mean(series)) / standard_deviation(series)
    return norm_series


# Next functions are specific to managers, and will provide interpretation only when used for that purpose.


def _skewness_interpretation(given_skewness):
    if given_skewness < -0.5:
        return 'This manager has a **negative** measure of monthly return distribution skewness. ' \
               'This implies that in some months the manager has had returns far below their average monthly return. ' \
               'Thus, one should expect few far below average returns and several small above average returns.'
    elif given_skewness > 0.5:
        return 'This manager has a **positive** measure of monthly return distribution skewness. ' \
               'This implies that in some months the manager has had returns far above their average monthly return. ' \
               'Thus, one should expect few far above average returns and generally below average returns. '
    else:
        return 'This manager has a relatively **neutral** measure of monthly return distribution skewness. ' \
               'This implies that the manager tends to have roughly the same amount of returns above and below their ' \
               'average monthly return. Thus, one should expect the average monthly return to be indicative of ' \
               'long term performance.'


def _kurtosis_interpretation(given_kurtosis):
    if given_kurtosis < 2:
        return 'The distribution of the average monthly returns for this manager is **platykurtic**. This implies that ' \
               'the manager does not tend to have many returns which are far from their average monthly return. ' \
               'One can expect a relatively stable return from this manager. '
    elif given_kurtosis > 5:
        return 'The distribution of the average monthly returns for this manager is **leptokurtic**. This implies that ' \
               'the manager tends to have returns which are quite distant from their average monthly return. ' \
               'One can expect there to be extremely above or below average returns, depending on the skewness. ' \
               'Note that because of the sample size and Covid-19 pandemic, many managers will show leptokurtic returns' \
               'although it might not be indicative of their general performance.'
    else:
        return 'The distribution of the average monthly returns for this manager is **mesokurtic**. This implies that ' \
               'the tails of the distribution are very similar to that of a normal distribution. Extreme deviations ' \
               'from the average monthly return should occur very rarely for this manager, but they will still vary ' \
               'slightly. '


def _beta_interpretation(given_beta):
    if given_beta < -0.3:
        return 'This manager has a **negative** market beta. This implies that their return' \
               'is negatively correlated with the return of the Nifty 500. Typically, these managers have positive ' \
               'returns' \
               'in recession like market conditions, and act as a good way to lower portfolio systematic risk. '
    elif given_beta > 0.3:
        if given_beta > 1:
            return 'This manager has a **positive**  market beta. This implies that their return ' \
                   'is positively correlated with the return of the Nifty 500. Typically, these managers have ' \
                   'positive ' \
                   'returns when the market is booming. This manager has a beta greater than one, which means that ' \
                   'they beat' \
                   'the market when it rises, but also that they typically tend to have lower returns than the market ' \
                   'when it falls.'
        else:
            return 'This manager has a **positive** beta coefficient. This implies that their return ' \
                   'is positively correlated with the return of the Nifty 500. Typically, these managers have ' \
                   'positive ' \
                   'returns when the market is booming, This manager has a beta smaller than one, which means that ' \
                   'they rise less than the market but also are less risky because they tend to fall less than the ' \
                   'market as well.'
    else:
        return 'This manager has a relatively low correlation with the Nifty 500 index. Thus, their monthly returns ' \
               'are not influenced too much by the overarching business cycle, which can make them relatively stable ' \
               'sources of income. '


def _sharpe_ratio_interpretation(given_sharpe_ratio):
    pass
