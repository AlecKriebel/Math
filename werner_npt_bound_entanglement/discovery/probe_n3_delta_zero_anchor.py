#!/usr/bin/env python3
"""Discovery probe for the implication delta(A)=0 => M_A >= 0.

This is floating-point discovery code, not a verifier.  It minimizes the
proved diagonal defect

    delta(A) = 3 q_K - 2 sum_i q_Ki + sum_i q_i

for a pure vector A on K x (C^d)^3, then diagonalizes the exact anchored
operator

    M_A = (I-|A><A|)/2 + 3 rho_K
          - 2 sum_i rho_Ki + sum_{i<j} rho_Kij,

where every reduced operator is lifted by identities on its complement.
The auxiliary system K has dimension two.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


def reduced_pure(vector: np.ndarray, dims: tuple[int, ...], keep: tuple[int, ...]):
    tensor = vector.reshape(dims)
    complement = tuple(i for i in range(len(dims)) if i not in keep)
    order = keep + complement
    matrix = np.transpose(tensor, order).reshape(
        np.prod([dims[i] for i in keep], dtype=int), -1
    )
    return matrix @ matrix.conj().T


def lift_reduction(
    reduced: np.ndarray,
    dims: tuple[int, ...],
    keep: tuple[int, ...],
) -> np.ndarray:
    complement = tuple(i for i in range(len(dims)) if i not in keep)
    matrix = np.kron(
        reduced,
        np.eye(np.prod([dims[i] for i in complement], dtype=int)),
    )
    ordered_dims = tuple(dims[i] for i in keep + complement)
    tensor = matrix.reshape(ordered_dims + ordered_dims)
    inverse = np.argsort(keep + complement)
    axes = tuple(inverse) + tuple(len(dims) + inverse)
    return np.transpose(tensor, axes).reshape(
        np.prod(dims, dtype=int), np.prod(dims, dtype=int)
    )


def unpack(point: np.ndarray, dimension: int) -> np.ndarray:
    vector = point[:dimension] + 1j * point[dimension:]
    return vector / np.linalg.norm(vector)


def diagonal_defect(vector: np.ndarray, dims: tuple[int, ...]) -> float:
    q_k = np.vdot(
        reduced_pure(vector, dims, (0,)),
        reduced_pure(vector, dims, (0,)),
    ).real
    value = 3 * q_k
    for site in (1, 2, 3):
        rho_ki = reduced_pure(vector, dims, (0, site))
        rho_i = reduced_pure(vector, dims, (site,))
        value -= 2 * np.vdot(rho_ki, rho_ki).real
        value += np.vdot(rho_i, rho_i).real
    return float(value)


def anchored_operator(vector: np.ndarray, dims: tuple[int, ...]) -> np.ndarray:
    dimension = int(np.prod(dims))
    projection = np.outer(vector, vector.conj())
    out = (np.eye(dimension) - projection) / 2
    rho_k = reduced_pure(vector, dims, (0,))
    out += 3 * lift_reduction(rho_k, dims, (0,))
    for site in (1, 2, 3):
        rho_ki = reduced_pure(vector, dims, (0, site))
        out -= 2 * lift_reduction(rho_ki, dims, (0, site))
    for first, second in itertools.combinations((1, 2, 3), 2):
        rho_kij = reduced_pure(vector, dims, (0, first, second))
        out += lift_reduction(rho_kij, dims, (0, first, second))
    return (out + out.conj().T) / 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=int, default=3)
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--save-threshold", type=float, default=1e-9)
    args = parser.parse_args()

    dims = (2, args.local, args.local, args.local)
    dimension = int(np.prod(dims))
    rng = np.random.default_rng(args.seed)
    best = None

    for start in range(args.starts):
        initial = rng.normal(size=2 * dimension)
        result = minimize(
            lambda point: diagonal_defect(unpack(point, dimension), dims),
            initial,
            method="L-BFGS-B",
            options={"maxiter": args.iterations, "ftol": 1e-14, "gtol": 1e-10},
        )
        vector = unpack(result.x, dimension)
        defect = diagonal_defect(vector, dims)
        spectrum = np.linalg.eigvalsh(anchored_operator(vector, dims))
        record = (defect, float(spectrum[0]), vector)
        if best is None or (record[0], record[1]) < (best[0], best[1]):
            best = record
        print(
            start,
            "delta",
            f"{defect:.12g}",
            "lambda_min",
            f"{spectrum[0]:.12g}",
            "zeros",
            int(np.count_nonzero(np.abs(spectrum) < 1e-7)),
            "nit",
            result.nit,
            flush=True,
        )

    assert best is not None
    print("best delta/lambda_min", best[0], best[1])
    if best[0] < args.save_threshold:
        np.savez(
            "n3_delta_zero_anchor_best.npz",
            vector=best[2],
            dims=np.asarray(dims),
            delta=best[0],
            lambda_min=best[1],
        )


if __name__ == "__main__":
    main()
