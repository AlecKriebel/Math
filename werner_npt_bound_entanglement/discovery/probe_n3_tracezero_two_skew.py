#!/usr/bin/env python3
"""Search the two-skew exterior inequality on trace-zero rank-two matrices.

The tested quantity is

    3 N - 2 S + P + 2 s1 s2,

where N is the Hilbert--Schmidt norm, S is the sum of one-site
partial-trace norms, and P the sum of two-site partial-trace norms.
The unrestricted inequality is known to be false.  This probe asks
whether merely imposing Tr(C)=0 could explain the square-zero case.
Floating-point output is discovery evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import minimize


DIMS = (3, 3, 3)


def partial_trace(matrix: np.ndarray, sites: tuple[int, ...]) -> np.ndarray:
    tensor = matrix.reshape(DIMS + DIMS)
    number = 3
    for site in sorted(sites, reverse=True):
        tensor = np.trace(tensor, axis1=site, axis2=site + number)
        number -= 1
    return tensor.reshape(3**number, 3**number)


def exterior_quantity(matrix: np.ndarray) -> float:
    norm = float(np.vdot(matrix, matrix).real)
    one = sum(
        float(np.vdot(reduced, reduced).real)
        for reduced in (
            partial_trace(matrix, (0,)),
            partial_trace(matrix, (1,)),
            partial_trace(matrix, (2,)),
        )
    )
    pair = sum(
        float(np.vdot(reduced, reduced).real)
        for reduced in (
            partial_trace(matrix, (0, 1)),
            partial_trace(matrix, (0, 2)),
            partial_trace(matrix, (1, 2)),
        )
    )
    singular = np.linalg.svd(matrix, compute_uv=False)[:2]
    return 3 * norm - 2 * one + pair + 2 * singular[0] * singular[1]


def random_isometry(
    rng: np.random.Generator, columns: int
) -> np.ndarray:
    raw = rng.standard_normal((27, columns)) + 1j * rng.standard_normal(
        (27, columns)
    )
    return np.linalg.qr(raw)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--optimize-counterfamily", action="store_true")
    parser.add_argument("--optimize-corrected", action="store_true")
    args = parser.parse_args()
    if args.optimize_counterfamily:
        optimize_counterfamily()
        return
    if args.optimize_corrected:
        optimize_corrected()
        return
    rng = np.random.default_rng(args.seed)
    best = (float("inf"), None)
    for sample in range(args.samples):
        left = random_isometry(rng, 2)
        right = random_isometry(rng, 2)
        overlap = right.conj().T @ left
        coefficient = (
            rng.standard_normal((2, 2))
            + 1j * rng.standard_normal((2, 2))
        )
        normal = overlap.conj().T
        denominator = float(np.vdot(normal, normal).real)
        if denominator > 1e-14:
            coefficient -= (
                np.trace(overlap @ coefficient) / denominator
            ) * normal
        coefficient /= np.linalg.norm(coefficient)
        matrix = left @ coefficient @ right.conj().T
        value = exterior_quantity(matrix)
        if value < best[0]:
            best = (value, sample)
    print("best trace-zero exterior quantity", best)


BINARY_INDICES = np.asarray((0, 1, 3, 4, 9, 10, 12, 13))


def unpack_binary_factors(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = vector.reshape(4, 8, 2)
    factors = []
    for factor in range(2):
        matrix = values[2 * factor] + 1j * values[2 * factor + 1]
        factors.append(matrix)
    return factors[0], factors[1]


def pack_binary_factors(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.stack(
        (left.real, left.imag, right.real, right.imag)
    ).reshape(-1)


def embedded_product(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    full_left = np.zeros((27, 2), dtype=np.complex128)
    full_right = np.zeros((27, 2), dtype=np.complex128)
    full_left[BINARY_INDICES] = left
    full_right[BINARY_INDICES] = right
    return full_left @ full_right.conj().T


def normalized_exterior(vector: np.ndarray) -> float:
    left, right = unpack_binary_factors(vector)
    matrix = embedded_product(left, right)
    norm = float(np.vdot(matrix, matrix).real)
    return exterior_quantity(matrix) / norm


def normalized_corrected_exterior(vector: np.ndarray) -> float:
    left, right = unpack_binary_factors(vector)
    matrix = embedded_product(left, right)
    norm = float(np.vdot(matrix, matrix).real)
    spectral_determinant = abs(np.linalg.det(right.conj().T @ left))
    return (exterior_quantity(matrix) + 2 * spectral_determinant) / norm


def factor_norm_constraint(vector: np.ndarray, factor: int) -> float:
    left, right = unpack_binary_factors(vector)
    matrix = left if factor == 0 else right
    return float(np.vdot(matrix, matrix).real) - 1.0


def trace_constraint(vector: np.ndarray, component: int) -> float:
    left, right = unpack_binary_factors(vector)
    value = np.trace(right.conj().T @ left)
    return float(value.real if component == 0 else value.imag)


def optimize_counterfamily() -> None:
    """Constrained finite-difference search seeded by the exact counterpencil."""

    left = np.column_stack(
        (
            np.asarray(
                (4 + 3j, 0, 0, 5, 0, -3 - 3j, 4 + 2j, -9 - 3j)
            ),
            np.asarray((1 - 1j, 0, 0, -2j, 0, -1 + 1j, 1 - 1j, -2j)),
        )
    )
    right = np.column_stack(
        (
            np.asarray(
                (
                    1 + 7j,
                    -2 - 7j,
                    4 + 6j,
                    -5 - 5j,
                    1 - 7j,
                    7j,
                    -2 - 7j,
                    3 + 6j,
                )
            ),
            np.asarray((1, 0, 0, 0, 0, 0, 0, 0)),
        )
    )
    left /= np.linalg.norm(left)
    right /= np.linalg.norm(right)
    initial = pack_binary_factors(left, right)
    constraints = [
        {"type": "eq", "fun": lambda value: factor_norm_constraint(value, 0)},
        {"type": "eq", "fun": lambda value: factor_norm_constraint(value, 1)},
        {"type": "eq", "fun": lambda value: trace_constraint(value, 0)},
        {"type": "eq", "fun": lambda value: trace_constraint(value, 1)},
    ]
    result = minimize(
        normalized_exterior,
        initial,
        method="SLSQP",
        constraints=constraints,
        options={"maxiter": 2000, "ftol": 1e-12, "disp": True},
    )
    print("success", result.success, result.message)
    print("objective", result.fun)
    print("constraints", [constraint["fun"](result.x) for constraint in constraints])
    left, right = unpack_binary_factors(result.x)
    np.savez(
        "/tmp/n3_tracezero_two_skew_candidate.npz",
        left=left,
        right=right,
    )


def optimize_corrected() -> None:
    """Try to falsify the overlap-corrected exterior inequality."""

    left = np.column_stack(
        (
            np.asarray(
                (4 + 3j, 0, 0, 5, 0, -3 - 3j, 4 + 2j, -9 - 3j)
            ),
            np.asarray((1 - 1j, 0, 0, -2j, 0, -1 + 1j, 1 - 1j, -2j)),
        )
    )
    right = np.column_stack(
        (
            np.asarray(
                (
                    1 + 7j,
                    -2 - 7j,
                    4 + 6j,
                    -5 - 5j,
                    1 - 7j,
                    7j,
                    -2 - 7j,
                    3 + 6j,
                )
            ),
            np.asarray((1, 0, 0, 0, 0, 0, 0, 0)),
        )
    )
    left /= np.linalg.norm(left)
    right /= np.linalg.norm(right)
    initial = pack_binary_factors(left, right)
    constraints = [
        {"type": "eq", "fun": lambda value: factor_norm_constraint(value, 0)},
        {"type": "eq", "fun": lambda value: factor_norm_constraint(value, 1)},
    ]
    result = minimize(
        normalized_corrected_exterior,
        initial,
        method="SLSQP",
        constraints=constraints,
        options={"maxiter": 3000, "ftol": 1e-12, "disp": True},
    )
    print("success", result.success, result.message)
    print("objective", result.fun)
    print("constraints", [constraint["fun"](result.x) for constraint in constraints])
    left, right = unpack_binary_factors(result.x)
    print("overlap", right.conj().T @ left)
    np.savez(
        "/tmp/n3_corrected_two_skew_candidate.npz",
        left=left,
        right=right,
    )


if __name__ == "__main__":
    main()
