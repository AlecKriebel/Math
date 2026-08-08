#!/usr/bin/env python3
"""Floating hostile screen for the marked stationary-promotion conjecture.

Discovery only.  The exact verifier remains verify_marked_lift.py.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
from scipy.sparse import csr_matrix


def marked_sparse(P):
    n = len(P)
    states = [(C, v) for v in range(n) for C in range(1 << n) if not C >> v & 1]
    index = {state: i for i, state in enumerate(states)}
    rows, cols, data = [], [], []
    for source, (C, v) in enumerate(states):
        for i, probability in enumerate(P[v]):
            if probability == 0:
                continue
            B = C | 1 << i
            rows.append(source)
            cols.append(index[B, v])
            data.append(probability / 2)
            b = B.bit_count()
            for w in range(n):
                if B >> w & 1:
                    rows.append(source)
                    cols.append(index[B & ~(1 << w), w])
                    data.append(probability / (2 * b))
    return states, csr_matrix((data, (rows, cols)), shape=(len(states), len(states)))


def psi_values(states, n):
    N = n - 1
    by_rank = np.zeros(n)
    for j in range(N):
        by_rank[j] = 2 * sum((-1) ** (k - 1 - j) / k for k in range(j + 1, N + 1))
    return np.array([by_rank[C.bit_count()] for C, _ in states])


def trial(P, steps=400, zgrid=None):
    if zgrid is None:
        zgrid = np.linspace(0, 1, 41)
    n = len(P)
    states, M = marked_sparse(P)
    law = np.full(len(states), 1 / len(states))
    psi = psi_values(states, n)
    laws = [law]
    for _ in range(steps):
        law = law @ M
        laws.append(law)
    a = np.array([x @ psi for x in laws])
    psi_gap = a[-1] - a[2]
    min_psi_gap = np.min(a[2:] - a[2])

    pgf_gap = np.inf
    pgf_arg = None
    ranks = np.array([C.bit_count() for C, _ in states])
    for z in zgrid:
        f = z ** ranks
        base = laws[2] @ f
        values = np.array([x @ f for x in laws[2:]])
        here = np.min(values - base)
        if here < pgf_gap:
            pgf_gap = here
            pgf_arg = (z, 2 + int(np.argmin(values - base)))
    return psi_gap, min_psi_gap, pgf_gap, pgf_arg, a


def random_reversible(n, rng):
    weights = np.zeros((n, n))
    for i, j in combinations(range(n), 2):
        weights[i, j] = weights[j, i] = 10 ** rng.uniform(-5, 5)
    return weights / weights.sum(axis=1, keepdims=True)


def random_directed(n, rng):
    raw = 10 ** rng.uniform(-5, 5, size=(n, n))
    np.fill_diagonal(raw, 0)
    return raw / raw.sum(axis=1, keepdims=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--seed", type=int, default=81917)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    best_psi = (np.inf, None)
    best_path = (np.inf, None)
    best_pgf = (np.inf, None)
    for trial_index in range(args.trials):
        P = random_directed(args.n, rng) if args.directed else random_reversible(args.n, rng)
        psi_gap, min_path, pgf_gap, pgf_arg, sequence = trial(P)
        if psi_gap < best_psi[0]:
            best_psi = (psi_gap, (trial_index, P, sequence))
        if min_path < best_path[0]:
            best_path = (min_path, (trial_index, P, sequence))
        if pgf_gap < best_pgf[0]:
            best_pgf = (pgf_gap, (trial_index, pgf_arg, P))
    print("stationary psi gap", best_psi[0], "trial", best_psi[1][0])
    print("minimum path psi gap", best_path[0], "trial", best_path[1][0])
    print("minimum PGF path gap", best_pgf[0], "at", best_pgf[1][1])
    if best_pgf[0] < -1e-10:
        print("PGF witness P=", repr(best_pgf[1][2].tolist()))


if __name__ == "__main__":
    main()
