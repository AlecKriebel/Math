#!/usr/bin/env python3
"""Exact counterexample to pairwise negative correlation at r=2.

This is a route-falsification certificate only.  It does not contradict the
aggregate reflected-level conjecture.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


OBSTRUCTION = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(OBSTRUCTION))

from verify_exact_duals import dual_generator, stationary  # noqa: E402


def main() -> None:
    # Edge order (01,02,03,12,13,23)=(30,20,30,20,30,1).
    weights = [
        [0, 30, 20, 30],
        [30, 0, 20, 30],
        [20, 20, 0, 1],
        [30, 30, 1, 0],
    ]
    invariant = stationary(
        dual_generator(weights, sp.Integer(2), "dB")
    )
    marginals = [
        sum(
            invariant[state - 1]
            for state in range(1, 16)
            if (state >> vertex) & 1
        )
        for vertex in range(4)
    ]
    pair_23 = sum(
        invariant[state - 1]
        for state in range(1, 16)
        if (state >> 2) & 1 and (state >> 3) & 1
    )
    covariance = sp.cancel(pair_23 - marginals[2] * marginals[3])
    expected = sp.Rational(
        80738385242712417797218479495402739,
        12986979462920913004371912333407883289,
    )
    assert covariance == expected
    assert covariance > 0
    print("PASS exact positive-covariance counterexample")
    print(f"Cov(1_2,1_3) = {covariance}")


if __name__ == "__main__":
    main()
