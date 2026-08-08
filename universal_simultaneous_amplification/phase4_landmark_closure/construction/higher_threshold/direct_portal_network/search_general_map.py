#!/usr/bin/env python3
"""Relaxed hostile search for the direct-portal affine survival-map gap.

The row marks and the weights of the prospective parent type are optimized
directly.  This is a relaxation of a finite blade-type incidence model and
therefore a useful counterexample screen, not a proof.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution


def episode_survival(rule, r, loads, portal, marks):
    q = len(loads)
    degrees = loads + portal.sum(axis=1)
    masks = list(range(1, 1 << q))
    row = {mask: j for j, mask in enumerate(masks)}
    matrix = np.zeros((len(masks), len(masks)))
    rhs = np.zeros(len(masks))
    for mask in masks:
        active = [a for a in range(q) if mask >> a & 1]
        inactive = [a for a in range(q) if not mask >> a & 1]
        transitions = []
        if rule == "Bd":
            for a in active:
                rate = loads[a] + sum(portal[a, b] / degrees[b]
                                      for b in inactive)
                transitions.append((mask ^ (1 << a), rate))
            for b in inactive:
                rate = r * sum(portal[a, b] / degrees[a] for a in active)
                transitions.append((mask | (1 << b), rate))
            killing = r * r / (r + 1.0) * sum(
                loads[a] * marks[a] / degrees[a] for a in active
            )
        elif rule == "dB":
            for a in active:
                resident = loads[a] + sum(portal[a, b] for b in inactive)
                mutant = sum(portal[a, b] for b in active if b != a)
                transitions.append(
                    (mask ^ (1 << a), resident / (resident + r * mutant))
                )
            for b in inactive:
                mutant = sum(portal[a, b] for a in active)
                resident = loads[b] + sum(
                    portal[b, c] for c in inactive if c != b
                )
                transitions.append(
                    (mask | (1 << b), r * mutant / (resident + r * mutant))
                )
            killing = r / 2.0 * sum(loads[a] * marks[a] for a in active)
        else:
            raise ValueError(rule)
        j = row[mask]
        matrix[j, j] = sum(rate for _, rate in transitions) + killing
        rhs[j] = killing
        for nxt, rate in transitions:
            if nxt:
                matrix[j, row[nxt]] -= rate
    solution = np.linalg.solve(matrix, rhs)
    return np.array([solution[row[1 << a]] for a in range(q)])


def decode(v, q):
    j = 0
    loads = np.exp(np.asarray(v[j:j + q])); j += q
    portal = np.zeros((q, q))
    for value, (a, b) in zip(
        np.exp(np.asarray(v[j:j + q * (q - 1) // 2])),
        itertools.combinations(range(q), 2),
    ):
        portal[a, b] = portal[b, a] = value
    j += q * (q - 1) // 2
    marks = 1.0 / (1.0 + np.exp(-np.asarray(v[j:j + q]))); j += q
    logits = np.asarray(v[j:j + q]); logits -= logits.max()
    parent = np.exp(logits); parent /= parent.sum()
    return loads, portal, marks, parent


def affine_margin(v, q, r):
    loads, portal, marks, parent = decode(v, q)
    degrees = loads + portal.sum(axis=1)
    hb = episode_survival("Bd", r, loads, portal, marks)
    aa = 4.0 * (r - 1.0) / r
    kk = 2.0 * r / (r + 1.0)
    dual_marks = np.minimum(1.0, aa - kk * marks)
    hd = episode_survival("dB", r, loads, portal, dual_marks)
    # parent is a_a=B_a f_at/d_a, normalized.
    xodds = r * (r + 1.0) * np.dot(parent, degrees * hb)
    x = xodds / (1.0 + xodds)
    y = min(1.0, aa - kk * x)
    if y >= 1.0:
        return 1.0
    yodds = y / (1.0 - y)
    return yodds * np.dot(parent, degrees) - 2.0 * r * r * np.dot(parent, hd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portals", type=int, default=3)
    ap.add_argument("--fitness", type=float, default=31 / 20)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=800)
    ap.add_argument("--popsize", type=int, default=18)
    args = ap.parse_args()
    q = args.portals
    dim = 3 * q + q * (q - 1) // 2
    result = differential_evolution(
        affine_margin,
        [(-14.0, 14.0)] * dim,
        args=(q, args.fitness),
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        tol=1e-10,
        polish=True,
        workers=1,
        updating="immediate",
    )
    loads, portal, marks, parent = decode(result.x, q)
    print("minimum relaxed affine-map margin", result.fun)
    print("loads", loads)
    print("portal\n", portal)
    print("marks", marks)
    print("parent weights a", parent)


if __name__ == "__main__":
    main()
