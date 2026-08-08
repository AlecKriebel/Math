#!/usr/bin/env python3
"""Discovery search for the growing two-portal-class boundary trace.

Each portal class has ``q`` vertices.  Within-class portal edge weights are
``H_gg/(q-1)`` and cross-class weights are ``H_01/q``.  As ``q`` grows, a
finite portal episode converges to a two-type continuous-time branching
process.  This file numerically solves that nested portal/blade branching
trace.  It is not a proof of convergence or of any sign claim.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, root


HERE = Path(__file__).resolve().parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fast = load_module("fast_no_portal", HERE / "search_higher_rank_no_portal.py")


def portal_transform(rule, r, loads, frac, totals, z):
    """Minimal marked-child transform of the limiting portal BP."""
    h00, h11, h01 = totals
    h = np.array([[h00, h01], [h01, h11]])
    degree = loads + h.sum(axis=1)
    pi0 = np.ones(frac.shape[1]) / frac.shape[1]
    lam = loads[:, None] * frac / (2.0 * pi0[None, :])
    if rule == "Bd":
        death = np.array([
            loads[g] + sum(h[g, j] / degree[j] for j in range(2))
            for g in range(2)
        ])
        birth = r * h / degree[:, None]
        child = 2.0 * pi0[None, :] * r**2 / (r + 1.0) * lam / degree[:, None]
    elif rule == "dB":
        death = np.ones(2)
        birth = r * h / degree[None, :]
        child = pi0[None, :] * r * lam
    else:
        raise ValueError(rule)
    killing = child @ (1.0 - z)
    def mapping(value):
        return death / (death + birth @ (1.0 - value) + killing)

    # Positive marking makes the killed portal transform the subunit root.
    # A few monotone steps select its basin before the local root solve.
    value = np.zeros(2)
    for _ in range(12):
        value = mapping(value)
    answer = root(lambda x: mapping(x) - x, value, method="hybr")
    if (
        not answer.success
        or np.max(np.abs(mapping(answer.x) - answer.x)) > 2e-9
        or np.min(answer.x) < -1e-9
        or np.max(answer.x) > 1.0 + 1e-9
    ):
        raise RuntimeError("portal transform did not converge")
    return np.clip(answer.x, 0.0, 1.0)


def extinction(rule, r, loads, frac, totals):
    t = frac.shape[1]
    pi0 = np.ones(t) / t
    lam = loads[:, None] * frac / (2.0 * pi0[None, :])
    h00, h11, h01 = totals
    h = np.array([[h00, h01], [h01, h11]])
    degree = loads + h.sum(axis=1)
    if rule == "Bd":
        death = 2.0 / (r + 1.0) * (lam / degree[:, None]).sum(axis=0)
        seed = 2.0 * r * lam
        portal_death = np.array([
            loads[g] + sum(h[g, j] / degree[j] for j in range(2))
            for g in range(2)
        ])
        portal_birth = r * h / degree[:, None]
        portal_child = (
            2.0 * pi0[None, :] * r**2 / (r + 1.0)
            * lam / degree[:, None]
        )
    else:
        death = lam.sum(axis=0) / r
        seed = 2.0 * r * lam / degree[:, None]
        portal_death = np.ones(2)
        portal_birth = r * h / degree[None, :]
        portal_child = pi0[None, :] * r * lam

    def mapping(value):
        z, f = value[:t], value[t:]
        killed = (seed * (1.0 - f[:, None])).sum(axis=0)
        next_z = death / (death + killed)
        killing = portal_child @ (1.0 - z)
        next_f = portal_death / (
            portal_death + portal_birth @ (1.0 - f) + killing
        )
        return np.r_[next_z, next_f]

    value = np.zeros(t + 2)
    for _ in range(30):
        value = mapping(value)
    candidates = []
    for start in (value, np.zeros(t + 2), np.full(t + 2, 0.5)):
        answer = root(lambda x: mapping(x) - x, start, method="hybr")
        if (
            answer.success
            and np.max(np.abs(mapping(answer.x) - answer.x)) < 2e-8
            and np.min(answer.x) >= -1e-8
            and np.max(answer.x) <= 1.0 + 1e-8
        ):
            candidates.append(np.clip(answer.x, 0.0, 1.0))
    if not candidates:
        raise RuntimeError("blade fixed point did not converge")
    # Extinction is the componentwise-minimal fixed point.  For an
    # irreducible two-type trace the valid roots are ordered; retain the
    # smallest sum and verify it is no larger than every other candidate.
    answer = min(candidates, key=lambda x: float(x.sum()))
    if any(np.any(answer > other + 2e-7) for other in candidates):
        raise RuntimeError("unordered blade roots")
    return answer[:t]


def decode(v):
    loads = np.exp(np.asarray(v[:2]))
    p = 1.0 / (1.0 + np.exp(-np.asarray(v[2:4])))
    frac = np.c_[p, 1.0 - p]
    totals = np.exp(np.asarray(v[4:7]))
    return loads, frac, totals


def objective(v, r):
    try:
        loads, frac, totals = decode(v)
        qb = extinction("Bd", r, loads, frac, totals)
        qd = extinction("dB", r, loads, frac, totals)
        return -fast.best_type_mixture(r, qb, qd)[0]
    except (FloatingPointError, RuntimeError, np.linalg.LinAlgError, ValueError):
        return 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fitness", type=float, default=1.6)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=500)
    ap.add_argument("--popsize", type=int, default=20)
    args = ap.parse_args()
    result = differential_evolution(
        objective,
        [(-12.0, 12.0)] * 7,
        args=(args.fitness,),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        polish=True,
        tol=1e-11,
        workers=1,
        updating="immediate",
    )
    loads, frac, totals = decode(result.x)
    qb = extinction("Bd", args.fitness, loads, frac, totals)
    qd = extinction("dB", args.fitness, loads, frac, totals)
    score, pi, gaps = fast.best_type_mixture(args.fitness, qb, qd)
    print("objective min gap", -result.fun)
    print("loads", loads)
    print("fractions\n", frac)
    print("within0, within1, cross totals", totals)
    print("optimal type mixture", pi, "gaps", gaps, "score", score)
    print("q_B", qb, "q_D", qd)


if __name__ == "__main__":
    main()
