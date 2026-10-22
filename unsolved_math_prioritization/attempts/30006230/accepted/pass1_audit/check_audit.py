#!/usr/bin/env python3
"""Independent exact arithmetic and radial/mode integration-by-parts checks.
These checks supplement, and do not replace, the mathematical audit.
"""
from fractions import Fraction as F
from math import factorial
import json

checks = {}
def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks[name] = True

exp4_lower = sum(F(4**j, factorial(j)) for j in range(8))
require('exp4_series_lower_exceeds_50', exp4_lower > 50)
require('pi_bound_squared_below_10', F(22,7)**2 < 10)
trial_upper = F(9,4)+F(1,10)+F(1,50)
require('trial_upper_below_19_over_8', trial_upper < F(19,8))
require('19_over_8_below_12_over_5', F(19,8) < F(12,5))
require('12_over_5_below_5_over_2', F(12,5) < F(5,2))
# For Q=5,V=1, integrating the cross term by parts gives a*(a-2).
for k in range(1,101):
    a = k*(k+3)
    # -a*(m-2)*(m-3) + a*m*(m-3) + a*a - a*m, m=4.
    raw = -a*2*1 + a*4*1 + a*a-a*4
    require(f'mode_{k}_coefficient', raw == a*(a-2))
    require(f'mode_{k}_positive_uniform_margin', F(a)-F(3,2)-F(12,5) >= F(1,10))
# The actual all-size argument is monotonicity a=k(k+3)>=4, not this finite loop.
print(json.dumps({
    'status':'PASS',
    'checks':checks,
    'exact_exp4_lower':str(exp4_lower),
    'exact_trial_upper':str(trial_upper),
    'strict_trial_margin_to_19_over_8':str(F(19,8)-trial_upper),
    'all_size_mode_argument':'a=k(k+3)>=4; a-3/2-lambda > 4-3/2-12/5=1/10',
    'limits':'Finite arithmetic smoke checks are not the universal proof; see the acceptance report.'
}, indent=2, sort_keys=True))
