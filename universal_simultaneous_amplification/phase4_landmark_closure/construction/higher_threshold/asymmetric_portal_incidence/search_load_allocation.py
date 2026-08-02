#!/usr/bin/env python3
"""Discovery search in aggregate portal-load coordinates.

For portal ``a`` let ``B[a]`` be its total blade weight, and let
``f[a,t]`` be the fraction of that load supplied by blade type ``t``.
Then ``lambda[a,t] = B[a] f[a,t] / (2 pi[t])``.  This removes the severe
scale degeneracy of a direct incidence-matrix parametrization.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "asym_trace", HERE / "search_asymmetric_trace.py"
)
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)


def softmax_rows(x):
    x = x - x.max(axis=1, keepdims=True)
    y = np.exp(x)
    return y / y.sum(axis=1, keepdims=True)


def decode(v, q, t):
    j = 0
    bload = np.exp(np.asarray(v[j : j + q])); j += q
    h = np.zeros((q, q))
    for value, (a, b) in zip(
        np.exp(np.asarray(v[j : j + q * (q - 1) // 2])),
        itertools.combinations(range(q), 2),
    ):
        h[a, b] = h[b, a] = value
    j += q * (q - 1) // 2
    logits = np.asarray(v[j : j + q * (t - 1)]).reshape(q, t - 1)
    j += q * (t - 1)
    frac = softmax_rows(np.c_[logits, np.zeros(q)])
    pilogit = np.r_[np.asarray(v[j : j + t - 1]), 0.0]
    pilogit -= pilogit.max()
    pi = np.exp(pilogit); pi /= pi.sum()
    lam = bload[:, None] * frac / (2.0 * pi[None, :])
    return bload, frac, pi, lam, h


def objective(v, q, t, fitnesses):
    try:
        _, _, pi, lam, h = decode(v, q, t)
        gaps = []
        for r in fitnesses:
            p = 1.0 - 1.0 / r
            for rule in ("Bd", "dB"):
                alpha, _ = trace.establishment(rule, r, pi, lam, h)
                gaps.append(alpha - p)
        ans = min(gaps)
        return -ans if np.isfinite(ans) else 1e6
    except (np.linalg.LinAlgError, RuntimeError, FloatingPointError):
        return 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portals", type=int, default=2)
    ap.add_argument("--types", type=int, default=2)
    ap.add_argument("--fitness", type=float, nargs="+", default=[1.6])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=500)
    ap.add_argument("--popsize", type=int, default=20)
    args = ap.parse_args()
    q, t = args.portals, args.types
    dim = q + q * (q - 1) // 2 + q * (t - 1) + t - 1
    res = differential_evolution(
        objective,
        [(-8.0, 8.0)] * dim,
        args=(q, t, args.fitness),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        tol=1e-9,
        polish=True,
        workers=1,
        updating="immediate",
    )
    bload, frac, pi, lam, h = decode(res.x, q, t)
    print("objective min gap", -res.fun)
    print("B", bload)
    print("load fractions\n", frac)
    print("pi", pi)
    print("lambda\n", lam)
    print("h\n", h)
    for r in args.fitness:
        p = 1.0 - 1.0 / r
        for rule in ("Bd", "dB"):
            alpha, ext = trace.establishment(rule, r, pi, lam, h)
            print(r, rule, "alpha", alpha, "gap", alpha - p, "q", ext)


if __name__ == "__main__":
    main()
