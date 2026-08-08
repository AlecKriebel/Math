#!/usr/bin/env python3
"""Search for a genuinely two-dual pointwise Poisson certificate.

The baseline potential is the sum of the exact complete-chain radial
Poisson solutions for normalized Bd and dB rank.  We then ask whether a
bilinear overlap correction ``sum_ij c_ij 1(i in A)1(j in B)`` makes its
drift dominate the normalized-rank target on the product of the actual Bd
and dB duals.  Feasibility is discovery evidence only; infeasibility is
converted to exact rational data separately before any claim is made.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linprog


OBSTRUCTION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OBSTRUCTION))
from verify_exact_duals import dual_generator, stationary  # noqa: E402


R = sp.Rational(3, 2)


def complete_weights(n):
    return tuple(tuple(0 if i == j else 1 for j in range(n)) for i in range(n))


def poisson(generator, invariant, target):
    """Solve Q f=target with invariant-mean-zero normalization exactly."""
    q = generator.copy()
    rhs = sp.Matrix(target)
    assert sp.cancel(sum(invariant[i] * rhs[i] for i in range(len(target)))) == 0
    for j in range(q.cols):
        q[-1, j] = invariant[j]
    rhs[-1] = 0
    return list(q.inv() * rhs)


def baseline(n):
    weights = complete_weights(n)
    full = (1 << n) - 1
    lb = dual_generator(weights, R, "Bd")
    ld = dual_generator(weights, R, "dB")
    pb = stationary(lb)
    pd = stationary(ld)
    mb = sp.cancel(sum(pb[a - 1] * a.bit_count() for a in range(1, full + 1)))
    md = sp.cancel(sum(pd[a - 1] * a.bit_count() for a in range(1, full + 1)))
    fb = poisson(lb, pb, [sp.Rational(a.bit_count(), 1) - mb for a in range(1, full + 1)])
    # The full state is transient for dB.  Restrict to the recurrent proper
    # states when solving the Poisson equation.
    proper = list(range(1, full))
    ld0 = ld.extract([a - 1 for a in proper], [a - 1 for a in proper])
    pd0 = pd[:-1]
    fd0 = poisson(ld0, pd0, [sp.Rational(a.bit_count(), 1) - md for a in proper])
    return mb, md, fb, fd0


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
        w = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.72:
                    w[i][j] = w[j][i] = rng.choice((1, 1, 2, 5, 17))
        if connected(w):
            return tuple(map(tuple, w))


def feasibility(weights, base):
    n = len(weights)
    full = (1 << n) - 1
    mb, md, fb, fd = base
    lb = np.array(dual_generator(weights, R, "Bd"), dtype=float)
    dd_full = np.array(dual_generator(weights, R, "dB"), dtype=float)
    proper = list(range(1, full))
    dd = dd_full[: full - 1, : full - 1]
    a_states = list(range(1, full + 1))
    b_states = proper

    fbv = np.array([float(value / mb) for value in fb])
    fdv = np.array([float(value / md) for value in fd])
    base_b_drift = lb @ fbv
    base_d_drift = dd @ fdv

    rows = []
    rhs = []
    for ai, a in enumerate(a_states):
        xa = np.array([(a >> i) & 1 for i in range(n)], dtype=float)
        lxa = np.array(
            [sum(lb[ai, aj] * ((aa >> i) & 1) for aj, aa in enumerate(a_states)) for i in range(n)]
        )
        for bi, b in enumerate(b_states):
            yb = np.array([(b >> j) & 1 for j in range(n)], dtype=float)
            dyb = np.array(
                [sum(dd[bi, bj] * ((bb >> j) & 1) for bj, bb in enumerate(b_states)) for j in range(n)]
            )
            # Q[x_i y_j]=(Lx_i)y_j+x_i(Dy_j).
            correction_drift = np.outer(lxa, yb) + np.outer(xa, dyb)
            target = a.bit_count() / float(mb) + b.bit_count() / float(md) - 2
            defect = base_b_drift[ai] + base_d_drift[bi] - target
            rows.append(-correction_drift.ravel())
            rhs.append(defect)
    result = linprog(
        np.zeros(n * n),
        A_ub=np.array(rows),
        b_ub=np.array(rhs),
        bounds=[(None, None)] * (n * n),
        method="highs",
    )
    return result


def main():
    rng = random.Random(20260802)
    for n in (3, 4, 5):
        base = baseline(n)
        trials = 40 if n < 5 else 8
        for trial in range(trials):
            weights = random_graph(n, rng)
            result = feasibility(weights, base)
            if not result.success:
                print("INFEASIBLE", n, trial, result.message)
                print("weights =", weights)
                break
        else:
            print("all feasible", n, trials)


if __name__ == "__main__":
    main()
