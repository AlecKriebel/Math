#!/usr/bin/env python3
"""Targeted exact checks of the reversed-arrow intermediate dual.

This is a discovery aid, not a certificate.  It compares stationary mean
sizes of the Bd dual L, the row-P unbatched reversed-arrow generator C, and
the geometric-burst dB dual D on a few hand-selected rational graphs.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random

import sympy as sp


SOURCE = Path(__file__).parents[1] / "verify_exact_duals.py"
SPEC = importlib.util.spec_from_file_location("exact_duals", SOURCE)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def mean_size(generator: sp.Matrix) -> sp.Expr:
    pi = MOD.stationary(generator)
    return sp.cancel(
        sum(
            pi[state - 1] * state.bit_count()
            for state in range(1, generator.rows + 1)
        )
    )


def slacks(weights: list[list[int]]) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    r = sp.Rational(3, 2)
    l_gen = MOD.dual_generator(weights, r, "Bd")
    c_gen = MOD.reversed_arrow_generator(weights, r)
    d_gen = MOD.dual_generator(weights, r, "dB")
    means = tuple(map(mean_size, (l_gen, c_gen, d_gen)))
    n = len(weights)
    a = r - 1
    mu_mean = n * a * (1 + a) ** (n - 1) / ((1 + a) ** n - 1)
    hole_mean = (n - 1) * a * (1 + a) ** (n - 2) / (
        (1 + a) ** (n - 1) - 1
    )
    return (
        sp.factor(means[2] - means[1]),
        sp.factor(means[0] * means[1] - mu_mean**2),
        sp.factor(means[2] / means[1] - hole_mean / mu_mean),
    )


def audit(weights: list[list[int]]) -> None:
    print("n", len(weights), "slacks D-C, LC, normalized DC", slacks(weights))


def main() -> None:
    graphs = (
        [[0, 1, 4], [1, 0, 2], [4, 2, 0]],
        [[0, 1, 0, 0], [1, 0, 2, 0], [0, 2, 0, 3], [0, 0, 3, 0]],
        [[0, 1, 1, 1], [1, 0, 4, 0], [1, 4, 0, 2], [1, 0, 2, 0]],
        [
            [0, 1, 0, 0, 7],
            [1, 0, 2, 0, 3],
            [0, 2, 0, 5, 0],
            [0, 0, 5, 0, 4],
            [7, 3, 0, 4, 0],
        ],
    )
    for graph in graphs:
        audit(graph)
    rng = random.Random(20260802)
    for n, trials in ((3, 40), (4, 40)):
        for trial in range(trials):
            graph = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    graph[i][j] = graph[j][i] = rng.randint(1, 20)
            values = slacks(graph)
            if any(value > 0 for value in values):
                print("SPLIT COUNTEREXAMPLE", n, trial, values, graph)
                return
        print("random exact split screen passed", n, trials)


if __name__ == "__main__":
    main()
