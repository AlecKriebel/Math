#!/usr/bin/env python3
"""Fast discovery search for higher-rank incidence without portal edges.

This is numerical discovery code, not a proof.  Rows of ``frac`` are the
fractions of each portal's total blade load supplied by each blade type.
In these coordinates the multitype extinction vector is independent of the
limiting type proportions.  The latter are optimized exactly over the
simplex after each fixed-point solve (an optimum uses at most two types).
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import differential_evolution


def softmax_rows(x: np.ndarray) -> np.ndarray:
    x = x - x.max(axis=1, keepdims=True)
    y = np.exp(x)
    return y / y.sum(axis=1, keepdims=True)


def decode(v: np.ndarray, q: int, t: int):
    loads = np.exp(np.asarray(v[:q]))
    logits = np.asarray(v[q:]).reshape(q, t - 1)
    frac = softmax_rows(np.c_[logits, np.zeros(q)])
    return loads, frac


def offspring(rule: str, r: float, loads: np.ndarray, frac: np.ndarray, z: np.ndarray):
    """Evaluate the no-portal-edge multitype offspring PGF."""
    if rule == "Bd":
        marks = frac @ (1.0 - z)
        episode = loads / (loads + r**2 / (r + 1.0) * marks)
        col_count = frac.sum(axis=0)
        killed = (loads[:, None] * frac * (1.0 - episode[:, None])).sum(axis=0)
        return col_count / (col_count + r * (r + 1.0) * killed)
    if rule == "dB":
        marks = frac @ (1.0 - z)
        episode = 1.0 / (1.0 + r * loads * marks / 2.0)
        col_load = (loads[:, None] * frac).sum(axis=0)
        killed = (frac * (1.0 - episode[:, None])).sum(axis=0)
        return col_load / (col_load + 2.0 * r**2 * killed)
    raise ValueError(rule)


def extinction(rule: str, r: float, loads: np.ndarray, frac: np.ndarray):
    z = np.zeros(frac.shape[1])
    for _ in range(200000):
        new = offspring(rule, r, loads, frac, z)
        if np.max(np.abs(new - z)) < 2e-13:
            return new
        z = new
    raise RuntimeError("fixed point did not converge")


def best_type_mixture(r: float, qb: np.ndarray, qd: np.ndarray):
    """Maximize the smaller Bd/dB gap over all type proportions."""
    p = 1.0 - 1.0 / r
    ab = r / (r + 1.0)

    def gaps(w):
        return ab * (1.0 - float(w @ qb)) - p, 0.5 * (1.0 - float(w @ qd)) - p

    best = (-np.inf, None, None)
    t = len(qb)
    for i in range(t):
        w = np.zeros(t); w[i] = 1.0
        gb, gd = gaps(w)
        candidate = (min(gb, gd), w, (gb, gd))
        if candidate[0] > best[0]:
            best = candidate
    # On an edge, the lower envelope of two affine functions is maximized
    # at an endpoint or at their intersection.
    cb = ab * (1.0 - qb) - p
    cd = 0.5 * (1.0 - qd) - p
    for i in range(t):
        for j in range(i + 1, t):
            denominator = (cb[i] - cb[j]) - (cd[i] - cd[j])
            if abs(denominator) < 1e-15:
                continue
            x = (cd[j] - cb[j]) / denominator
            if 0.0 < x < 1.0:
                w = np.zeros(t); w[i], w[j] = x, 1.0 - x
                gb, gd = gaps(w)
                candidate = (min(gb, gd), w, (gb, gd))
                if candidate[0] > best[0]:
                    best = candidate
    return best


def objective(v, q, t, fitnesses):
    try:
        loads, frac = decode(v, q, t)
        # A common type mixture must work at every requested fitness.
        # For one fitness use the exact two-type simplex optimization; for
        # several, retain a conservative uniform mixture during discovery.
        if len(fitnesses) == 1:
            r = fitnesses[0]
            qb = extinction("Bd", r, loads, frac)
            qd = extinction("dB", r, loads, frac)
            return -best_type_mixture(r, qb, qd)[0]
        pi = np.ones(t) / t
        gaps = []
        for r in fitnesses:
            p = 1.0 - 1.0 / r
            qb = extinction("Bd", r, loads, frac)
            qd = extinction("dB", r, loads, frac)
            gaps.extend([
                r / (r + 1.0) * (1.0 - float(pi @ qb)) - p,
                0.5 * (1.0 - float(pi @ qd)) - p,
            ])
        return -min(gaps)
    except (FloatingPointError, RuntimeError):
        return 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portals", type=int, default=4)
    ap.add_argument("--types", type=int, default=4)
    ap.add_argument("--fitness", type=float, nargs="+", default=[1.6])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=500)
    ap.add_argument("--popsize", type=int, default=20)
    args = ap.parse_args()
    q, t = args.portals, args.types
    result = differential_evolution(
        objective,
        [(-10.0, 10.0)] * (q + q * (t - 1)),
        args=(q, t, args.fitness),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        polish=True,
        workers=1,
        updating="immediate",
        tol=1e-10,
    )
    loads, frac = decode(result.x, q, t)
    print("objective min gap", -result.fun)
    print("loads", loads)
    print("load fractions\n", frac)
    for r in args.fitness:
        qb = extinction("Bd", r, loads, frac)
        qd = extinction("dB", r, loads, frac)
        score, pi, gaps = best_type_mixture(r, qb, qd)
        print("r", r, "score", score, "pi", pi, "gaps", gaps)
        print("q_B", qb)
        print("q_D", qd)


if __name__ == "__main__":
    main()
