#!/usr/bin/env python3
"""Exact rational replay of constants already appearing in the authored proof.

This checks scalar arithmetic, not an operator identity or an infinite frame.
The proof of those statements is in accepted/core/COUNTEREXAMPLE.md.
All checks remain active under Python -O and -OO.
"""
from fractions import Fraction as Q
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    epsilon = Q(1, 100)
    q = 2 * epsilon + epsilon ** 2
    remainder_upper = q ** 2 / (1 - q)
    rb_upper = remainder_upper + epsilon ** 2 / 2
    error_upper = epsilon ** 2 + rb_upper * (1 + epsilon)
    stated_error_factor = Q(3937, 200)
    checks = {
        'epsilon_is_one_hundredth': epsilon == Q(1, 100),
        'lower_frame_bound': (1 - epsilon) ** 2 == Q(9801, 10000),
        'upper_frame_bound': (1 + epsilon) ** 2 == Q(10201, 10000),
        'q': q == Q(201, 10000),
        'q_less_than_three_epsilon': q < 3 * epsilon,
        'q_less_than_one_half': q < Q(1, 2),
        'remainder_bound': remainder_upper < 18 * epsilon ** 2,
        'adjusted_remainder_bound': rb_upper < Q(37, 2) * epsilon ** 2,
        'stated_error_factor': 1 + Q(37, 2) * (1 + epsilon) == stated_error_factor,
        'error_factor_less_than_twenty': stated_error_factor < 20,
        'error_bound': error_upper < 20 * epsilon ** 2,
        'displayed_defect_threshold': epsilon / 2 - 40 * epsilon ** 2 == Q(1, 1000),
    }
    for name, passed in checks.items():
        require(passed, 'Scalar diagnostic failed: ' + name)
    report = {
        'status': 'PASS',
        'optimization_flag': sys.flags.optimize,
        'arithmetic': 'exact rational; Python standard-library fractions.Fraction',
        'scope': 'Constants in the existing proof only; no finite-dimensional truncation and no mathematical proof certification.',
        'checks': checks,
        'values': {'epsilon': str(epsilon), 'q': str(q),
                   'lower_frame_bound': str((1 - epsilon) ** 2),
                   'upper_frame_bound': str((1 + epsilon) ** 2),
                   'stated_error_factor': str(stated_error_factor),
                   'stated_defect_threshold': str(Q(1, 1000))},
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
