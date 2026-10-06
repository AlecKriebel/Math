#!/usr/bin/env python3
"""Exact rational certificate for the numerical inequalities in PROOF.md.

Only Python's standard library is used. Run with python -I -B certificate.py.
All acceptance checks are explicit exceptions and remain active under -O.
This certificate checks arithmetic, not the analytic lemmas in PROOF.md.
"""
from fractions import Fraction as Q
from math import isqrt
import json
import sys

L = 10000
ROUND_BOUND = Q(129, 200)
CYLINDER_BOUND = Q(13, 20)
CHECKS = 0


def require(condition, description):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(description)


def exp_series(x, degree):
    term = Q(1)
    total = term
    for k in range(1, degree + 1):
        term *= x / k
        total += term
    return total, term


def exp_negative_upper(x):
    require(x > 0, "positive exponential argument")
    total, _ = exp_series(x, 64)
    return 1 / total


def sqrt_upper(x):
    scale = 10**9
    floor = isqrt(x.numerator * scale**2 // x.denominator)
    lo, hi = Q(floor, scale), Q(floor + 1, scale)
    require(lo * lo <= x < hi * hi, "integer square-root enclosure")
    return hi


def atan_interval(x, pairs):
    # Alternating series: even number of terms is a lower bound;
    # adding the next positive term is an upper bound.
    lo = sum(((-1)**k * x**(2*k + 1) / (2*k + 1)
              for k in range(2*pairs)), Q(0))
    hi = lo + x**(4*pairs + 1) / (4*pairs + 1)
    return lo, hi


def decimal_bound(x, upward=False, digits=12):
    scale = 10**digits
    n = x.numerator * scale // x.denominator
    if upward:
        n += 1
    return f"{n // scale}.{n % scale:0{digits}d}"


def calculate():
    # Machin identity: pi = 16 atan(1/5) - 4 atan(1/239).
    a_lo, a_hi = atan_interval(Q(1, 5), 8)
    b_lo, b_hi = atan_interval(Q(1, 239), 4)
    pi_lo, pi_hi = 16*a_lo - 4*b_hi, 16*a_hi - 4*b_lo
    require(pi_lo > Q(157, 50), "pi > 3.14")
    require(pi_hi < Q(22, 7), "pi < 22/7")
    require(Q(1772, 1000)**2 < Q(157, 50), "sqrt(pi) > 1.772")
    require(Q(1773, 1000)**2 > Q(22, 7), "sqrt(pi) < 1.773")

    # The exponential tail after degree 10 has first term term/11
    # and all subsequent ratios <= 1/12.
    total, term = exp_series(Q(1), 10)
    e_hi = total + (term/11) / (1-Q(1, 12))
    require(e_hi < Q(2719, 1000), "e < 2.719")
    require(Q(8, 3) < Q(1) + 3 + Q(9, 2), "cap integral bound: e^3 > 8/3")

    small_time_upper = Q(1773, 3000)
    require(small_time_upper < ROUND_BOUND, "small-time bound")
    require(2*Q(157, 50)**2 > 1, "negative theta correction for t <= 1")
    require(Q(25, 16) / (1+9) < Q(1, 2), "round spectral-tail ratio < 1/2")

    cells = []
    for k in range(100, 200):
        a, b = Q(k, 100), Q(k+1, 100)
        prefactor = b * sqrt_upper(b)
        terms = sum((j*j*exp_negative_upper(a*(j*j-Q(1, 4)))
                     for j in (1, 2, 3)), Q(0))
        tail = 32*exp_negative_upper(63*a/4)
        bound = prefactor*(terms+tail)
        require(bound < ROUND_BOUND, f"round interval [{a}, {b}]")
        cells.append((k, bound))
    require(len(cells) == 100, "100 intervals")
    worst_k, worst = max(cells, key=lambda item: item[1])

    lower = Q(1772, 2719) * Q(1000*L-4*1773, 1000*(L+4))
    require(L-4*Q(1773, 1000) > 0, "positive cylinder lower bound")
    require(lower > CYLINDER_BOUND, "finite-cylinder strict separation")
    require(CYLINDER_BOUND > ROUND_BOUND, "separated constants")

    return {
        "problem_id": 30001168,
        "dimension": 3,
        "cylinder_length": L,
        "round_uniform_upper_threshold": "129/200",
        "round_grid_certified_upper_decimal": decimal_bound(worst, True),
        "round_grid_worst_interval": [f"{worst_k}/100", f"{worst_k+1}/100"],
        "round_small_time_upper": "1773/3000",
        "cylinder_strict_lower_threshold": "13/20",
        "cylinder_rational_lower": f"{lower.numerator}/{lower.denominator}",
        "cylinder_lower_decimal": decimal_bound(lower),
        "strict_threshold_gap": "1/200",
        "grid_cells": len(cells),
        "checks": CHECKS,
        "arithmetic": "integer and Fraction only; displayed decimals are outward rounded",
        "scope": "Arithmetic certificate only; analytic construction and min-max argument in PROOF.md",
    }


if __name__ == "__main__":
    if len(sys.argv) != 1:
        raise SystemExit("No command-line arguments are accepted.")
    print(json.dumps(calculate(), indent=2, sort_keys=True))
