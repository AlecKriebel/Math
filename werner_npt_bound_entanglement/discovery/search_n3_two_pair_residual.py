#!/usr/bin/env python3
"""Numerically minimize lambda Q_23(C) + R(Tr_1 C) over rank-two C.

This is discovery code only.  The optimization uses the exact analytic
gradient of the Rayleigh quotient in a rank-two factorization C = U V^*.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


BASIS = list(itertools.product(range(3), repeat=3))
N = 27
SUBSETS = [(), (1,), (2,), (1, 2), (0, 1), (0, 2), (0, 1, 2)]
REMAINING = {
    subset: tuple(i for i in range(3) if i not in subset)
    for subset in SUBSETS
}


def partial_trace(matrix: np.ndarray, subset: tuple[int, ...]) -> np.ndarray:
    remaining = REMAINING[subset]
    remaining_tuples = list(
        itertools.product(range(3), repeat=len(remaining))
    )
    traced_tuples = list(itertools.product(range(3), repeat=len(subset)))
    result = np.zeros((len(remaining_tuples), len(remaining_tuples)), complex)
    for row_index, row_remaining in enumerate(remaining_tuples):
        for column_index, column_remaining in enumerate(remaining_tuples):
            for traced in traced_tuples:
                row = [0] * 3
                column = [0] * 3
                for site, value in zip(remaining, row_remaining):
                    row[site] = value
                for site, value in zip(remaining, column_remaining):
                    column[site] = value
                for site, value in zip(subset, traced):
                    row[site] = column[site] = value
                result[row_index, column_index] += matrix[
                    (row[0] * 3 + row[1]) * 3 + row[2],
                    (column[0] * 3 + column[1]) * 3 + column[2],
                ]
    return result


def trace_adjoint(matrix: np.ndarray, subset: tuple[int, ...]) -> np.ndarray:
    remaining = REMAINING[subset]
    remaining_tuples = list(
        itertools.product(range(3), repeat=len(remaining))
    )
    remaining_index = {
        values: index for index, values in enumerate(remaining_tuples)
    }
    result = np.zeros((N, N), complex)
    for row_index, row in enumerate(BASIS):
        for column_index, column in enumerate(BASIS):
            if all(row[site] == column[site] for site in subset):
                result[row_index, column_index] = matrix[
                    remaining_index[tuple(row[site] for site in remaining)],
                    remaining_index[tuple(column[site] for site in remaining)],
                ]
    return result


def pack(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.concatenate(
        (
            left.real.ravel(),
            left.imag.ravel(),
            right.real.ravel(),
            right.imag.ravel(),
        )
    )


def unpack(parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    left = parameters[:54].reshape(27, 2) + 1j * parameters[54:108].reshape(
        27, 2
    )
    right = parameters[108:162].reshape(
        27, 2
    ) + 1j * parameters[162:].reshape(27, 2)
    return left, right


def coefficients(lam: float) -> dict[tuple[int, ...], float]:
    return {
        (): lam,
        (1,): -lam / 2,
        (2,): -lam / 2,
        (1, 2): lam / 4,
        (0, 1): 1 / 6,
        (0, 2): 1 / 6,
        (0, 1, 2): -5 / 36,
    }


def quadratic_operator(
    matrix: np.ndarray, weights: dict[tuple[int, ...], float]
) -> np.ndarray:
    result = np.zeros_like(matrix)
    for subset, weight in weights.items():
        if not subset:
            result += weight * matrix
        else:
            result += weight * trace_adjoint(
                partial_trace(matrix, subset), subset
            )
    return result


def objective_and_gradient(
    parameters: np.ndarray, weights: dict[tuple[int, ...], float]
) -> tuple[float, np.ndarray]:
    left, right = unpack(parameters)
    matrix = left @ right.conj().T
    norm_squared = np.vdot(matrix, matrix).real
    image = quadratic_operator(matrix, weights)
    value = np.vdot(matrix, image).real / norm_squared
    residual = (image - value * matrix) / norm_squared
    left_gradient = residual @ right
    right_gradient = residual.conj().T @ left
    gradient = 2 * np.concatenate(
        (
            left_gradient.real.ravel(),
            left_gradient.imag.ravel(),
            right_gradient.real.ravel(),
            right_gradient.imag.ravel(),
        )
    )
    return value, gradient


def component_values(matrix: np.ndarray) -> dict[tuple[int, ...], float]:
    return {
        subset: float(
            np.vdot(
                partial_trace(matrix, subset),
                partial_trace(matrix, subset),
            ).real
        )
        for subset in SUBSETS
        if subset
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lambda-values", nargs="+", type=float, required=True)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=9511)
    args = parser.parse_args()
    generator = np.random.default_rng(args.seed)
    for lam in args.lambda_values:
        weights = coefficients(lam)
        best_value = float("inf")
        best_matrix = None
        for _ in range(args.starts):
            left = generator.normal(size=(27, 2)) + 1j * generator.normal(
                size=(27, 2)
            )
            right = generator.normal(size=(27, 2)) + 1j * generator.normal(
                size=(27, 2)
            )
            result = minimize(
                lambda parameters: objective_and_gradient(parameters, weights),
                pack(left, right),
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": 1000,
                    "maxfun": 3000,
                    "ftol": 1e-15,
                    "gtol": 1e-10,
                    "maxls": 50,
                },
            )
            if result.fun < best_value:
                best_value = result.fun
                left, right = unpack(result.x)
                best_matrix = left @ right.conj().T
                best_matrix /= np.linalg.norm(best_matrix)
        assert best_matrix is not None
        print(
            f"lambda={lam:.16g} minimum={best_value:.16g} "
            f"singular_values={np.linalg.svd(best_matrix, compute_uv=False)[:2]}"
        )
        print(component_values(best_matrix))


if __name__ == "__main__":
    main()
