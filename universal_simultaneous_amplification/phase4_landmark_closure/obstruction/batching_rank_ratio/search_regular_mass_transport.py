#!/usr/bin/env python3
"""Numerically falsify the regular-kernel occupation inequality.

For a symmetric stochastic zero-diagonal kernel P, the exact regular-case
linear-response identity reduces the normalized batching loss at s=0 to

    (r-1)/n * T(P),

where

    T(P) = sum_x E_{V\\{x}} int_0^tau
             1_H^T (P^2-P) 1_H dt

under the biased link process.  This discovery script searches the relative
interior of the symmetric stochastic polytope for T(P)<T(K_n).
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import differential_evolution


def symmetric_stochastic_basis(n: int) -> tuple[list[tuple[int, int]], np.ndarray]:
    pairs = list(itertools.combinations(range(n), 2))
    incidence = np.zeros((n, len(pairs)))
    for column, (i, j) in enumerate(pairs):
        incidence[i, column] = 1.0
        incidence[j, column] = 1.0
    return pairs, null_space(incidence)


def kernel_from_coordinates(
    n: int,
    pairs: list[tuple[int, int]],
    basis: np.ndarray,
    coordinates: np.ndarray,
) -> np.ndarray | None:
    edge_values = np.full(len(pairs), 1.0 / (n - 1)) + basis @ coordinates
    if edge_values.min() <= 1e-9:
        return None
    kernel = np.zeros((n, n))
    for value, (i, j) in zip(edge_values, pairs):
        kernel[i, j] = kernel[j, i] = value
    if np.max(np.abs(kernel.sum(axis=1) - 1.0)) > 1e-8:
        raise AssertionError("basis failed the stochastic constraints")
    return kernel


def occupation_integral(kernel: np.ndarray, fitness: float) -> float:
    n = len(kernel)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    generator = np.zeros((len(states), len(states)))
    integrand = np.zeros(len(states))
    square_minus = kernel @ kernel - kernel
    for state in states:
        row = index[state]
        indicator = np.array([(state >> v) & 1 for v in range(n)], dtype=float)
        integrand[row] = indicator @ square_minus @ indicator
        for target in range(n):
            q = kernel[target] @ indicator
            if (state >> target) & 1:
                rate = 1.0 - q
                new_state = state & ~(1 << target)
            else:
                rate = fitness * q
                new_state = state | (1 << target)
            generator[row, row] -= rate
            if new_state not in (0, full):
                generator[row, index[new_state]] += rate
    potential = np.linalg.solve(-generator, integrand)
    residual = np.linalg.norm(-generator @ potential - integrand, ord=np.inf)
    if residual > 1e-7:
        raise FloatingPointError(f"linear residual {residual}")
    return float(sum(potential[index[full ^ (1 << x)]] for x in range(n)))


def complete_target(n: int, fitness: float) -> float:
    powers = np.array([fitness ** (-ell) for ell in range(1, n)])
    a_sum = powers.sum()
    b_sum = (fitness - 1.0) / (n - 1) * sum(
        ell * fitness ** (-ell) for ell in range(1, n)
    )
    return n * b_sum / ((fitness - 1.0) * (1.0 + a_sum))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--fitness", type=float, default=1.5)
    parser.add_argument("--span", type=float, default=1.0)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    pairs, basis = symmetric_stochastic_basis(args.n)
    target = complete_target(args.n, args.fitness)
    complete = np.ones((args.n, args.n)) - np.eye(args.n)
    complete /= args.n - 1
    direct_target = occupation_integral(complete, args.fitness)
    if abs(target - direct_target) > 1e-8:
        raise AssertionError((target, direct_target))

    best: list[object] = [np.inf, None, None]

    def objective(coordinates: np.ndarray) -> float:
        kernel = kernel_from_coordinates(args.n, pairs, basis, coordinates)
        if kernel is None:
            return 1e3 + float(np.dot(coordinates, coordinates))
        try:
            value = occupation_integral(kernel, args.fitness)
        except (FloatingPointError, np.linalg.LinAlgError):
            return 1e3
        excess = value - target
        if excess < best[0]:
            best[:] = [excess, kernel.copy(), value]
        return excess

    dimension = basis.shape[1]
    if not dimension:
        print("polytope has no nontrivial directions")
        return
    differential_evolution(
        objective,
        [(-args.span, args.span)] * dimension,
        seed=args.seed,
        popsize=15,
        maxiter=args.iterations,
        polish=True,
    )
    print("dimension", dimension)
    print("complete T", target)
    print("best T-complete", best[0], "T", best[2])
    print("kernel", best[1].tolist() if best[1] is not None else None)


if __name__ == "__main__":
    main()
