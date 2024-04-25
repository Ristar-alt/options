import time

import numpy as np


def generate_path(spot, b, vol, t, n_sim):
    """
    generate price series according to the market dynamics
    :param spot:  spot price
    :param b: carry cost
    :param vol: volatility
    :param t: times to valuation time
    :param n_sim: number of simulations
    :return: n_sim  simulated price paths, and discount factors
    """
    dts = np.diff(t)
    dts = np.insert(dts, 0, 0)
    drift = dts * (b - 0.5 * vol * vol)
    drift = np.cumsum(drift)

    eps = np.random.normal(0, 1, (n_sim, len(dts)))

    diffusion = vol * np.sqrt(dts) * eps
    diffusion = np.cumsum(diffusion, 1)
    x = drift + diffusion
    paths = spot * np.exp(x)

    return paths


class Snowball:
    def __init__(self,
                 initial_price,
                 start_day,
                 ko_days,
                 ko_barriers,
                 ko_coupon_rates,
                 ki_barrier,
                 ):
        self.initial_price = initial_price
        self.start_day = start_day
        self.ko_days = ko_days
        self.ko_coupon_rates = ko_coupon_rates
        self.ko_barriers = ko_barriers
        self.ki_barrier = ki_barrier
        self.is_ki = False

    def set_ki(self, ki_flag):
        self.is_ki = ki_flag

    def calculate_pv_by_mc(self, val_day, spot, r, b, vol, bus_days_in_year, n_sim):
        """

        :param val_day:
        :param spot:
        :param r:
        :param b:
        :param vol:
        :param bus_days_in_year
        :param n_sim:
        :return:
        """
        # extract out the structure for rest of its lifetime
        ko_days = []
        ko_coupons = []
        ko_barriers = []
        ki_barrier = self.ki_barrier * self.initial_price

        for i in range(len(self.ko_days)):
            if self.ko_days[i] >= val_day:
                ko_days.append(self.ko_days[i])
                coupon = self.ko_coupon_rates[i] * self.initial_price * (self.ko_days[i] - self.start_day + 1) / 365.0
                ko_coupons.append(coupon)
                ko_barriers.append(self.ko_barriers[i] * self.initial_price)

        ki_days = np.array([0])
        if not self.is_ki:
            ki_days = np.arange(0, ko_days[-1] + 1, 1, dtype=int)

        all_days = np.union1d(ki_days, ko_days)

        t = all_days / bus_days_in_year

        df = np.exp(-r * t)

        # simulate paths by monte carlo
        paths = generate_path(spot, b, vol, t, n_sim)

        # for simplicity use for loop
        pv = 0
        for i in range(n_sim):
            is_ko = False
            is_ki = self.is_ki

            # check if knock out at ko days
            for k in range(len(ko_days)):
                time_index = ko_days[k]
                if paths[i][time_index] >= ko_barriers[k]:
                    is_ko = True
                    pv += ko_coupons[k] * df[time_index]
                    break

            if not is_ko and not is_ki:
                for k in range(len(ki_days)):
                    time_index = ki_days[k]
                    if paths[i][time_index] < ki_barrier:
                        is_ki = True
                        break

            if not is_ko and is_ki:
                pv += min(paths[i][ko_days[-1]] - self.initial_price, 0.0) * df[-1]

            if not is_ko:
                pv += ko_coupons[-1] * df[-1]

        return pv / n_sim


my_snowball = Snowball(1,
                       0,
                       np.array([20, 40, 60, 80, 100]),
                       np.array([1, 1, 1, 1, 1]),
                       np.array([1, 1, 1, 1, 1]),
                       0.8)

s_time = time.time()
pv = my_snowball.calculate_pv_by_mc(0, 1, 0.03, 0, 0.2, 242, 100000)
e_time = time.time()
print(e_time - s_time)

print(pv)
