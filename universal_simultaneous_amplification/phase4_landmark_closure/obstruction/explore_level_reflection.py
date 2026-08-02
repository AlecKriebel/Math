#!/usr/bin/env python3
"""Exact diagnostics for the open reflected-level inequality.

This is a discovery script, not a proof certificate.  It computes the
stationary law of the geometric-OR dB dual and tests both the aggregate
conjecture and the stronger pointwise complement comparison after tilting by
``(r-1)^-|A|``.
"""

from __future__ import annotations

import itertools
import pathlib
import sys

import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verify_exact_duals import dual_generator, stationary  # noqa: E402


def analyse(weights: list[list[int]], fitness: sp.Rational) -> None:
    n = len(weights)
    full = (1 << n) - 1
    invariant = stationary(dual_generator(weights, fitness, "dB"))
    a = fitness - 1
    tilted = {
        state: sp.cancel(invariant[state - 1] / a ** state.bit_count())
        for state in range(1, full + 1)
    }
    levels = {
        k: sp.cancel(
            sum(
                tilted[state]
                for state in range(1, full + 1)
                if state.bit_count() == k
            )
        )
        for k in range(1, n)
    }
    print("weights", weights, "r", fitness)
    for k in range(n // 2 + 1, n):
        slack = sp.cancel((n - k) * levels[n - k] - k * levels[k])
        pointwise = []
        for state in range(1, full):
            if state.bit_count() != k:
                continue
            pointwise.append(
                sp.cancel((n - k) * tilted[full ^ state] - k * tilted[state])
            )
        print(" level", k, "slack", slack)
        print(" pointwise signs", [sp.sign(x) for x in pointwise])


def main() -> None:
    graphs = [
        [[0, 1, 0], [1, 0, 2], [0, 2, 0]],
        [[0, 1, 3, 0], [1, 0, 2, 4], [3, 2, 0, 5], [0, 4, 5, 0]],
        [[0, 1, 0, 0, 2], [1, 0, 3, 0, 0], [0, 3, 0, 4, 0],
         [0, 0, 4, 0, 5], [2, 0, 0, 5, 0]],
    ]
    for weights, fitness in itertools.product(
        graphs, [sp.Rational(3, 2), sp.Rational(2), sp.Rational(3)]
    ):
        analyse(weights, fitness)


if __name__ == "__main__":
    main()
