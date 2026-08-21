#!/usr/bin/env python3
"""Search the exact three-pair scalar/slack ratio over rank-two matrices.

The optimized quotient is

    (2 sum_i r_i + 4 sum_i s_i) / (9 sum_i c_i)
      = 1 + 4 Q_3(C) / sum_i c_i.

Values below one would therefore be genuine numerical candidates for
unrestricted three-copy negativity.  This is discovery code only.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


BASIS = list(itertools.product(range(3), repeat=3))
N = 27
SUBSETS = [
    (),
    (0,),
    (1,),
    (2,),
    (0, 1),
    (0, 2),
    (1, 2),
    (0, 1, 2),
]
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


Q3_WEIGHTS = {
    (): 1.0,
    (0,): -0.5,
    (1,): -0.5,
    (2,): -0.5,
    (0, 1): 0.25,
    (0, 2): 0.25,
    (1, 2): 0.25,
    (0, 1, 2): -0.125,
}

# Sum of the three degree-two sector masses:
# (1/3) sum_i ||Tr_i C||^2
# - (2/9) sum_{i<j} ||Tr_ij C||^2
# + (1/9) |Tr C|^2.
DEGREE_TWO_WEIGHTS = {
    (): 0.0,
    (0,): 1.0 / 3.0,
    (1,): 1.0 / 3.0,
    (2,): 1.0 / 3.0,
    (0, 1): -2.0 / 9.0,
    (0, 2): -2.0 / 9.0,
    (1, 2): -2.0 / 9.0,
    (0, 1, 2): 1.0 / 9.0,
}


def quadratic_operator(
    matrix: np.ndarray, weights: dict[tuple[int, ...], float]
) -> np.ndarray:
    result = np.zeros_like(matrix)
    for subset, weight in weights.items():
        if weight == 0:
            continue
        if not subset:
            result += weight * matrix
        else:
            result += weight * trace_adjoint(
                partial_trace(matrix, subset), subset
            )
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


def objective_and_gradient(parameters: np.ndarray) -> tuple[float, np.ndarray]:
    left, right = unpack(parameters)
    matrix = left @ right.conj().T
    q3_image = quadratic_operator(matrix, Q3_WEIGHTS)
    degree_two_image = quadratic_operator(matrix, DEGREE_TWO_WEIGHTS)
    q3_value = np.vdot(matrix, q3_image).real
    degree_two_value = np.vdot(matrix, degree_two_image).real
    quotient = 1.0 + 4.0 * q3_value / degree_two_value
    residual = 4.0 * (
        q3_image - (q3_value / degree_two_value) * degree_two_image
    ) / degree_two_value
    left_gradient = residual @ right
    right_gradient = residual.conj().T @ left
    gradient = 2.0 * np.concatenate(
        (
            left_gradient.real.ravel(),
            left_gradient.imag.ravel(),
            right_gradient.real.ravel(),
            right_gradient.imag.ravel(),
        )
    )
    return quotient, gradient


def trace_norm_squared(
    matrix: np.ndarray, subset: tuple[int, ...]
) -> float:
    reduced = partial_trace(matrix, tuple(sorted(subset)))
    return float(np.vdot(reduced, reduced).real)


def diagnostics(matrix: np.ndarray) -> dict[str, object]:
    trace_masses = {
        subset: trace_norm_squared(matrix, subset)
        for subset in SUBSETS
        if subset
    }
    q3_value = float(
        np.vdot(matrix, quadratic_operator(matrix, Q3_WEIGHTS)).real
    )
    c_values = []
    q_values = []
    t_values = []
    w_values = []
    for site in range(3):
        others = tuple(index for index in range(3) if index != site)
        first, second = others
        t_site = partial_trace(matrix, (site,))
        t_value = (
            np.vdot(t_site, t_site).real
            - 0.5
            * (
                trace_norm_squared(matrix, (site, first))
                + trace_norm_squared(matrix, (site, second))
            )
            + 0.25 * trace_norm_squared(matrix, (0, 1, 2))
        )
        q_value = (
            np.vdot(matrix, matrix).real
            - 0.5
            * (
                trace_norm_squared(matrix, (first,))
                + trace_norm_squared(matrix, (second,))
            )
            + 0.25 * trace_norm_squared(matrix, others)
        )
        w_value = (
            np.vdot(t_site, t_site).real
            - (
                trace_norm_squared(matrix, (site, first))
                + trace_norm_squared(matrix, (site, second))
            )
            / 3.0
            + trace_norm_squared(matrix, (0, 1, 2)) / 9.0
        )
        c_values.append(w_value / 3.0)
        q_values.append(q_value)
        t_values.append(t_value)
        w_values.append(w_value)
    r_values = [
        1.5 * w_value - t_value
        for w_value, t_value in zip(w_values, t_values)
    ]
    s_values = [
        3.0 * q_value - t_value
        for q_value, t_value in zip(q_values, t_values)
    ]
    left_vectors, _, right_adjoint = np.linalg.svd(matrix, full_matrices=False)
    right_vectors = right_adjoint.conj().T

    def local_purities(vector: np.ndarray) -> list[float]:
        tensor = vector.reshape(3, 3, 3)
        purities = []
        for site in range(3):
            matricized = np.moveaxis(tensor, site, 0).reshape(3, 9)
            marginal = matricized @ matricized.conj().T
            purities.append(float(np.vdot(marginal, marginal).real))
        return purities

    def plane_local_spectra(vectors: np.ndarray) -> list[list[float]]:
        plane = sum(
            np.outer(vectors[:, index], vectors[:, index].conj())
            for index in range(2)
        )
        tensor = plane.reshape(3, 3, 3, 3, 3, 3)
        spectra = []
        for site in range(3):
            marginal = np.zeros((3, 3), complex)
            for row_value in range(3):
                for column_value in range(3):
                    total = 0j
                    for other_values in itertools.product(range(3), repeat=2):
                        row = [0] * 3
                        column = [0] * 3
                        row[site] = row_value
                        column[site] = column_value
                        other_sites = [
                            index for index in range(3) if index != site
                        ]
                        for other_site, value in zip(
                            other_sites, other_values
                        ):
                            row[other_site] = column[other_site] = value
                        total += tensor[tuple(row + column)]
                    marginal[row_value, column_value] = total
            spectra.append(
                [float(value) for value in np.linalg.eigvalsh(marginal)]
            )
        return spectra

    return {
        "q3": q3_value,
        "normality_squared": float(
            np.vdot(
                matrix @ matrix.conj().T - matrix.conj().T @ matrix,
                matrix @ matrix.conj().T - matrix.conj().T @ matrix,
            ).real
        ),
        "left_singular_vector_local_purities": [
            local_purities(left_vectors[:, index]) for index in range(2)
        ],
        "right_singular_vector_local_purities": [
            local_purities(right_vectors[:, index]) for index in range(2)
        ],
        "left_plane_local_spectra": plane_local_spectra(left_vectors),
        "right_plane_local_spectra": plane_local_spectra(right_vectors),
        "left_right_plane_principal_cosines": [
            float(value)
            for value in np.linalg.svd(
                left_vectors[:, :2].conj().T @ right_vectors[:, :2],
                compute_uv=False,
            )
        ],
        "c": c_values,
        "q": q_values,
        "t": t_values,
        "r": r_values,
        "s": s_values,
        "trace_masses": trace_masses,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--seed", type=int, default=9731)
    args = parser.parse_args()
    generator = np.random.default_rng(args.seed)
    for start in range(args.starts):
        left = generator.normal(size=(27, 2)) + 1j * generator.normal(
            size=(27, 2)
        )
        right = generator.normal(size=(27, 2)) + 1j * generator.normal(
            size=(27, 2)
        )
        result = minimize(
            objective_and_gradient,
            pack(left, right),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": 1500,
                "maxfun": 4000,
                "ftol": 1e-15,
                "gtol": 1e-10,
                "maxls": 50,
            },
        )
        left, right = unpack(result.x)
        matrix = left @ right.conj().T
        matrix /= np.linalg.norm(matrix)
        print(
            f"start={start} ratio={result.fun:.16g} "
            f"iterations={result.nit} "
            f"singular_values={np.linalg.svd(matrix, compute_uv=False)[:2]}"
        )
        print(diagnostics(matrix))


if __name__ == "__main__":
    main()
