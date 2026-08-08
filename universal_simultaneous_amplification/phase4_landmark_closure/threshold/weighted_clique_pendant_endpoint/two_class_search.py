#!/usr/bin/env python3
"""Hostile endpoint search with two symmetric pendant-weight classes.

The graph has a unit clique on a hub and ``c`` ordinary vertices, ``a``
leaves of weight ``u`` and ``b`` leaves of weight ``v``.  This is a
discovery implementation; exact certification is required for any witness.
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from itertools import product

import numpy as np
from scipy.optimize import differential_evolution
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


R = 1.5


def all_states(c, a, b):
    return product((0, 1), range(c + 1), range(a + 1), range(b + 1))


def changing_moves(rule, state, c, a, b, u, v):
    h, i, j, k = state
    n = 1 + c + a + b
    out = defaultdict(float)
    if rule == "Bd":
        F = n + (R - 1) * (h + i + j + k)
        d = c + a * u + b * v
        if h == 0:
            out[(1, i, j, k)] += R * (i / c + j + k) / F
        else:
            out[(0, i, j, k)] += ((c - i) / c + a - j + b - k) / F
        if i < c:
            out[(h, i + 1, j, k)] += R * (c - i) * (h / d + i / c) / F
        if i:
            out[(h, i - 1, j, k)] += i * ((1 - h) / d + (c - i) / c) / F
        if j < a:
            out[(h, i, j + 1, k)] += R * h * u * (a - j) / (d * F)
        if j and not h:
            out[(h, i, j - 1, k)] += u * j / (d * F)
        if k < b:
            out[(h, i, j, k + 1)] += R * h * v * (b - k) / (d * F)
        if k and not h:
            out[(h, i, j, k - 1)] += v * k / (d * F)
    else:
        mutant_load = i + u * j + v * k
        resident_load = c - i + u * (a - j) + v * (b - k)
        den = R * mutant_load + resident_load
        if h == 0 and mutant_load:
            out[(1, i, j, k)] += R * mutant_load / (n * den)
        if h == 1 and resident_load:
            out[(0, i, j, k)] += resident_load / (n * den)
        if i < c and h + i:
            out[(h, i + 1, j, k)] += (c - i) * R * (h + i) / (
                n * (R * (h + i) + c - h - i)
            )
        if i and c - h - i + 1:
            out[(h, i - 1, j, k)] += i * (c - h - i + 1) / (
                n * (R * (h + i - 1) + c - h - i + 1)
            )
        if j < a and h:
            out[(h, i, j + 1, k)] += (a - j) / n
        if j and not h:
            out[(h, i, j - 1, k)] += j / n
        if k < b and h:
            out[(h, i, j, k + 1)] += (b - k) / n
        if k and not h:
            out[(h, i,j, k - 1)] += k / n
    return out


def baseline(rule, n):
    if rule == "Bd":
        return (1 - 1 / R) / (1 - R ** (-n))
    return (n - 1) / n * (1 - 1 / R) / (1 - R ** (-(n - 1)))


def fixation(rule, c, a, b, u, v):
    extinct, fixed = (0, 0, 0, 0), (1, c, a, b)
    transient = [s for s in all_states(c, a, b) if s not in (extinct, fixed)]
    index = {s: q for q, s in enumerate(transient)}
    rr, cc, data, rhs = [], [], [], np.zeros(len(transient))
    for row, state in enumerate(transient):
        moves = changing_moves(rule, state, c, a, b, u, v)
        rr.append(row); cc.append(row); data.append(sum(moves.values()))
        for target, probability in moves.items():
            if target == fixed:
                rhs[row] += probability
            elif target != extinct:
                rr.append(row); cc.append(index[target]); data.append(-probability)
    A = coo_matrix((data, (rr, cc)), shape=(len(transient),) * 2).tocsr()
    ans = spsolve(A, rhs)
    n = 1 + c + a + b
    rho = (
        ans[index[(1, 0, 0, 0)]]
        + c * ans[index[(0, 1, 0, 0)]]
        + a * ans[index[(0, 0, 1, 0)]]
        + b * ans[index[(0, 0, 0, 1)]]
    ) / n
    return rho / baseline(rule, n)


def ratios(c, a, b, z):
    u, v = math.exp(z[0]), math.exp(z[1])
    x = fixation("Bd", c, a, b, u, v)
    y = fixation("dB", c, a, b, u, v)
    return u, v, x, y, min(x, y), (x + 2 * y) / 3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=14)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument("--maxiter", type=int, default=35)
    parser.add_argument("--objective", choices=("M", "S"), default="M")
    args = parser.parse_args()
    best = None
    for n in range(4, args.max_n + 1):
        for a in range(1, n - 2):
            for b in range(1, n - 1 - a):
                c = n - 1 - a - b
                column = 4 if args.objective == "M" else 5
                objective = lambda z: -ratios(c, a, b, z)[column]
                opt = differential_evolution(
                    objective,
                    [(-9.21, 9.21), (-9.21, 9.21)],
                    seed=args.seed + 1000 * n + 31 * a + b,
                    maxiter=args.maxiter,
                    popsize=7,
                    polish=True,
                    updating="immediate",
                    workers=1,
                    tol=1e-7,
                )
                values = ratios(c, a, b, opt.x)
                row = (*values, c, a, b)
                if best is None or row[column] > best[column]:
                    best = row
                if row[column] > 0.999:
                    print(
                        f"n={n} c={c} a={a} b={b} u={row[0]:.8g} "
                        f"v={row[1]:.8g} Bd={row[2]:.12f} "
                        f"dB={row[3]:.12f} M={row[4]:.12f} S={row[5]:.12f}",
                        flush=True,
                    )
        print(
            f"through n={n}: best c,a,b={best[6:]} u,v={best[:2]} "
            f"Bd,dB,M,S={best[2:6]}",
            flush=True,
        )


if __name__ == "__main__":
    main()
