"""Discovery search for the qutrit three-copy operator cofactor bound.

For an isometry U:C^2 -> (C^3)^tensor3, this tests

    M_Q(|U><U|) - coefficient * H(U) >= 0,

where H(U) is the kernel-compatible cofactor form recorded in the log.
This is numerical discovery code only.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np


DIMS = (2, 3, 3, 3)
DIMENSION = int(np.prod(DIMS))


def trace_replace(matrix: np.ndarray, site: int) -> np.ndarray:
    tensor = matrix.reshape(DIMS + DIMS)
    reduced = np.trace(tensor, axis1=site, axis2=len(DIMS) + site)
    out = np.zeros(DIMS + DIMS, dtype=complex)
    for digit in range(DIMS[site]):
        selection = [slice(None)] * (2 * len(DIMS))
        selection[site] = digit
        selection[len(DIMS) + site] = digit
        out[tuple(selection)] = reduced
    return out.reshape(DIMENSION, DIMENSION)


def reduced_matrix(matrix: np.ndarray, site: int) -> np.ndarray:
    tensor = matrix.reshape(DIMS + DIMS)
    row_labels = list("abcd")
    column_labels = list("efgh")
    for other_site in range(len(DIMS)):
        if other_site != site:
            column_labels[other_site] = row_labels[other_site]
    expression = (
        "".join(row_labels + column_labels)
        + "->"
        + row_labels[site]
        + column_labels[site]
    )
    return np.einsum(expression, tensor)


def adjugate_three(matrix: np.ndarray) -> np.ndarray:
    return np.array(
        [
            [
                matrix[1, 1] * matrix[2, 2]
                - matrix[1, 2] * matrix[2, 1],
                matrix[0, 2] * matrix[2, 1]
                - matrix[0, 1] * matrix[2, 2],
                matrix[0, 1] * matrix[1, 2]
                - matrix[0, 2] * matrix[1, 1],
            ],
            [
                matrix[1, 2] * matrix[2, 0]
                - matrix[1, 0] * matrix[2, 2],
                matrix[0, 0] * matrix[2, 2]
                - matrix[0, 2] * matrix[2, 0],
                matrix[0, 2] * matrix[1, 0]
                - matrix[0, 0] * matrix[1, 2],
            ],
            [
                matrix[1, 0] * matrix[2, 1]
                - matrix[1, 1] * matrix[2, 0],
                matrix[0, 1] * matrix[2, 0]
                - matrix[0, 0] * matrix[2, 1],
                matrix[0, 0] * matrix[1, 1]
                - matrix[0, 1] * matrix[1, 0],
            ],
        ]
    )


def embed_local(matrix: np.ndarray, site: int) -> np.ndarray:
    factors = [np.eye(dimension) for dimension in DIMS]
    factors[site] = matrix
    out = factors[0]
    for factor in factors[1:]:
        out = np.kron(out, factor)
    return out


def anchored_operators(
    isometry: np.ndarray, coefficient: float = 2.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[float]]:
    vector = isometry.T.reshape(-1)
    projection = np.outer(vector, vector.conj())
    endpoint = projection
    for site in (1, 2, 3):
        endpoint = 2 * trace_replace(endpoint, site) - endpoint

    reductions = [
        reduced_matrix(projection, site) for site in (1, 2, 3)
    ]
    determinants = [
        float(np.linalg.det(reduction).real) for reduction in reductions
    ]
    hodge = np.zeros_like(endpoint)
    for position, site in enumerate((1, 2, 3)):
        other = [index for index in range(3) if index != position]
        hodge += (
            determinants[other[0]]
            * determinants[other[1]]
            * embed_local(adjugate_three(reductions[position]), site)
        )
    residual = endpoint - coefficient * hodge
    return (
        (residual + residual.conj().T) / 2,
        (endpoint + endpoint.conj().T) / 2,
        hodge,
        determinants,
    )


def factorized_zero_anchor() -> np.ndarray:
    out = np.zeros((27, 2), dtype=complex)
    for logical in range(2):
        for physical in range(3):
            index = 9 * physical + 3 * physical + logical
            out[index, logical] = 1 / np.sqrt(3)
    return out


def retract(anchor: np.ndarray, tangent: np.ndarray, scale: float) -> np.ndarray:
    candidate = anchor + scale * tangent
    return np.linalg.qr(candidate)[0]


def random_tangent(
    anchor: np.ndarray, generator: np.random.Generator
) -> np.ndarray:
    raw = generator.normal(size=anchor.shape) + 1j * generator.normal(
        size=anchor.shape
    )
    tangent = raw - anchor @ ((anchor.conj().T @ raw + raw.conj().T @ anchor) / 2)
    return tangent / np.linalg.norm(tangent)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--scale", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=120729)
    parser.add_argument("--coefficient", type=float, default=2.0)
    args = parser.parse_args()
    generator = np.random.default_rng(args.seed)
    anchor = factorized_zero_anchor()
    best = (float("inf"), None)
    for trial in range(args.trials):
        tangent = random_tangent(anchor, generator)
        isometry = retract(anchor, tangent, args.scale)
        residual, endpoint, _, determinants = anchored_operators(
            isometry, args.coefficient
        )
        eigenvalue = float(np.linalg.eigvalsh(residual)[0])
        scaled = eigenvalue / (args.scale * args.scale)
        if scaled < best[0]:
            best = (
                scaled,
                (
                    trial,
                    eigenvalue,
                    float(np.linalg.eigvalsh(endpoint)[0]),
                    determinants,
                    tangent,
                ),
            )
            print("best", best[0], best[1][0:4], flush=True)
    if best[1] is not None:
        np.save("/tmp/n3_qutrit_hodge_best_tangent.npy", best[1][4])


if __name__ == "__main__":
    main()
