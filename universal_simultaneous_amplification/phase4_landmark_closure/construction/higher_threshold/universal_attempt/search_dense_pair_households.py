#!/usr/bin/env python3
"""Discovery search for dense complete support with weighted partner edges.

There are many disjoint pairs.  A type-k pair has partner edge weight z_k n;
all other edges have weight one.  Pair-type vertex proportions are pi_k.
In the rare-mutant n->infinity limit, different occupied pairs form an exact
colony branching process, while states 1 and 2 within a pair retain collision
effects.  The equations below are direct first-event equations.

This script is numerical reconnaissance, not a finite-population proof.
"""

from __future__ import annotations

import argparse

import numpy as np


def extinction(pi, z, r, rule, tolerance=2e-14):
    pi = np.asarray(pi, dtype=float)
    z = np.asarray(z, dtype=float)
    pi = pi / pi.sum()
    inv = 1.0 / (1.0 + z)
    A = float(pi @ inv)
    if rule == "Bd":
        child_weight = pi
    elif rule == "dB":
        child_weight = pi * inv / A
    else:
        raise ValueError(rule)

    Q = 0.0
    for _ in range(1000000):
        if rule == "Bd":
            h = z / (1.0 + z)
            e = A + h
            g = r * h
            b = r * (1.0 - h)
            d = np.full_like(z, 2.0 * A)
            b2 = 2.0 * b
        else:
            e = np.ones_like(z)
            g = r * z / (1.0 + r * z)
            b = np.full_like(z, r * A)
            d = 2.0 / (1.0 + r * z)
            b2 = np.full_like(z, 2.0 * r * A)
        q2_over_q1 = d / (d + b2 * (1.0 - Q))
        q1 = e / (e + g + b * (1.0 - Q) - g * q2_over_q1)
        q2 = q2_over_q1 * q1
        new = float(child_weight @ q1)
        if abs(new - Q) < tolerance:
            Q = new
            break
        Q = new
    else:
        raise RuntimeError("fixed point did not converge")
    # Uniform initial vertex selects pair type with probabilities pi.
    return float(pi @ q1), q1, q2, A, Q


def evaluate(pi, z, r):
    qb, b1, b2, A, QB = extinction(pi, z, r, "Bd")
    qd, d1, d2, _, QD = extinction(pi, z, r, "dB")
    p = 1.0 - 1.0 / r
    return 1.0 - qb - p, 1.0 - qd - p, b1, d1, A, QB, QD


def search(r, types, samples, seed, zmax):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(samples):
        pi = rng.dirichlet(np.ones(types))
        # Include zero-scale boundary layers and broad strong partners.
        z = np.exp(rng.uniform(np.log(1e-8), np.log(zmax), types))
        gb, gd, *_ = evaluate(pi, z, r)
        rows.append((min(gb, gd), gb, gd, *pi, *z))
    rows.sort(reverse=True)
    return rows[:30]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--r", type=float, default=1.51)
    parser.add_argument("--types", type=int, default=2)
    parser.add_argument("--samples", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--zmax", type=float, default=100.0)
    args = parser.parse_args()
    for row in search(args.r, args.types, args.samples, args.seed, args.zmax):
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
