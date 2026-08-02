#!/usr/bin/env python3
"""Search the exact limiting multitype strong-pair trace.

This is a discovery program, not a proof.  It retains every portal subset
and solves the corresponding finite phase-type equations exactly up to
floating-point linear algebra.
"""

from __future__ import annotations

import argparse
import itertools
import math

import numpy as np
from scipy.optimize import differential_evolution


def portal_transform(rule, r, pi, lam, h, z):
    """Return F_a(z), episode PGFs begun from the singleton portal a."""
    q, t = lam.shape
    bload = 2.0 * (lam * pi[None, :]).sum(axis=1)
    deg = bload + h.sum(axis=1)
    masks = list(range(1, 1 << q))
    row = {mask: j for j, mask in enumerate(masks)}
    mat = np.zeros((len(masks), len(masks)))
    rhs = np.zeros(len(masks))

    for mask in masks:
        j = row[mask]
        active = [a for a in range(q) if mask >> a & 1]
        inactive = [a for a in range(q) if not (mask >> a & 1)]
        transitions = []
        if rule == "Bd":
            for a in active:
                rate = bload[a] + sum(h[a, b] / deg[b] for b in inactive)
                transitions.append((mask ^ (1 << a), rate))
            for b in inactive:
                rate = r * sum(h[a, b] / deg[a] for a in active)
                transitions.append((mask | (1 << b), rate))
            child = (
                2.0
                * pi
                * r**2
                / (r + 1.0)
                * sum((lam[a] / deg[a] for a in active), start=np.zeros(t))
            )
        elif rule == "dB":
            for a in active:
                resident_portal = sum(h[a, b] for b in inactive)
                mutant_portal = sum(h[a, b] for b in active if b != a)
                rate = (bload[a] + resident_portal) / (
                    bload[a] + resident_portal + r * mutant_portal
                )
                transitions.append((mask ^ (1 << a), rate))
            for b in inactive:
                mutant_portal = sum(h[a, b] for a in active)
                resident_portal = sum(
                    h[b, c] for c in inactive if c != b
                )
                rate = r * mutant_portal / (
                    bload[b] + resident_portal + r * mutant_portal
                )
                transitions.append((mask | (1 << b), rate))
            child = pi * r * sum((lam[a] for a in active), start=np.zeros(t))
        else:
            raise ValueError(rule)

        killing = float(child @ (1.0 - z))
        mat[j, j] = sum(rate for _, rate in transitions) + killing
        for nxt, rate in transitions:
            if nxt == 0:
                rhs[j] += rate
            else:
                mat[j, row[nxt]] -= rate

    sol = np.linalg.solve(mat, rhs)
    return np.array([sol[row[1 << a]] for a in range(q)])


def extinction(rule, r, pi, lam, h, tol=2e-13, max_iter=100000):
    q, t = lam.shape
    bload = 2.0 * (lam * pi[None, :]).sum(axis=1)
    deg = bload + h.sum(axis=1)
    if rule == "Bd":
        death = 2.0 / (r + 1.0) * (lam / deg[:, None]).sum(axis=0)
        seed = 2.0 * r * lam
    else:
        death = lam.sum(axis=0) / r
        seed = 2.0 * r * lam / deg[:, None]

    z = np.zeros(t)
    for _ in range(max_iter):
        f = portal_transform(rule, r, pi, lam, h, z)
        killed = (seed * (1.0 - f[:, None])).sum(axis=0)
        new = death / (death + killed)
        if np.max(np.abs(new - z)) < tol:
            return new
        z = new
    raise RuntimeError("fixed-point iteration did not converge")


def establishment(rule, r, pi, lam, h):
    q = extinction(rule, r, pi, lam, h)
    entrance = r / (r + 1.0) if rule == "Bd" else 0.5
    return entrance * float(pi @ (1.0 - q)), q


def decode(v, q, t):
    k = q * t
    lam = np.exp(np.asarray(v[:k])).reshape(q, t)
    e = q * (q - 1) // 2
    h = np.zeros((q, q))
    for value, (a, b) in zip(np.exp(np.asarray(v[k : k + e])), itertools.combinations(range(q), 2)):
        h[a, b] = h[b, a] = value
    logits = np.r_[np.asarray(v[k + e :]), 0.0]
    logits -= logits.max()
    pi = np.exp(logits)
    pi /= pi.sum()
    return pi, lam, h


def score(v, q, t, fitnesses):
    try:
        pi, lam, h = decode(v, q, t)
        gaps = []
        for r in fitnesses:
            p = 1.0 - 1.0 / r
            for rule in ("Bd", "dB"):
                alpha, _ = establishment(rule, r, pi, lam, h)
                gaps.append(alpha - p)
        ans = min(gaps)
        if not np.isfinite(ans):
            return 1e6
        return -ans
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
    dim = q * t + q * (q - 1) // 2 + t - 1
    result = differential_evolution(
        score,
        [(-5.0, 5.0)] * dim,
        args=(q, t, args.fitness),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        polish=True,
        workers=1,
        updating="immediate",
        tol=1e-9,
    )
    pi, lam, h = decode(result.x, q, t)
    print("objective min gap", -result.fun)
    print("pi", pi)
    print("lambda\n", lam)
    print("h\n", h)
    for r in args.fitness:
        p = 1.0 - 1.0 / r
        for rule in ("Bd", "dB"):
            alpha, ext = establishment(rule, r, pi, lam, h)
            print(r, rule, "alpha", alpha, "gap", alpha - p, "q", ext)


if __name__ == "__main__":
    main()
