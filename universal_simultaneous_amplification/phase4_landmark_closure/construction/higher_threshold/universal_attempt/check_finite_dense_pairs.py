#!/usr/bin/env python3
"""Exact-double finite subset-chain check for complete graphs with pair edges.

Numerical discovery only.  All nonpartner edges have weight one; the edge of
pair k has the supplied positive weight.  The full 2^n chain is solved after
deleting self-loops.
"""

from __future__ import annotations

import itertools

import numpy as np


def baseline(n, r, rule):
    if rule == "Bd":
        return (1 - 1 / r) / (1 - r ** (-n))
    return (n - 1) / n * (1 - 1 / r) / (1 - r ** (-(n - 1)))


def graph(pair_weights):
    n = 2 * len(pair_weights)
    W = np.ones((n, n)) - np.eye(n)
    for k, weight in enumerate(pair_weights):
        W[2 * k, 2 * k + 1] = W[2 * k + 1, 2 * k] = weight
    return W


def fixation(W, r, rule):
    n = len(W); degree = W.sum(axis=1); full = (1 << n) - 1
    states = list(range(1, full)); index = {mask: k for k, mask in enumerate(states)}
    A = np.eye(len(states)); rhs = np.zeros(len(states))
    for mask in states:
        x = np.array([(mask >> i) & 1 for i in range(n)], dtype=int)
        changes = []
        if rule == "Bd":
            fit = 1 + (r - 1) * x; total = fit.sum()
            for u in range(n):
                for v in range(n):
                    if x[u] != x[v] and W[u, v]:
                        target = mask ^ (1 << v)
                        changes.append((target, fit[u] / total * W[u, v] / degree[u]))
        else:
            fit = 1 + (r - 1) * x
            for v in range(n):
                denom = float(W[v] @ fit)
                for u in range(n):
                    if x[u] != x[v] and W[u, v]:
                        target = mask ^ (1 << v)
                        changes.append((target, W[u, v] * fit[u] / (n * denom)))
        mass = sum(p for _, p in changes)
        row = index[mask]
        for target, probability in changes:
            probability /= mass
            if target == full:
                rhs[row] += probability
            elif target:
                A[row, index[target]] -= probability
    f = np.linalg.solve(A, rhs)
    return sum(f[index[1 << i]] for i in range(n)) / n


def main():
    rng = np.random.default_rng(4); r = 1.51
    for pairs in (2, 3, 4):
        best = [-1e9, None]
        simultaneous = 0
        for _ in range(200 if pairs < 4 else 30):
            weights = np.exp(rng.uniform(-4, 6, pairs))
            W = graph(weights)
            gaps = [fixation(W, r, rule) - baseline(2 * pairs, r, rule) for rule in ("Bd", "dB")]
            if min(gaps) > best[0]: best = [min(gaps), (weights, gaps)]
            simultaneous += min(gaps) > 1e-10
        print(pairs, best, simultaneous)


if __name__ == "__main__":
    main()
