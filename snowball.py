import numpy as np

# ===============
#
# define the structure to be valuated
days_in_year = 365.0
bus_days_in_year = 242
initial_price = 1.0
ko_days = np.array([20, 40, 60, 80, 100])
ko_barriers = np.array([1, 1, 1, 1, 1])
ki_barrier = 0.8 * initial_price
ki_days = np.arange(0, 101, 1, dtype=int)
coupon_rate = 365.0
ko_coupons = ko_days / days_in_year * coupon_rate * initial_price
# ===================

# define market dynamics
spot = 1.0
rf = 0.00
b = 0
vol = 0.2
# ====


df = np.exp(-rf * ki_days / bus_days_in_year)

dt = np.diff(ki_days) / bus_days_in_year

drift = dt * (b - 0.5 * vol * vol)
drift = np.cumsum(drift)

sim_n = 100000
ob_size = len(ki_days) - 1
eps = np.random.normal(0, 1, ob_size * sim_n)
total_pv = 0
for k in range(sim_n):
    pv = 0
    diffusion = vol * np.sqrt(dt) * eps[k * ob_size:(k + 1) * ob_size]
    diffusion = np.cumsum(diffusion)
    x = drift + diffusion
    prices = spot * np.exp(x)
    prices = np.insert(prices, 0, spot)
    ko_flag = False
    ki_flag = False
    for i in range(len(ko_days)):
        if prices[ko_days[i]] >= ko_barriers[i]:
            pv = ko_coupons[i] * df[ko_days[i]]
            ko_flag = True
            break

    if not ko_flag:
        for i in range(len(ki_days)):
            if prices[ki_days[i]] <= ki_barrier:
                ki_flag = True
                break

    if not ki_flag and not ko_flag:
        pv = ko_coupons[-1] * df[-1]

    elif ki_flag and not ko_flag:
        pv = np.min([prices[-1] - initial_price, 0], 0) * df[ko_days[-1]]

    total_pv += pv

print(total_pv / sim_n)
