#!/usr/bin/env python3
"""Rare-mutant colony search for finite gadgets overlaid on complete support.

Take M copies of a labelled k-vertex gadget and put weight one on every edge
between different copies.  Inside a copy, edge ij has additional leading
weight n Z_ij (the background unit weight is lower order).  Sending M to
infinity with fixed k yields the exact finite-state colony branching process
built below.  Local mutant collisions are retained exactly.

This is numerical discovery code.  A positive branching score would still
need a finite-population coupling and post-establishment proof.
"""

from __future__ import annotations

import argparse

import numpy as np


def local_rates(mask, Z, r, rule):
    k = len(Z); z = Z.sum(axis=1); inv = 1.0 / (1.0 + z)
    A = float(inv.mean()); result = {}
    mutants = [(mask >> i) & 1 for i in range(k)]
    if rule == "Bd":
        for v in range(k):
            if not mutants[v]:
                rate = sum(r * Z[u, v] * inv[u] for u in range(k) if mutants[u])
                if rate: result[mask | (1 << v)] = rate
            else:
                rate = A + sum(Z[u, v] * inv[u] for u in range(k) if not mutants[u])
                if rate: result[mask & ~(1 << v)] = rate
        external = sum(r * inv[u] for u in range(k) if mutants[u])
    elif rule == "dB":
        for v in range(k):
            mutant_mass = sum(Z[u, v] for u in range(k) if mutants[u] and u != v)
            resident_mass = 1.0 + sum(Z[u, v] for u in range(k) if not mutants[u] and u != v)
            denom = r * mutant_mass + resident_mass
            if not mutants[v] and mutant_mass:
                result[mask | (1 << v)] = r * mutant_mass / denom
            elif mutants[v] and resident_mass:
                result[mask & ~(1 << v)] = resident_mass / denom
        external = bin(mask).count("1") * r * A
    else:
        raise ValueError(rule)
    return result, external


def extinction(Z, r, rule, tolerance=3e-13):
    Z = np.asarray(Z, dtype=float); k = len(Z); full = (1 << k) - 1
    states = list(range(1, full + 1)); index = {mask: i for i, mask in enumerate(states)}
    z = Z.sum(axis=1); inv = 1.0 / (1.0 + z); A = float(inv.mean())
    child = np.ones(k) / k if rule == "Bd" else inv / inv.sum()
    Q = 0.0
    for _ in range(100000):
        matrix = np.zeros((len(states), len(states))); rhs = np.zeros(len(states))
        for mask in states:
            row = index[mask]; rates, external = local_rates(mask, Z, r, rule)
            matrix[row, row] = sum(rates.values()) + external * (1.0 - Q)
            for target, rate in rates.items():
                if target == 0: rhs[row] += rate
                else: matrix[row, index[target]] -= rate
        q = np.linalg.solve(matrix, rhs)
        qsingle = np.array([q[index[1 << i]] for i in range(k)])
        new = float(child @ qsingle)
        if abs(new - Q) < tolerance:
            Q = new; break
        Q = new
    else:
        raise RuntimeError("colony fixed point did not converge")
    residual = np.max(np.abs(matrix @ q - rhs))
    if residual > 1e-8: raise AssertionError(residual)
    return qsingle, Q, A


def evaluate(Z, r):
    qb, _, _ = extinction(Z, r, "Bd")
    qd, _, _ = extinction(Z, r, "dB")
    p = 1.0 - 1.0 / r
    return 1.0 - qb.mean() - p, 1.0 - qd.mean() - p


def make_Z(k, logs):
    Z = np.zeros((k, k)); z = np.exp(logs); cursor = 0
    for i in range(k):
        for j in range(i + 1, k):
            Z[i, j] = Z[j, i] = z[cursor]; cursor += 1
    return Z


def search(k, r, samples, seed, lower, upper):
    rng = np.random.default_rng(seed); edges = k * (k - 1) // 2; rows = []
    for _ in range(samples):
        logs = rng.uniform(np.log(lower), np.log(upper), edges)
        Z = make_Z(k, logs)
        gb, gd = evaluate(Z, r)
        rows.append((min(gb, gd), gb, gd, *np.exp(logs)))
    rows.sort(reverse=True)
    return rows[:20]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--r", type=float, default=1.51)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--lower", type=float, default=1e-5)
    parser.add_argument("--upper", type=float, default=10.0)
    args = parser.parse_args()
    for row in search(args.k, args.r, args.samples, args.seed, args.lower, args.upper):
        print(" ".join(f"{x:.12g}" for x in row))


if __name__ == "__main__":
    main()
