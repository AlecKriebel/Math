#!/usr/bin/env python3
"""Discovery search for the stationary Shannon entropy-reflection gap."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import numpy as np
from scipy.linalg import solve
from scipy.optimize import differential_evolution


_SPEC = importlib.util.spec_from_file_location(
    "explore_i2", Path(__file__).with_name("explore_i2.py")
)
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MOD)
union_law = _MOD.union_law
directed_kernel = _MOD.directed_kernel
reversible_kernel = _MOD.reversible_kernel


def stationary_data(P: np.ndarray):
    n = len(P)
    states = list(range(1, 1 << n))
    index = {state: pos for pos, state in enumerate(states)}
    laws = [union_law(P[v]) for v in range(n)]
    kernels = []
    average = np.zeros((len(states), len(states)))
    for v in range(n):
        kernel = np.zeros_like(average)
        for A in states:
            if not (A >> v) & 1:
                kernel[index[A], index[A]] = 1
            else:
                for U, probability in laws[v].items():
                    B = (A & ~(1 << v)) | U
                    kernel[index[A], index[B]] += probability
        kernels.append(kernel)
        average += kernel / n
    matrix = average.T - np.eye(len(states))
    matrix[-1] = 1
    rhs = np.zeros(len(states))
    rhs[-1] = 1
    pi = solve(matrix, rhs, assume_a="gen", check_finite=False)
    return states, kernels, pi


def entropy_gap(P: np.ndarray) -> tuple[float, float, float, float]:
    n = len(P)
    states, kernels, pi = stationary_data(P)
    mus = [pi @ kernel for kernel in kernels]
    information = 0.0
    mixing_entropy = 0.0
    direct_gap = 0.0
    for pos, B in enumerate(states[:-1]):
        probability = pi[pos]
        if probability <= 1e-14:
            continue
        k = B.bit_count()
        h = n - k
        x = k / n
        mixing_entropy += probability * (-x * np.log(x) - (1-x) * np.log(1-x))
        posterior = np.array([mus[v][pos] / (n * probability) for v in range(n)])
        positive = posterior > 1e-15
        information += probability * np.sum(posterior[positive] * np.log(n * posterior[positive]))
        divergence = np.sum(posterior[positive] * np.log(h * posterior[positive]))
        direct_gap += probability * (x * np.log(h / k) - divergence)
    return direct_gap, mixing_entropy - information, mixing_entropy, information


def optimize(n: int, directed: bool, seed: int, bound: float) -> None:
    dim = n * (n - 1) if directed else n * (n - 1) // 2
    builder = directed_kernel if directed else reversible_kernel

    def objective(x: np.ndarray) -> float:
        try:
            return entropy_gap(builder(n, x))[0]
        except Exception:
            return 1e3

    result = differential_evolution(
        objective,
        [(-bound, bound)] * dim,
        seed=seed,
        popsize=10,
        maxiter=250,
        polish=True,
        workers=1,
    )
    P = builder(n, result.x)
    values = entropy_gap(P)
    print(f"n={n} directed={directed} gap={values[0]:.14g} M-I={values[1]:.14g} M={values[2]:.14g} I={values[3]:.14g}")
    np.set_printoptions(precision=10, suppress=True)
    print(P)


def random_scan(n: int, directed: bool, count: int, seed: int, scale: float) -> None:
    rng = np.random.default_rng(seed)
    dim = n * (n - 1) if directed else n * (n - 1) // 2
    builder = directed_kernel if directed else reversible_kernel
    best = (np.inf, None, None)
    for _ in range(count):
        P = builder(n, rng.normal(0, scale, dim))
        values = entropy_gap(P)
        if values[0] < best[0]:
            best = (values[0], P, values)
    print(f"random n={n} directed={directed} gap={best[0]:.14g} values={best[2]}")
    print(best[1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--random", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--scale", type=float, default=4.0)
    parser.add_argument("--bound", type=float, default=10.0)
    args = parser.parse_args()
    if args.random:
        random_scan(args.n, args.directed, args.random, args.seed, args.scale)
    else:
        optimize(args.n, args.directed, args.seed, args.bound)


if __name__ == "__main__":
    main()
