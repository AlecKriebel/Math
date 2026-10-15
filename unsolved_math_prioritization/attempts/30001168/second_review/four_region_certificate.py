#!/usr/bin/env python3
"""Exact arithmetic for a four-region all-time round-trace bound.

No code or routines are imported from either previous certificate. The
geometric and spectral claims are analytic obligations in SECOND_REVIEW.md.
"""
from fractions import Fraction as Q
import json
import sys


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def positive_exp_bounds(x, n):
    require(x >= 0 and n >= 0 and x < n + 2, 'Taylor tail range')
    term = total = Q(1)
    for k in range(1, n + 1):
        term = term * x / k
        total += term
    first_omitted = term * x / (n + 1)
    upper = total + first_omitted / (1 - x / (n + 2))
    return total, upper


def exp_minus_upper(x):
    require(x > 0, 'strictly positive exponential argument')
    return 1 / positive_exp_bounds(x, 40)[0]


def root_upper(x):
    # Explicit brackets, each verified by exact squaring.
    numerators = {Q(3, 2): 1224745, Q(13, 8): 1274755,
                  Q(7, 4): 1322876, Q(2): 1414214}
    hi = Q(numerators[x], 10**6)
    lo = hi - Q(1, 10**6)
    require(lo * lo <= x < hi * hi, 'explicit square root bracket')
    return hi


def prefactor(t):
    return t * root_upper(t)


def first_mode_upper(t):
    return prefactor(t) * exp_minus_upper(3*t/4)


def higher_modes_upper(t):
    # Modes j>=2 decrease for t>=2/5. The j>=3 spectral tail has
    # consecutive ratio <=(16/9)e^(-7t)<1/2 for t>=3/2.
    require(t >= Q(3, 2), 'higher-mode tail time range')
    require(Q(16, 9)/(1 + 7*t) < Q(1, 2), 'geometric tail ratio')
    return prefactor(t) * (4*exp_minus_upper(15*t/4)
                          + 18*exp_minus_upper(35*t/4))


def decimal_upper(x):
    scale = 10**15
    k = x.numerator * scale // x.denominator + 1
    return str(k // scale) + '.' + str(k % scale).zfill(15)


def calculate(limit=Q(129, 200), length=10000):
    # Direct Gregory alternating series: pi/4=1-1/3+1/5-... .
    pi_lower = 4 * sum((Q((-1)**k, 2*k+1) for k in range(2000)), Q(0))
    pi_upper = pi_lower + Q(4, 4001)
    require(Q(157, 50) < pi_lower < pi_upper < Q(22, 7), 'pi enclosure')
    require(Q(1772, 1000)**2 < Q(157, 50), 'sqrt pi lower')
    require(Q(1773, 1000)**2 > Q(22, 7), 'sqrt pi upper')
    require(positive_exp_bounds(Q(1), 12)[1] < Q(2719, 1000), 'e upper')
    require(2*Q(157, 50)**2 > Q(3, 2), 'negative theta correction')
    require(Q(3, 2) > Q(2, 5), 'higher modes are decreasing')

    bounds = {
        '(0, 3/2]': Q(1773, 4000)*positive_exp_bounds(Q(3, 8), 12)[1],
        '[3/2, 13/8]': first_mode_upper(Q(13, 8)) + higher_modes_upper(Q(3, 2)),
        '[13/8, 7/4]': first_mode_upper(Q(7, 4)) + higher_modes_upper(Q(13, 8)),
        '[7/4, infinity)': first_mode_upper(Q(2)) + higher_modes_upper(Q(7, 4)),
    }
    for region, bound in bounds.items():
        require(bound < limit, 'round bound failed: ' + region)
    first_at_two_lower = 2*(root_upper(Q(2))-Q(1, 10**6))/positive_exp_bounds(Q(3, 2), 12)[1]
    require(first_at_two_lower > Q(1773, 4000), 'round value exceeds Weyl limit')
    require(Q(13, 20) > Q(1773, 4000), 'cylinder value exceeds Weyl limit')
    lower = Q(1772, 2719) * (length - 4*Q(1773, 1000))/(length+4)
    require(length > 4*Q(1773, 1000), 'positive Gaussian lower bound')
    require(lower > Q(13, 20) > limit, 'cylinder separation')
    return {
        'problem_id': 30001168,
        'accepted': True,
        'round_threshold': str(limit),
        'round_regions': {region: decimal_upper(bound) for region, bound in bounds.items()},
        'round_global_upper_decimal': decimal_upper(max(bounds.values())),
        'cylinder_length': length,
        'cylinder_rational_lower': str(lower),
        'cylinder_threshold': '13/20',
        'arithmetic': 'Fraction and integer only; displayed decimal upper bounds are rounded upward',
        'method': 'Four analytic time regions, separate modal monotonicity, a geometric spectral tail, positive Taylor bounds, and direct Gregory-series pi enclosure',
    }


if __name__ == '__main__':
    require(len(sys.argv) == 1, 'No command-line arguments supported')
    print(json.dumps(calculate(), indent=2, sort_keys=True))
