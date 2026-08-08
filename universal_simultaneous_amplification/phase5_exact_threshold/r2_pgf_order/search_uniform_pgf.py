#!/usr/bin/env python3
"""Hostile floating search for the stationary uniform-baseline PGF order.

This is discovery code.  Any apparent violation must be reconstructed with
the separate exact verifier before it is treated as mathematics.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
import scipy.linalg
from scipy.optimize import minimize_scalar
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigs


def marked_sparse(P: np.ndarray):
    n = len(P)
    states = [(C, v) for v in range(n) for C in range(1 << n) if not C >> v & 1]
    index = {state: i for i, state in enumerate(states)}
    rows, cols, data = [], [], []
    for source, (C, v) in enumerate(states):
        for i, probability in enumerate(P[v]):
            if probability <= 0:
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
    M = coo_matrix((data, (rows, cols)), shape=(len(states), len(states))).tocsr()
    return states, M


def stationary_rank_law(P: np.ndarray, tolerance: float = 2e-13):
    states, M = marked_sparse(P)
    law = np.full(len(states), 1 / len(states))
    # Cesaro averaging is unnecessary in the connected examples because the
    # chain has self-loops, but direct iteration is faster and its residual is
    # checked explicitly.
    for _ in range(1000):
        nxt = law @ M
        if np.max(np.abs(nxt - law)) < tolerance:
            law = nxt
            break
        law = nxt
    residual = np.max(np.abs(law @ M - law))
    if residual > 2e-10:
        # Extreme weight ratios can mix far too slowly for power iteration.
        # Shift-invert recovers the Perron vector directly in that regime.
        try:
            _, vectors = eigs(M.T, k=1, sigma=1.0, which="LM", tol=1e-12)
            law = np.real(vectors[:, 0])
            if law.sum() < 0:
                law = -law
            law /= law.sum()
        except RuntimeError:
            system = M.T.toarray() - np.eye(M.shape[0])
            system[-1, :] = 1
            rhs = np.zeros(M.shape[0])
            rhs[-1] = 1
            law = scipy.linalg.solve(system, rhs, check_finite=False)
        law[np.abs(law) < 1e-14] = 0
        residual = np.max(np.abs(law @ M - law))
        if residual > 2e-9 or law.min() < -1e-8:
            raise RuntimeError(f"stationary residual {residual}, minimum {law.min()}")
    n = len(P)
    eta = np.zeros(n)
    for probability, (C, _) in zip(law, states):
        eta[C.bit_count()] += probability
    eta /= eta.sum()
    return eta, residual


def pgf_gap(eta: np.ndarray, t: float) -> float:
    n = len(eta)
    return float(eta @ (t ** np.arange(n)) - ((1 + t) / 2) ** (n - 1))


def minimum_gap(eta: np.ndarray):
    grid = np.unique(np.r_[0, np.geomspace(1e-8, 1, 160), np.linspace(0, 1, 161)])
    gaps = np.array([pgf_gap(eta, t) for t in grid])
    candidates = [(gaps.min(), float(grid[gaps.argmin()]))]
    for i in range(1, len(grid) - 1):
        if gaps[i] <= gaps[i - 1] and gaps[i] <= gaps[i + 1]:
            opt = minimize_scalar(
                lambda z: pgf_gap(eta, z),
                bounds=(float(grid[i - 1]), float(grid[i + 1])),
                method="bounded",
                options={"xatol": 1e-14},
            )
            candidates.append((float(opt.fun), float(opt.x)))
    return min(candidates)


def kernel_from_weights(weights: np.ndarray):
    degrees = weights.sum(axis=1)
    if np.any(degrees <= 0):
        return None
    return weights / degrees[:, None]


def random_reversible(n: int, rng: np.random.Generator, sparsity: float):
    W = np.zeros((n, n))
    # A random spanning path guarantees connectedness.  Its ordering is
    # randomized, and all remaining edges are independently retained.
    order = rng.permutation(n)
    for i in range(n - 1):
        u, v = sorted((int(order[i]), int(order[i + 1])))
        W[u, v] = W[v, u] = 10 ** rng.uniform(-9, 9)
    for i, j in combinations(range(n), 2):
        if W[i, j] == 0 and rng.random() > sparsity:
            W[i, j] = W[j, i] = 10 ** rng.uniform(-9, 9)
    return W


def random_directed(n: int, rng: np.random.Generator, sparsity: float):
    raw = 10 ** rng.uniform(-9, 9, size=(n, n))
    raw[rng.random((n, n)) < sparsity] = 0
    np.fill_diagonal(raw, 0)
    # Keep a directed cycle so the kernel is irreducible.
    order = rng.permutation(n)
    for i in range(n):
        raw[order[i], order[(i + 1) % n]] = 10 ** rng.uniform(-9, 9)
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=826031)
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--sparsity", type=float, default=0.25)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    best = (float("inf"), None)
    for trial in range(args.trials):
        raw = (
            random_directed(args.n, rng, args.sparsity)
            if args.directed
            else random_reversible(args.n, rng, args.sparsity)
        )
        P = kernel_from_weights(raw)
        if P is None:
            continue
        eta, residual = stationary_rank_law(P)
        gap, t = minimum_gap(eta)
        if gap < best[0]:
            best = (gap, (trial, t, raw, eta, residual))
            print(f"best {gap:.16g} t={t:.12g} trial={trial} residual={residual:.2g}")
        if gap < -1e-9:
            break

    gap, payload = best
    print("minimum", gap)
    if payload is not None:
        trial, t, raw, eta, residual = payload
        print("trial", trial, "t", repr(t), "residual", residual)
        print("raw=", repr(raw.tolist()))
        print("eta=", repr(eta.tolist()))


if __name__ == "__main__":
    main()
