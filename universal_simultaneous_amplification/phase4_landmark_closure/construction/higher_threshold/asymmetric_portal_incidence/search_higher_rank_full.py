#!/usr/bin/env python3
"""Search the full labelled higher-rank portal trace efficiently.

Numerical discovery only.  Portal loads and row-wise type fractions are
used in place of raw incidences.  The multitype extinction vectors then do
not depend on the blade-type proportions, whose optimal mixture is solved
exactly after each pair of fixed-point computations.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


trace = load_module("asym_trace", HERE / "search_asymmetric_trace.py")
fast = load_module("fast_no_portal", HERE / "search_higher_rank_no_portal.py")


def softmax_rows(x):
    x = x - x.max(axis=1, keepdims=True)
    y = np.exp(x)
    return y / y.sum(axis=1, keepdims=True)


def decode(v, q, t):
    j = 0
    loads = np.exp(np.asarray(v[j : j + q])); j += q
    h = np.zeros((q, q))
    for value, (a, b) in zip(
        np.exp(np.asarray(v[j : j + q * (q - 1) // 2])),
        itertools.combinations(range(q), 2),
    ):
        h[a, b] = h[b, a] = value
    j += q * (q - 1) // 2
    logits = np.asarray(v[j:]).reshape(q, t - 1)
    frac = softmax_rows(np.c_[logits, np.zeros(q)])
    # Any positive type mixture gives the same extinction law in these
    # coordinates.  Uniform proportions are numerically best conditioned.
    pi = np.ones(t) / t
    lam = loads[:, None] * frac / (2.0 * pi[None, :])
    return loads, frac, pi, lam, h


def objective(v, q, t, r):
    try:
        _, _, pi, lam, h = decode(v, q, t)
        qb = trace.extinction("Bd", r, pi, lam, h)
        qd = trace.extinction("dB", r, pi, lam, h)
        return -fast.best_type_mixture(r, qb, qd)[0]
    except (FloatingPointError, RuntimeError, np.linalg.LinAlgError):
        return 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portals", type=int, default=3)
    ap.add_argument("--types", type=int, default=3)
    ap.add_argument("--fitness", type=float, default=1.6)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=500)
    ap.add_argument("--popsize", type=int, default=20)
    args = ap.parse_args()
    q, t, r = args.portals, args.types, args.fitness
    dim = q + q * (q - 1) // 2 + q * (t - 1)
    result = differential_evolution(
        objective,
        [(-10.0, 10.0)] * dim,
        args=(q, t, r),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        polish=True,
        workers=1,
        updating="immediate",
        tol=1e-10,
    )
    loads, frac, pi0, lam, h = decode(result.x, q, t)
    qb = trace.extinction("Bd", r, pi0, lam, h)
    qd = trace.extinction("dB", r, pi0, lam, h)
    score, pi, gaps = fast.best_type_mixture(r, qb, qd)
    print("objective min gap", -result.fun)
    print("loads", loads)
    print("load fractions\n", frac)
    print("portal weights\n", h)
    print("optimal type mixture", pi)
    print("gaps", gaps, "score", score)
    print("q_B", qb)
    print("q_D", qd)


if __name__ == "__main__":
    main()
