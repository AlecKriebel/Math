#!/usr/bin/env python3
"""Inspect an SDP Gram matrix for exact quadratic-field structure.

This is discovery code.  It intentionally depends only on NumPy so it can
run in the numerical virtual environment used for the SDP searches.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import math
import os

import numpy as np


INPUT = os.environ.get(
    "N3_QUARTIC_GRAM_INPUT",
    "/tmp/n3_boundary_quartic_trace_grams.npz",
)
MAX_DENOMINATOR = int(os.environ.get("N3_QUARTIC_FIELD_DENOMINATOR", "128"))
MAX_RADICAL_COEFFICIENT = int(
    os.environ.get("N3_QUARTIC_FIELD_RADICAL_COEFFICIENT", "256")
)


def nearest_quadratic_field(value: float):
    """Find a small (p+r sqrt(14))/q nearest to ``value``."""

    root = math.sqrt(14)
    best = None
    for denominator in range(1, MAX_DENOMINATOR + 1):
        scaled = denominator * value
        for radical in range(
            -MAX_RADICAL_COEFFICIENT, MAX_RADICAL_COEFFICIENT + 1
        ):
            rational = round(scaled - radical * root)
            error = abs(value - (rational + radical * root) / denominator)
            score = (
                error,
                denominator + abs(rational) + abs(radical),
                denominator,
            )
            if best is None or score < best[0]:
                best = (
                    score,
                    int(rational),
                    int(radical),
                    denominator,
                )
    assert best is not None
    return best


def expression(data) -> str:
    _, rational, radical, denominator = data
    return f"({rational:+d}{radical:+d}*sqrt(14))/{denominator}"


def main() -> None:
    archive = np.load(INPUT, allow_pickle=True)
    blocks = archive["blocks"]
    matrices = [
        np.asarray(archive[f"gram_{number}"], dtype=float)
        for number in range(len(blocks))
    ]

    # Cluster values coarsely so numerical splitting of symmetry-equivalent
    # entries does not dominate the report.
    occurrences: defaultdict[int, list[float]] = defaultdict(list)
    for matrix in matrices:
        for value in matrix.flat:
            if abs(value) > 1e-7:
                occurrences[round(float(value) * 1e6)].append(float(value))

    print("input", INPUT)
    print("nonzero value clusters", len(occurrences))
    print("largest clusters")
    for _, values in sorted(
        occurrences.items(), key=lambda item: (-len(item[1]), -abs(item[0]))
    )[:100]:
        mean = sum(values) / len(values)
        candidate = nearest_quadratic_field(mean)
        print(
            f"{len(values):5d} mean={mean:+.12f} "
            f"spread={max(values)-min(values):.2e} "
            f"err={candidate[0][0]:.2e} {expression(candidate)}"
        )

    print("block spectra")
    profiles = Counter()
    for number, matrix in enumerate(matrices):
        eigenvalues = np.linalg.eigvalsh(matrix)
        rank = int(np.count_nonzero(eigenvalues > 1e-6))
        profile = (
            matrix.shape[0],
            rank,
            tuple(np.round(eigenvalues[eigenvalues > 1e-6], 6)),
        )
        profiles[profile] += 1
        if matrix.shape[0] >= 8:
            print(
                number,
                matrix.shape[0],
                rank,
                np.round(eigenvalues, 9).tolist(),
            )
    print("repeated spectral profiles")
    for profile, multiplicity in profiles.most_common():
        print(multiplicity, profile)


if __name__ == "__main__":
    main()
