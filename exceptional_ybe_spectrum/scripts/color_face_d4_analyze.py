#!/usr/bin/env python3
"""Analyze the two canonical fixed algebras of a numerical d=4 solution.

For P=(I-H)/2 with scalar partial traces, consider the bistochastic maps

    Phi_1(x) = (2/d) Tr_2(P (x tensor I) P),
    Phi_2(x) = (2/d) Tr_1(P (I tensor x) P).

The saved unconstrained d=4 search point has a two-dimensional fixed algebra
for each map.  This script extracts their traceless Hermitian generators,
checks the claimed 2+2 spectra and commutation with P, then resolves P into
the resulting left/right "face" blocks.

This is numerical structural analysis, not an exact certificate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def partial_trace_2(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum("ijkj->ik", a.reshape(d, d, d, d))


def partial_trace_1(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum("ijil->jl", a.reshape(d, d, d, d))


def hermitian_basis(d: int) -> list[np.ndarray]:
    """Hilbert--Schmidt orthonormal Hermitian basis, identity first."""
    basis = [np.eye(d, dtype=np.complex128) / np.sqrt(d)]
    for k in range(1, d):
        diagonal = np.zeros((d, d), dtype=np.complex128)
        diagonal[np.arange(k), np.arange(k)] = 1.0
        diagonal[k, k] = -float(k)
        basis.append(diagonal / np.sqrt(k * (k + 1)))
    for i in range(d):
        for j in range(i + 1, d):
            symmetric = np.zeros((d, d), dtype=np.complex128)
            symmetric[i, j] = symmetric[j, i] = 1 / np.sqrt(2)
            basis.append(symmetric)
            antisymmetric = np.zeros((d, d), dtype=np.complex128)
            antisymmetric[i, j] = -1j / np.sqrt(2)
            antisymmetric[j, i] = 1j / np.sqrt(2)
            basis.append(antisymmetric)
    assert len(basis) == d * d
    return basis


def channel_matrix(channel, basis: list[np.ndarray]) -> np.ndarray:
    result = np.empty((len(basis), len(basis)), dtype=np.float64)
    for j, bj in enumerate(basis):
        image = channel(bj)
        for i, bi in enumerate(basis):
            result[i, j] = float(np.trace(bi @ image).real)
    return result


def fixed_reflection(
    channel, basis: list[np.ndarray], tolerance: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    matrix = channel_matrix(channel, basis)
    _, singular_values, vh = np.linalg.svd(matrix - np.eye(len(basis)))
    fixed = vh[singular_values < tolerance].conj().T
    if fixed.shape[1] != 2:
        raise RuntimeError(
            f"expected a two-dimensional fixed space, got {fixed.shape[1]}"
        )

    # Remove the identity component from either nonidentity fixed vector.
    coefficient = fixed[:, np.argmax(np.linalg.norm(fixed[1:, :], axis=0))]
    coefficient = coefficient - coefficient[0] * np.eye(len(basis))[0]
    coefficient = coefficient / np.linalg.norm(coefficient)
    generator = sum(
        (float(c) * b for c, b in zip(coefficient, basis)),
        np.zeros_like(basis[0]),
    )
    generator = (generator + generator.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(generator)

    # The numerical generator has eigenvalues +/-1/2, up to an overall sign.
    reflection = generator / np.mean(np.abs(eigenvalues))
    reflection = (reflection + reflection.conj().T) / 2
    reflection_eigenvalues, reflection_eigenvectors = np.linalg.eigh(reflection)
    order = np.argsort(reflection_eigenvalues)
    return (
        reflection,
        reflection_eigenvalues[order],
        reflection_eigenvectors[:, order],
    )


def block_indices(color: int, sector_dimension: int) -> np.ndarray:
    return np.arange(
        color * sector_dimension, (color + 1) * sector_dimension, dtype=np.int64
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fixed-tolerance", type=float, default=1e-7)
    args = parser.parse_args()

    h = np.load(args.candidate)["h"]
    d = int(round(np.sqrt(h.shape[0])))
    if d != 4:
        raise SystemExit("this calibration script expects d=4")
    identity = np.eye(d, dtype=np.complex128)
    p = (np.eye(d * d, dtype=np.complex128) - h) / 2
    scale = 2 / d

    phi_1 = lambda x: scale * partial_trace_2(
        p @ np.kron(x, identity) @ p, d
    )
    phi_2 = lambda x: scale * partial_trace_1(
        p @ np.kron(identity, x) @ p, d
    )
    basis = hermitian_basis(d)
    z1, eigenvalues_1, vectors_1 = fixed_reflection(
        phi_1, basis, args.fixed_tolerance
    )
    z2, eigenvalues_2, vectors_2 = fixed_reflection(
        phi_2, basis, args.fixed_tolerance
    )

    # Put negative then positive eigenspaces together.  These are the bases in
    # which the first and second tensor legs carry their respective colors.
    w1 = vectors_1
    w2 = vectors_2
    transformed_p = np.kron(w1, w2).conj().T @ p @ np.kron(w1, w2)

    off_block_squared = 0.0
    block_data: dict[str, dict[str, object]] = {}
    sector_dimension = 2
    for a in range(2):
        ia = block_indices(a, sector_dimension)
        for b in range(2):
            ib = block_indices(b, sector_dimension)
            pair_indices = np.asarray(
                [i * d + j for i in ia for j in ib], dtype=np.int64
            )
            block = transformed_p[np.ix_(pair_indices, pair_indices)]
            block_eigenvalues = np.linalg.eigvalsh(block)
            block_data[f"{a}{b}"] = {
                "trace": float(np.trace(block).real),
                "eigenvalues": [float(x) for x in block_eigenvalues],
                "projection_error": float(
                    np.linalg.norm(block @ block - block)
                ),
            }
            mask = np.ones(d * d, dtype=bool)
            mask[pair_indices] = False
            off_block_squared += float(
                np.linalg.norm(
                    transformed_p[np.ix_(pair_indices, np.flatnonzero(mask))]
                )
                ** 2
            )

    # Relative position of the two decompositions on a single local space.
    relative = w1.conj().T @ w2
    relative_blocks: dict[str, dict[str, object]] = {}
    overlap_spectra: dict[str, list[float]] = {}
    for a in range(2):
        ia = block_indices(a, sector_dimension)
        l_projection = w1[:, ia] @ w1[:, ia].conj().T
        for b in range(2):
            ib = block_indices(b, sector_dimension)
            r_projection = w2[:, ib] @ w2[:, ib].conj().T
            small = relative[np.ix_(ia, ib)]
            singular_values = np.linalg.svd(small, compute_uv=False)
            compressed_overlap = (
                w1[:, ia].conj().T
                @ r_projection
                @ w1[:, ia]
            )
            overlap_spectra[f"{a}{b}"] = [
                float(x) for x in np.linalg.eigvalsh(compressed_overlap)
            ]
            relative_blocks[f"{a}{b}"] = {
                "singular_values": [float(x) for x in singular_values],
                "scaled_unitarity_deviation": float(
                    np.linalg.norm(
                        small.conj().T @ small
                        - np.trace(small.conj().T @ small)
                        * np.eye(sector_dimension)
                        / sector_dimension
                    )
                ),
            }

    diagnostics = {
        "candidate": str(args.candidate.resolve()),
        "dimension": d,
        "ybe_residual": float(
            np.linalg.norm(
                np.kron(h, identity)
                @ np.kron(identity, h)
                @ np.kron(h, identity)
                - np.kron(identity, h)
                @ np.kron(h, identity)
                @ np.kron(identity, h)
                - (
                    np.kron(h, identity) - np.kron(identity, h)
                )
                / 3
            )
        ),
        "fixed_reflection_1_eigenvalues": [float(x) for x in eigenvalues_1],
        "fixed_reflection_2_eigenvalues": [float(x) for x in eigenvalues_2],
        "fixed_reflection_1_involution_error": float(
            np.linalg.norm(z1 @ z1 - identity)
        ),
        "fixed_reflection_2_involution_error": float(
            np.linalg.norm(z2 @ z2 - identity)
        ),
        "fixed_reflection_commutator": float(
            np.linalg.norm(z1 @ z2 - z2 @ z1)
        ),
        "p_commutator_first_color": float(
            np.linalg.norm(p @ np.kron(z1, identity) - np.kron(z1, identity) @ p)
        ),
        "p_commutator_second_color": float(
            np.linalg.norm(p @ np.kron(identity, z2) - np.kron(identity, z2) @ p)
        ),
        "face_off_block_frobenius": float(np.sqrt(off_block_squared)),
        "face_blocks": block_data,
        "relative_color_overlap_spectra": overlap_spectra,
        "relative_unitary_blocks": relative_blocks,
    }

    output = json.dumps(diagnostics, indent=2, sort_keys=True)
    print(output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
