#!/usr/bin/env python3
"""Search a qutrit-swap block enlargement of the exact Weyl cubic solution.

After grouping qubits and qutrits, put

    H = A (x) P_sym + B (x) P_asym,

where A,B are 4x4 Hermitian involutions on two qubits and P_sym/P_asym are
the symmetric/antisymmetric qutrit-pair projections.  Involutivity is then
automatic.  The exceptional three-site cubic is equivalent, for qutrit
dimension three, to six explicit 8x8 coefficient equations in the group
algebra of S_3.  This script minimizes those exact coefficient residuals.

The search is numerical and negative results do not prove nonexistence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy import linalg, optimize


QUBIT_PAIR_DIMENSION = 4
QUBIT_TRIPLE_DIMENSION = 8
DEFAULT_SEED = 26073501


def real_skew_generators(size: int) -> list[np.ndarray]:
    generators: list[np.ndarray] = []
    for row in range(size):
        for column in range(row + 1, size):
            generator = np.zeros((size, size), dtype=np.float64)
            generator[row, column] = 1
            generator[column, row] = -1
            generators.append(generator)
    return generators


def traceless_hermitian_generators(size: int) -> list[np.ndarray]:
    generators: list[np.ndarray] = []
    for row in range(size):
        for column in range(row + 1, size):
            real = np.zeros((size, size), dtype=np.complex128)
            real[row, column] = real[column, row] = 1
            imaginary = np.zeros((size, size), dtype=np.complex128)
            imaginary[row, column] = -1j
            imaginary[column, row] = 1j
            generators.extend((real, imaginary))
    for cutoff in range(1, size):
        diagonal = np.zeros((size, size), dtype=np.complex128)
        diagonal[:cutoff, :cutoff] += np.eye(cutoff)
        diagonal[cutoff, cutoff] = -cutoff
        diagonal /= np.sqrt(cutoff * (cutoff + 1))
        generators.append(diagonal)
    assert len(generators) == size * size - 1
    return generators


REAL_GENERATORS = real_skew_generators(QUBIT_PAIR_DIMENSION)
COMPLEX_GENERATORS = traceless_hermitian_generators(QUBIT_PAIR_DIMENSION)


def conjugated_signature(
    parameters: np.ndarray,
    plus_rank: int,
    field: str,
) -> np.ndarray:
    signature = np.diag(
        [1] * plus_rank + [-1] * (QUBIT_PAIR_DIMENSION - plus_rank)
    )
    if field == "real":
        generator = sum(
            (
                coefficient * basis
                for coefficient, basis in zip(parameters, REAL_GENERATORS)
            ),
            np.zeros_like(signature, dtype=np.float64),
        )
        unitary = linalg.expm(generator)
        return unitary @ signature @ unitary.T
    generator = sum(
        (
            coefficient * basis
            for coefficient, basis in zip(parameters, COMPLEX_GENERATORS)
        ),
        np.zeros_like(signature, dtype=np.complex128),
    )
    unitary = linalg.expm(1j * generator)
    return unitary @ signature @ unitary.conj().T


def split_parameters(
    parameters: np.ndarray,
    plus_rank_a: int,
    plus_rank_b: int,
    field: str,
) -> tuple[np.ndarray, np.ndarray]:
    count = len(REAL_GENERATORS) if field == "real" else len(COMPLEX_GENERATORS)
    cursor = 0
    if plus_rank_a in (0, 4):
        a = (1 if plus_rank_a == 4 else -1) * np.eye(4)
    else:
        a = conjugated_signature(
            parameters[cursor : cursor + count], plus_rank_a, field
        )
        cursor += count
    if plus_rank_b in (0, 4):
        b = (1 if plus_rank_b == 4 else -1) * np.eye(4)
    else:
        b = conjugated_signature(
            parameters[cursor : cursor + count], plus_rank_b, field
        )
        cursor += count
    assert cursor == len(parameters)
    return (
        a.astype(np.complex128, copy=False),
        b.astype(np.complex128, copy=False),
    )


def coefficient_residuals(
    a: np.ndarray,
    b: np.ndarray,
) -> list[np.ndarray]:
    """Return the six S_3 group-algebra coefficients of the cubic."""
    c = (a + b) / 2
    d = (a - b) / 2
    identity_two = np.eye(2, dtype=np.complex128)
    c_one = np.kron(c, identity_two)
    c_two = np.kron(identity_two, c)
    d_one = np.kron(d, identity_two)
    d_two = np.kron(identity_two, d)

    identity_coefficient = (
        c_one @ c_two @ c_one
        + d_one @ c_two @ d_one
        - c_two @ c_one @ c_two
        - d_two @ c_one @ d_two
        - (c_one - c_two) / 3
    )
    first_transposition = (
        c_one @ c_two @ d_one
        + d_one @ c_two @ c_one
        - c_two @ d_one @ c_two
        - d_one / 3
    )
    second_transposition = (
        c_one @ d_two @ c_one
        - c_two @ c_one @ d_two
        - d_two @ c_one @ c_two
        + d_two / 3
    )
    second_first = c_one @ d_two @ d_one - d_two @ d_one @ c_two
    first_second = d_one @ d_two @ c_one - c_two @ d_one @ d_two
    long_element = d_one @ d_two @ d_one - d_two @ d_one @ d_two
    return [
        identity_coefficient,
        first_transposition,
        second_transposition,
        second_first,
        first_second,
        long_element,
    ]


def real_residual_vector(
    parameters: np.ndarray,
    plus_rank_a: int,
    plus_rank_b: int,
    field: str,
    standardness_weight: float,
) -> np.ndarray:
    a, b = split_parameters(parameters, plus_rank_a, plus_rank_b, field)
    pieces = [
        coefficient.reshape(-1)
        for coefficient in coefficient_residuals(a, b)
    ]
    if standardness_weight:
        a_tensor = a.reshape(2, 2, 2, 2)
        b_tensor = b.reshape(2, 2, 2, 2)
        partial_second = (
            2 * np.einsum("abAb->aA", a_tensor)
            + np.einsum("abAb->aA", b_tensor)
        )
        partial_first = (
            2 * np.einsum("abaB->bB", a_tensor)
            + np.einsum("abaB->bB", b_tensor)
        )
        pieces.extend(
            (
                standardness_weight * partial_second.reshape(-1),
                standardness_weight * partial_first.reshape(-1),
            )
        )
    vector = np.concatenate(pieces)
    return np.concatenate((vector.real, vector.imag))


def qutrit_swap() -> np.ndarray:
    swap = np.zeros((9, 9), dtype=np.complex128)
    for first in range(3):
        for second in range(3):
            swap[second * 3 + first, first * 3 + second] = 1
    return swap


def full_h_sitewise(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Build H on (Q1,T1,Q2,T2), starting from grouped coordinates."""
    swap = qutrit_swap()
    p_symmetric = (np.eye(9) + swap) / 2
    p_antisymmetric = (np.eye(9) - swap) / 2
    grouped = np.kron(a, p_symmetric) + np.kron(b, p_antisymmetric)
    tensor = grouped.reshape(2, 2, 3, 3, 2, 2, 3, 3)
    # grouped row/column order is (Q1,Q2,T1,T2); sitewise is
    # (Q1,T1,Q2,T2).
    return tensor.transpose(0, 2, 1, 3, 4, 6, 5, 7).reshape(36, 36)


def full_cubic_norm(h: np.ndarray) -> float:
    h_one = np.kron(h, np.eye(6))
    h_two = np.kron(np.eye(6), h)
    residual = (
        h_one @ h_two @ h_one
        - h_two @ h_one @ h_two
        - (h_one - h_two) / 3
    )
    return float(np.linalg.norm(residual))


def run_search(
    seed: int,
    field: str,
    plus_rank_a: int,
    plus_rank_b: int,
    max_nfev: int,
    initial_scale: float,
    standardness_weight: float,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    generator_count = (
        len(REAL_GENERATORS) if field == "real" else len(COMPLEX_GENERATORS)
    )
    moving_blocks = int(plus_rank_a not in (0, 4)) + int(
        plus_rank_b not in (0, 4)
    )
    parameter_count = generator_count * moving_blocks
    initial = rng.normal(scale=initial_scale, size=parameter_count)
    started = time.time()
    result = optimize.least_squares(
        real_residual_vector,
        initial,
        args=(
            plus_rank_a,
            plus_rank_b,
            field,
            standardness_weight,
        ),
        method="trf",
        max_nfev=max_nfev,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
        verbose=0,
    )
    a, b = split_parameters(
        result.x, plus_rank_a, plus_rank_b, field
    )
    coefficients = coefficient_residuals(a, b)
    a_tensor = a.reshape(2, 2, 2, 2)
    b_tensor = b.reshape(2, 2, 2, 2)
    partial_second = (
        2 * np.einsum("abAb->aA", a_tensor)
        + np.einsum("abAb->aA", b_tensor)
    )
    partial_first = (
        2 * np.einsum("abaB->bB", a_tensor)
        + np.einsum("abaB->bB", b_tensor)
    )
    h = full_h_sitewise(a, b)
    eigenvalues = np.linalg.eigvalsh(h)
    encode_matrix = lambda matrix: [
        [
            [float(entry.real), float(entry.imag)]
            for entry in row
        ]
        for row in matrix
    ]
    return {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": "qutrit_swap_blocks",
        "seed": seed,
        "field": field,
        "plus_rank_a": plus_rank_a,
        "plus_rank_b": plus_rank_b,
        "parameter_count": parameter_count,
        "initial_scale": initial_scale,
        "standardness_weight": standardness_weight,
        "max_nfev": max_nfev,
        "actual_nfev": int(result.nfev),
        "actual_njev": None if result.njev is None else int(result.njev),
        "optimizer_status": int(result.status),
        "optimizer_message": result.message,
        "elapsed_seconds": time.time() - started,
        "coefficient_residual_norms": [
            float(np.linalg.norm(coefficient)) for coefficient in coefficients
        ],
        "coefficient_residual_total_norm": float(
            np.sqrt(sum(np.vdot(c, c).real for c in coefficients))
        ),
        "automatic_standardness_partial_second_norm": float(
            np.linalg.norm(partial_second)
        ),
        "automatic_standardness_partial_first_norm": float(
            np.linalg.norm(partial_first)
        ),
        "full_cubic_norm": full_cubic_norm(h),
        "involution_norm": float(np.linalg.norm(h @ h - np.eye(36))),
        "trace_h": [float(np.trace(h).real), float(np.trace(h).imag)],
        "h_eigenvalue_min": float(eigenvalues[0]),
        "h_eigenvalue_max": float(eigenvalues[-1]),
        "h_minus_one_count_tolerance_1e-8": int(
            np.sum(np.abs(eigenvalues + 1) < 1e-8)
        ),
        "h_plus_one_count_tolerance_1e-8": int(
            np.sum(np.abs(eigenvalues - 1) < 1e-8)
        ),
        "a_involution_norm": float(np.linalg.norm(a @ a - np.eye(4))),
        "b_involution_norm": float(np.linalg.norm(b @ b - np.eye(4))),
        "a_trace": [float(np.trace(a).real), float(np.trace(a).imag)],
        "b_trace": [float(np.trace(b).real), float(np.trace(b).imag)],
        "a_matrix": encode_matrix(a),
        "b_matrix": encode_matrix(b),
        "parameters": result.x.tolist(),
        "parameters_sha256": hashlib.sha256(
            result.x.astype("<f8").tobytes()
        ).hexdigest(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "warning": "Numerical search only; a small residual is not proof.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--field", choices=("real", "complex"), default="complex")
    parser.add_argument("--plus-rank-a", type=int, choices=range(5), default=2)
    parser.add_argument("--plus-rank-b", type=int, choices=range(5), default=2)
    parser.add_argument("--max-nfev", type=int, default=1500)
    parser.add_argument("--initial-scale", type=float, default=1.0)
    parser.add_argument("--standardness-weight", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if 6 * (2 * args.plus_rank_a - 4) + 3 * (
        2 * args.plus_rank_b - 4
    ) != 0:
        parser.error(
            "The signatures do not give trace(H)=0: require "
            "6 tr(A)+3 tr(B)=0."
        )
    payload = run_search(
        seed=args.seed,
        field=args.field,
        plus_rank_a=args.plus_rank_a,
        plus_rank_b=args.plus_rank_b,
        max_nfev=args.max_nfev,
        initial_scale=args.initial_scale,
        standardness_weight=args.standardness_weight,
    )
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n")


if __name__ == "__main__":
    main()
