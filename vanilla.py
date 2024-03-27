import numpy as np
from scipy.stats import norm


def pv(option_type, spot, strike, rf, b, vol, ttm):
    """
    calculate vanilla option pv
    :param option_type: "C" or "P"
    :type  option_type: str
    :param spot: spot price
    :type  spot: float
    :param strike: strike price
    :type  strike: float
    :param rf: risk-free rate
    :type rf: float
    :param b: carry cost
    :param vol: volatility
    :param ttm: time to maturity
    :return: pv of the option
    """

    d1 = (np.log(spot / strike) + (b + 0.5 * vol ** 2) * ttm) / (vol * np.sqrt(ttm))
    d2 = d1 - vol * np.sqrt(ttm)

    # Price of the call option
    if option_type.lower() == "c":
        return spot * np.exp(-(rf - b) * ttm) * norm.cdf(d1) - strike * np.exp(-rf * ttm) * norm.cdf(d2)

    elif option_type.lower() == "p":
        return strike * np.exp(-rf * ttm) * norm.cdf(-d2) - spot * np.exp(-(rf - b) * ttm) * norm.cdf(-d1)

    else:
        raise ValueError("Unknown option type!")
