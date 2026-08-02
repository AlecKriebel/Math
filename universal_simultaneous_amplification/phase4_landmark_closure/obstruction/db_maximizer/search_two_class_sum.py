#!/usr/bin/env python3
"""Reconnaissance for the Bd+dB sum on two equitable weighted classes.

There are ``a`` vertices of type A and ``b`` vertices of type B.  Every A--A
edge has weight ``alpha``, every B--B edge has weight ``beta``, and every
A--B edge has weight one.  The state is the pair of mutant counts ``(i,j)``.
Only the four count-changing transitions are retained; conditioning on a
change leaves all absorption probabilities unchanged.

This is floating-point discovery code, not a proof certificate.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import differential_evolution, minimize

from search_db import baseline, baseline_bd


def _rates(a: int, b: int, alpha: float, beta: float, r: float, rule: str):
    n = a + b
    d_a = alpha * (a - 1) + b
    d_b = beta * (b - 1) + a
    for i in range(a + 1):
        for j in range(b + 1):
            if i + j in (0, n):
                continue
            if rule == "Bd":
                total = n + (r - 1) * (i + j)
                yield (i, j), (
                    r * (a - i) * (i * alpha / d_a + j / d_b) / total,
                    i * ((a - i) * alpha / d_a + (b - j) / d_b) / total,
                    r * (b - j) * (j * beta / d_b + i / d_a) / total,
                    j * ((b - j) * beta / d_b + (a - i) / d_a) / total,
                )
            elif rule == "dB":
                ma = alpha * i + j
                ra = alpha * (a - i - 1) + (b - j)
                a_up = (a - i) / n * (r * ma / (r * ma + ra)) if a > i else 0.0
                ma_without = alpha * (i - 1) + j
                ra_full = alpha * (a - i) + (b - j)
                a_down = i / n * (ra_full / (r * ma_without + ra_full)) if i else 0.0

                mb = beta * j + i
                rb = beta * (b - j - 1) + (a - i)
                b_up = (b - j) / n * (r * mb / (r * mb + rb)) if b > j else 0.0
                mb_without = beta * (j - 1) + i
                rb_full = beta * (b - j) + (a - i)
                b_down = j / n * (rb_full / (r * mb_without + rb_full)) if j else 0.0
                yield (i, j), (a_up, a_down, b_up, b_down)
            else:
                raise ValueError(rule)


def fixation(a: int, b: int, alpha: float, beta: float, r: float, rule: str):
    n = a + b
    states = [
        (i, j)
        for i in range(a + 1)
        for j in range(b + 1)
        if 0 < i + j < n
    ]
    index = {state: k for k, state in enumerate(states)}
    rows, cols, data = [], [], []
    rhs = np.zeros(len(states))
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for state, raw in _rates(a, b, alpha, beta, r, rule):
        row = index[state]
        changing = sum(raw)
        if not changing > 0:
            raise ArithmeticError((state, raw))
        rows.append(row); cols.append(row); data.append(1.0)
        for probability, step in zip(raw, steps):
            if not probability:
                continue
            target = state[0] + step[0], state[1] + step[1]
            probability /= changing
            if sum(target) == n:
                rhs[row] += probability
            elif sum(target) > 0:
                rows.append(row); cols.append(index[target]); data.append(-probability)
    matrix = sp.csr_matrix((data, (rows, cols)), shape=(len(states), len(states)))
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    answer = (a * values[index[(1, 0)]] + b * values[index[(0, 1)]]) / n
    return float(answer), residual


def objective(logs, a: int, b: int, r: float):
    alpha, beta = np.exp(np.clip(logs, -30, 30))
    try:
        bd, e1 = fixation(a, b, alpha, beta, r, "Bd")
        db, e2 = fixation(a, b, alpha, beta, r, "dB")
    except Exception:
        return 10.0
    if max(e1, e2) > 1e-7 or not (-1e-8 <= bd <= 1 + 1e-8 and -1e-8 <= db <= 1 + 1e-8):
        return 10.0
    return baseline(a + b, r) + baseline_bd(a + b, r) - bd - db


def optimize(a: int, b: int, r: float, bound: float, seed: int):
    result = differential_evolution(
        objective, [(-bound, bound)] * 2, args=(a, b, r), seed=seed,
        maxiter=45, popsize=10, polish=False, tol=1e-9,
    )
    starts = [result.x, np.zeros(2)]
    rng = np.random.default_rng(seed + 11)
    starts += list(rng.uniform(-bound, bound, size=(8, 2)))
    candidates = []
    for start in starts:
        polished = minimize(
            objective, start, args=(a, b, r), method="Nelder-Mead",
            options={"maxiter": 500, "xatol": 1e-10, "fatol": 1e-12},
        )
        candidates.append(polished)
    best = min(candidates, key=lambda x: x.fun)
    logs = np.clip(best.x, -30, 30)
    alpha, beta = np.exp(logs)
    bd, e1 = fixation(a, b, alpha, beta, r, "Bd")
    db, e2 = fixation(a, b, alpha, beta, r, "dB")
    return dict(excess=-best.fun, alpha=alpha, beta=beta, bd=bd, db=db,
                residual=max(e1, e2), logs=logs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--fitness", type=float, default=1.5)
    parser.add_argument("--bound", type=float, default=16)
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--stride", type=int, default=1)
    args = parser.parse_args()
    records = []
    for a in range(1, args.size, args.stride):
        b = args.size - a
        result = optimize(a, b, args.fitness, args.bound, args.seed + 101 * a)
        records.append((result["excess"], a, result))
        print(a, b, result, flush=True)
    print("BEST", max(records, key=lambda x: x[0]))


if __name__ == "__main__":
    main()
