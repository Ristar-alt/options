import numpy as np


class Snowball:
    def __init__(self, ko_dates, ko_barriers, ki_barrier):

        self.ko_dates = ko_dates
        self.ko_barriers = ko_barriers
        self.ki_barrier = ki_barrier


def issue_snowball(snowball, price_series):
    initial_price = price_series[0]
    total_term = snowball.ko_dates[-1]

    ko_prices = price_series[snowball.ko_dates] / initial_price

    ko_status = ko_prices >= snowball.ko_barriers

    ki_status = np.any(price_series[:total_term + 1] / initial_price < snowball.ki_barrier)

    duration = 0
    ki = False
    pnl = 0
    if np.any(ko_status):
        ko_index = np.argmax(ko_status)
        duration = snowball.ko_dates[ko_index]
        pnl = duration

    elif ki_status:
        duration = total_term
        ki = True
        pnl = min(price_series[total_term] / initial_price - 1, 0)

    else:
        duration = total_term
        pnl = duration

    return ki, duration, pnl
