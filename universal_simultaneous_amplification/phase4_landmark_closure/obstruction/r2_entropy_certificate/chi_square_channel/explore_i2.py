#!/usr/bin/env python3
"""Explore the stationary random-target chi-square information at r=2.

This is discovery code, not a proof certificate.  It constructs the exact
geometric-union transition probabilities (in floating point), solves for the
stationary law on nonempty subsets, and reports the posterior target collision
functional I2.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
from scipy.linalg import eig
from scipy.optimize import differential_evolution


def union_law(row: np.ndarray) -> dict[int, float]:
    support = np.flatnonzero(row > 1e-15).tolist()
    vals = np.zeros(1 << len(support))
    for mask in range(1, 1 << len(support)):
        mass = sum(row[support[j]] for j in range(len(support)) if mask >> j & 1)
        vals[mask] = mass / (2.0 - mass)
    for j in range(len(support)):
        for mask in range(1 << len(support)):
            if mask >> j & 1:
                vals[mask] -= vals[mask ^ (1 << j)]
    ans = {}
    for mask in range(1, 1 << len(support)):
        actual = sum(1 << support[j] for j in range(len(support)) if mask >> j & 1)
        if vals[mask] > 1e-14:
            ans[actual] = vals[mask]
    assert abs(sum(ans.values()) - 1) < 1e-9
    return ans


def stationary_i2(P: np.ndarray) -> tuple[float, float, float, np.ndarray]:
    n = len(P)
    states = np.arange(1, 1 << n)
    index = {int(s): i for i, s in enumerate(states)}
    laws = [union_law(P[v]) for v in range(n)]
    kernels = np.zeros((n, len(states), len(states)))
    for v in range(n):
        for ia, aa in enumerate(states):
            a = int(aa)
            if not (a >> v) & 1:
                kernels[v, ia, ia] = 1
            else:
                for u, prob in laws[v].items():
                    b = (a & ~(1 << v)) | u
                    kernels[v, ia, index[b]] += prob
    T = kernels.mean(axis=0)
    values, vectors = eig(T.T)
    idx = np.argmin(np.abs(values - 1))
    pi = np.real(vectors[:, idx])
    if pi.sum() < 0:
        pi *= -1
    pi /= pi.sum()
    pi[np.abs(pi) < 1e-14] = 0
    mus = np.einsum("a,vab->vb", pi, kernels)
    positive = pi > 1e-13
    f = np.zeros_like(mus)
    f[:, positive] = mus[:, positive] / pi[positive]
    i2 = np.sum(mus[:, positive] ** 2 / pi[positive]) / n
    maxf = np.max(f[:, positive])
    mean_density = sum(pi[i] * int(int(s).bit_count()) for i, s in enumerate(states)) / n
    return float(i2), float(maxf), float(mean_density), f


def directed_kernel(n: int, x: np.ndarray) -> np.ndarray:
    P = np.zeros((n, n))
    q = 0
    for i in range(n):
        logits = []
        js = []
        for j in range(n):
            if i != j:
                logits.append(x[q])
                js.append(j)
                q += 1
        logits = np.asarray(logits)
        weights = np.exp(logits - logits.max())
        weights /= weights.sum()
        P[i, js] = weights
    return P


def reversible_kernel(n: int, x: np.ndarray) -> np.ndarray:
    W = np.zeros((n, n))
    for value, (i, j) in zip(x, combinations(range(n), 2)):
        W[i, j] = W[j, i] = np.exp(value)
    return W / W.sum(axis=1, keepdims=True)


def optimize(n: int, directed: bool, seed: int, bound: float) -> None:
    dim = n * (n - 1) if directed else n * (n - 1) // 2
    builder = directed_kernel if directed else reversible_kernel

    def objective(x: np.ndarray) -> float:
        try:
            return -stationary_i2(builder(n, x))[0]
        except Exception:
            return 1e3

    result = differential_evolution(
        objective,
        [(-bound, bound)] * dim,
        seed=seed,
        popsize=8,
        maxiter=150,
        polish=True,
        workers=1,
        updating="immediate",
    )
    P = builder(n, result.x)
    i2, maxf, density, _ = stationary_i2(P)
    print(f"n={n} directed={directed} I2={i2:.12g} maxf={maxf:.12g} density={density:.12g}")
    np.set_printoptions(precision=8, suppress=True)
    print(P)


def random_scan(n: int, directed: bool, count: int, seed: int, scale: float) -> None:
    rng = np.random.default_rng(seed)
    dim = n * (n - 1) if directed else n * (n - 1) // 2
    builder = directed_kernel if directed else reversible_kernel
    best = (-np.inf, None, None)
    for _ in range(count):
        x = rng.normal(0, scale, dim)
        P = builder(n, x)
        result = stationary_i2(P)
        if result[0] > best[0]:
            best = (result[0], P, result)
    i2, maxf, density, _ = best[2]
    print(f"random n={n} directed={directed} I2={i2:.12g} maxf={maxf:.12g} density={density:.12g}")
    print(best[1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--random", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--scale", type=float, default=3.0)
    parser.add_argument("--bound", type=float, default=6.0)
    args = parser.parse_args()
    if args.random:
        random_scan(args.n, args.directed, args.random, args.seed, args.scale)
    else:
        optimize(args.n, args.directed, args.seed, args.bound)


if __name__ == "__main__":
    main()
