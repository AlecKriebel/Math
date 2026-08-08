#!/usr/bin/env python3
"""Discovery-only diagnostics for two-dual rank convolution inequalities.

All chain equations are built exactly by ``verify_exact_duals``.  This file
tests possible strengthenings of the fixation-product conjecture and prints
the first exact rational counterexample to each failed strengthening.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import sympy as sp


OBSTRUCTION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OBSTRUCTION))
from verify_exact_duals import dual_generator, stationary  # noqa: E402


R = sp.Rational(3, 2)


def rank_law(weights, rule):
    n = len(weights)
    invariant = stationary(dual_generator(weights, R, rule))
    law = [sp.Integer(0)] * (n + 1)
    for state, mass in enumerate(invariant, start=1):
        law[state.bit_count()] += mass
    return list(map(sp.cancel, law))


def convolution(left, right):
    answer = [sp.Integer(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return list(map(sp.cancel, answer))


def complete_laws(n):
    a = R - 1
    z_b = (1 + a) ** n - 1
    bd = [sp.Integer(0)] + [
        sp.binomial(n, k) * a**k / z_b for k in range(1, n + 1)
    ]
    z_d = n * ((1 + a) ** (n - 1) - 1)
    db = [sp.Integer(0)] + [
        sp.binomial(n, k) * (n - k) * a**k / z_d
        for k in range(1, n + 1)
    ]
    assert sum(bd) == sum(db) == 1
    return bd, db


def connected(weights):
    n = len(weights)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j, value in enumerate(weights[i]):
            if value and j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == n


def random_graph(n, rng):
    while True:
        weights = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.7:
                    value = sp.Integer(rng.choice((1, 1, 2, 3, 7, 19)))
                    weights[i][j] = weights[j][i] = value
        if connected(weights):
            return tuple(map(tuple, weights))


def main():
    rng = random.Random(20260802)
    alive = {
        "sum-tail": True,
        "sum-cdf": True,
        "sum-pgf-z-half": True,
        "rank-product-tail": True,
        "factorial-products-j2": True,
    }
    for n in (3, 4, 5):
        kb, kd = complete_laws(n)
        kconv = convolution(kb, kd)
        kprod_tail = {
            threshold: sum(
                kb[i] * kd[j]
                for i in range(n + 1)
                for j in range(n + 1)
                if i * j >= threshold
            )
            for threshold in range(1, n * n + 1)
        }
        trials = 40 if n < 5 else 8
        for trial in range(trials):
            weights = random_graph(n, rng)
            bd = rank_law(weights, "Bd")
            db = rank_law(weights, "dB")
            conv = convolution(bd, db)
            diagnostics = {}
            diagnostics["sum-tail"] = min(
                sum(kconv[t:]) - sum(conv[t:])
                for t in range(2, 2 * n + 1)
            )
            diagnostics["sum-cdf"] = min(
                sum(conv[: t + 1]) - sum(kconv[: t + 1])
                for t in range(2, 2 * n + 1)
            )
            z = sp.Rational(1, 2)
            diagnostics["sum-pgf-z-half"] = sum(
                conv[t] * z**t for t in range(len(conv))
            ) - sum(kconv[t] * z**t for t in range(len(kconv)))
            diagnostics["rank-product-tail"] = min(
                kprod_tail[threshold]
                - sum(
                    bd[i] * db[j]
                    for i in range(n + 1)
                    for j in range(n + 1)
                    if i * j >= threshold
                )
                for threshold in range(1, n * n + 1)
            )
            diagnostics["factorial-products-j2"] = (
                sum(sp.binomial(i, 2) * bd[i] for i in range(n + 1))
                * sum(sp.binomial(i, 2) * db[i] for i in range(n + 1))
                - sum(sp.binomial(i, 2) * kb[i] for i in range(n + 1))
                * sum(sp.binomial(i, 2) * kd[i] for i in range(n + 1))
            )
            for label, slack in diagnostics.items():
                if alive[label] and slack < 0:
                    alive[label] = False
                    print("COUNTEREXAMPLE", label, "n", n, "trial", trial)
                    print("weights =", weights)
                    print("signed slack =", sp.factor(slack))
        print("finished order", n, "survivors", [k for k, v in alive.items() if v])


if __name__ == "__main__":
    main()
