#!/usr/bin/env python3
"""Reconstruct the rational minimal face of the flat-kernel SOS SDP.

This is discovery code.  It reads an approximate relative-interior Gram
solution, rationalizes each block's range projector, and verifies exact
idempotence.  A later verification layer must additionally reconstruct
the Gram matrices themselves and check the polynomial identity.
"""

from __future__ import annotations

from fractions import Fraction
import os

import numpy as np


INPUT = os.environ.get(
    "N3_QUARTIC_GRAM_INPUT",
    "/tmp/n3_boundary_quartic_logdet1e3_grams.npz",
)
MAX_DENOMINATOR = int(os.environ.get("N3_QUARTIC_FACE_DENOMINATOR", "120"))
RANK_TOLERANCE = float(os.environ.get("N3_QUARTIC_FACE_RANK_TOLERANCE", "1e-5"))
ENTRY_TOLERANCE = float(
    os.environ.get("N3_QUARTIC_FACE_ENTRY_TOLERANCE", "5e-4")
)


def multiply(first, second):
    rows = len(first)
    inner = len(second)
    columns = len(second[0])
    return [
        [
            sum(first[i][k] * second[k][j] for k in range(inner))
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def exact_rank(matrix):
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                x - scale * y for x, y in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def main() -> None:
    archive = np.load(INPUT, allow_pickle=True)
    blocks = archive["blocks"]
    maximum_error = 0.0
    rank_profiles = {}
    projectors = {}
    for number in range(len(blocks)):
        gram = np.asarray(archive[f"gram_{number}"], dtype=float)
        eigenvalues, eigenvectors = np.linalg.eigh(gram)
        numerical_rank = int(np.count_nonzero(eigenvalues > RANK_TOLERANCE))
        if numerical_rank:
            range_vectors = eigenvectors[:, -numerical_rank:]
            projector = range_vectors @ range_vectors.T
        else:
            projector = np.zeros_like(gram)
        exact = [
            [
                Fraction(float(value)).limit_denominator(MAX_DENOMINATOR)
                for value in row
            ]
            for row in projector
        ]
        error = max(
            abs(float(exact[i][j]) - projector[i, j])
            for i in range(len(exact))
            for j in range(len(exact))
        )
        maximum_error = max(maximum_error, error)
        assert error < ENTRY_TOLERANCE, (number, error)
        assert exact == [list(row) for row in zip(*exact)]
        assert multiply(exact, exact) == exact, number
        rational_rank = exact_rank(exact)
        assert rational_rank == numerical_rank, (
            number,
            rational_rank,
            numerical_rank,
        )
        rank_profiles[(len(exact), rational_rank)] = (
            rank_profiles.get((len(exact), rational_rank), 0) + 1
        )
        projectors[number] = exact

    print("input", INPUT)
    print("blocks", len(blocks))
    print("maximum rationalization error", maximum_error)
    print("exact rational face profiles")
    for profile, multiplicity in sorted(rank_profiles.items()):
        print(multiplicity, profile)


if __name__ == "__main__":
    main()
