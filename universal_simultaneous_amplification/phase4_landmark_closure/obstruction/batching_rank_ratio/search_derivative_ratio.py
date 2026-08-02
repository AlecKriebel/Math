#!/usr/bin/env python3
"""Numerical falsification of the normalized interpolation derivative.

This is discovery code.  For q_s=q_C/(1+s*x/2), it computes rho and rho'
by differentiating the exact finite linear system, then maximizes

    d_s log rho_G(s) - d_s log rho_Kn(s).
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution


def complete_log_derivative(n: int, s: float) -> float:
    powers = np.array([(2.0 / 3.0) ** ell for ell in range(1, n)])
    a_sum = powers.sum()
    b_sum = sum(
        ell * (2.0 / 3.0) ** ell for ell in range(1, n)
    ) / (2 * (n - 1))
    return -b_sum / (1 + a_sum + s * b_sum)


def value_and_log_derivative(weights: np.ndarray, s: float) -> tuple[float, float]:
    n = len(weights)
    p = weights / weights.sum(axis=1)[:, None]
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))
    matrix_prime = np.zeros_like(matrix)
    rhs = np.zeros(len(states))
    rhs_prime = np.zeros(len(states))
    for state in states:
        row = index[state]
        for target in range(n):
            x = sum(
                p[target, source]
                for source in range(n)
                if state >> source & 1
            )
            denominator = 1 + s * x / 2
            if state >> target & 1:
                base = 1 - x
                new_state = state & ~(1 << target)
            else:
                base = 1.5 * x
                new_state = state | (1 << target)
            rate = base / denominator
            rate_prime = -base * x / (2 * denominator**2)
            matrix[row, row] += rate
            matrix_prime[row, row] += rate_prime
            if new_state == full:
                rhs[row] += rate
                rhs_prime[row] += rate_prime
            elif new_state:
                matrix[row, index[new_state]] -= rate
                matrix_prime[row, index[new_state]] -= rate_prime
    values = np.linalg.solve(matrix, rhs)
    derivative = np.linalg.solve(
        matrix, rhs_prime - matrix_prime @ values
    )
    singleton_rows = [index[1 << vertex] for vertex in range(n)]
    rho = values[singleton_rows].mean()
    rho_prime = derivative[singleton_rows].mean()
    residual = max(
        np.linalg.norm(matrix @ values - rhs, ord=np.inf),
        np.linalg.norm(
            matrix @ derivative + matrix_prime @ values - rhs_prime,
            ord=np.inf,
        ),
    )
    if residual > 1e-7:
        raise FloatingPointError(f"linear residual {residual}")
    return float(rho), float(rho_prime / rho)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--s", type=float, default=0.5)
    parser.add_argument("--span", type=float, default=8)
    parser.add_argument("--iterations", type=int, default=80)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    pairs = list(itertools.combinations(range(args.n), 2))
    target = complete_log_derivative(args.n, args.s)
    best: list[object] = [-np.inf, None, None]

    def objective(logs: np.ndarray) -> float:
        logs = logs - logs.mean()
        weights = np.zeros((args.n, args.n))
        for (i, j), value in zip(pairs, np.exp(logs)):
            weights[i, j] = weights[j, i] = value
        try:
            rho, derivative = value_and_log_derivative(weights, args.s)
        except (FloatingPointError, np.linalg.LinAlgError):
            return 1e3
        excess = derivative - target
        if excess > best[0]:
            best[:] = [excess, weights.copy(), (rho, derivative)]
        return -excess

    differential_evolution(
        objective,
        [(-args.span, args.span)] * len(pairs),
        seed=args.seed,
        popsize=12,
        maxiter=args.iterations,
        polish=True,
    )
    print("complete derivative", target)
    print("best excess", best[0], "rho,derivative", best[2])
    print("weights", best[1].tolist() if best[1] is not None else None)


if __name__ == "__main__":
    main()
