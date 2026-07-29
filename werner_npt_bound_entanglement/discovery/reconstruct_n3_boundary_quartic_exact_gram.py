#!/usr/bin/env python3
"""Reconstruct an exact rational SOS Gram certificate on the flat face.

The rational face is built by ``build_n3_boundary_quartic_face_system``.
Sparse exact elimination leaves the free Gram parameters at rational
approximations to a numerical relative-interior point and solves all pivot
parameters exactly.  Success requires every reduced Gram block to remain
positive definite.

This script is discovery code until its output is checked by a smaller
independent verifier.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
import os
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "build_n3_boundary_quartic_face_system.py"
SPEC = importlib.util.spec_from_file_location("face_system", SOURCE)
face_system = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(face_system)

FREE_DENOMINATOR = int(
    os.environ.get("N3_QUARTIC_EXACT_FREE_DENOMINATOR", "10000000")
)
OUTPUT = Path(
    os.environ.get(
        "N3_QUARTIC_EXACT_GRAM_OUTPUT",
        "/tmp/n3_boundary_quartic_exact_gram.json",
    )
)


def eliminate(equations):
    """Sparse row-echelon elimination over the rationals."""

    pivots = {}
    insertion_order = []
    for _, original, original_rhs in sorted(
        equations, key=lambda equation: len(equation[1])
    ):
        row = {
            column: coefficient
            for column, coefficient in original.items()
            if coefficient
        }
        rhs = original_rhs
        for column in insertion_order:
            if column not in row:
                continue
            pivot_row, pivot_rhs = pivots[column]
            scale = row[column]
            for other, coefficient in pivot_row.items():
                row[other] = row.get(other, Fraction(0)) - scale * coefficient
                if not row[other]:
                    del row[other]
            rhs -= scale * pivot_rhs
        if row:
            column = min(row)
            scale = row[column]
            row = {
                other: coefficient / scale
                for other, coefficient in row.items()
            }
            rhs /= scale
            pivots[column] = (row, rhs)
            insertion_order.append(column)
        else:
            assert rhs == 0, ("inconsistent", rhs)
    return pivots, insertion_order


def numerical_reduced_grams(archive, blocks, bases):
    output = []
    for number, basis in enumerate(bases):
        basis_float = np.asarray(
            [[float(value) for value in row] for row in basis],
            dtype=float,
        )
        inverse = np.linalg.pinv(basis_float)
        gram = np.asarray(archive[f"gram_{number}"], dtype=float)
        reduced = inverse @ gram @ inverse.T
        output.append((reduced + reduced.T) / 2)
    return output


def exact_ldl(matrix):
    """Return exact positive LDL pivots, or fail on a nonpositive pivot."""

    size = len(matrix)
    lower = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    pivots = []
    for i in range(size):
        lower[i][i] = 1
        pivot = matrix[i][i] - sum(
            lower[i][k] * lower[i][k] * pivots[k] for k in range(i)
        )
        assert pivot > 0, (i, pivot)
        pivots.append(pivot)
        for j in range(i + 1, size):
            lower[j][i] = (
                matrix[j][i]
                - sum(
                    lower[j][k] * lower[i][k] * pivots[k]
                    for k in range(i)
                )
            ) / pivot
    return pivots


def encode_fraction(value: Fraction):
    return [value.numerator, value.denominator]


def main() -> None:
    effective_mode = bool(os.environ.get("N3_QUARTIC_EFFECTIVE"))
    (
        archive,
        _,
        blocks,
        bases,
        variable_pairs,
        equations,
    ) = face_system.build_system()
    pivots, insertion_order = eliminate(equations)
    pivot_columns = set(pivots)
    numerical = numerical_reduced_grams(archive, blocks, bases)

    values = [Fraction(0) for _ in variable_pairs]
    for column, (block, first, second) in enumerate(variable_pairs):
        if column not in pivot_columns:
            values[column] = Fraction(
                float(numerical[block][first, second])
            ).limit_denominator(FREE_DENOMINATOR)

    for column in reversed(insertion_order):
        row, rhs = pivots[column]
        values[column] = rhs - sum(
            coefficient * values[other]
            for other, coefficient in row.items()
            if other != column
        )

    # Exact coefficient check.
    for exponent, row, rhs in equations:
        value = sum(coefficient * values[column] for column, coefficient in row.items())
        assert value == rhs, (exponent, value, rhs)

    reduced_grams = []
    cursor = 0
    minimum_eigenvalue = float("inf")
    maximum_bits = 0
    for basis in bases:
        rank = len(basis[0])
        matrix = [[Fraction(0) for _ in range(rank)] for _ in range(rank)]
        for first in range(rank):
            for second in range(first, rank):
                value = values[cursor]
                cursor += 1
                matrix[first][second] = matrix[second][first] = value
                maximum_bits = max(
                    maximum_bits,
                    value.numerator.bit_length(),
                    value.denominator.bit_length(),
                )
        exact_ldl(matrix)
        if rank:
            minimum_eigenvalue = min(
                minimum_eigenvalue,
                float(np.linalg.eigvalsh(
                    np.asarray(
                        [
                            [float(value) for value in row]
                            for row in matrix
                        ]
                    )
                )[0]),
            )
        reduced_grams.append(matrix)
    assert cursor == len(values)

    certificate = {
        "format": (
            "n3-flat-kernel-effective-rational-face-v1"
            if effective_mode
            else "n3-flat-kernel-rational-face-v2"
        ),
        "dimension": 55,
        "quartic_terms": [
            [
                [
                    index
                    for index, power in enumerate(exponent)
                    for _ in range(power)
                ],
                encode_fraction(rhs),
            ]
            for exponent, _, rhs in equations
            if rhs
        ],
        "bases": [
            [[encode_fraction(value) for value in row] for row in basis]
            for basis in bases
        ],
        "reduced_grams": [
            [[encode_fraction(value) for value in row] for row in matrix]
            for matrix in reduced_grams
        ],
    }
    if effective_mode:
        effective_source = HERE / "build_n3_boundary_effective_quartic.py"
        effective_spec = importlib.util.spec_from_file_location(
            "effective_reduction", effective_source
        )
        effective_module = importlib.util.module_from_spec(effective_spec)
        assert effective_spec.loader is not None
        effective_spec.loader.exec_module(effective_module)
        _, positive_pivots, mixed_forms, independently_built = (
            effective_module.build()
        )
        target = {
            tuple(
                index
                for index, power in enumerate(exponent)
                for _ in range(power)
            ): rhs
            for exponent, _, rhs in equations
            if rhs
        }
        assert independently_built == target
        hessian = effective_module.boundary.hessian()
        certificate["lyapunov_schmidt"] = [
            {
                "pivot_coordinate": pivot,
                "hessian_diagonal": encode_fraction(
                    hessian[pivot][pivot]
                ),
                "mixed_quadratic_form": [
                    [list(monomial), encode_fraction(coefficient)]
                    for monomial, coefficient in sorted(form.items())
                ],
            }
            for pivot, form in zip(positive_pivots, mixed_forms)
        ]
    OUTPUT.write_text(json.dumps(certificate, separators=(",", ":")))
    print("equation rank", len(pivots))
    print("free variables", len(values) - len(pivots))
    print("minimum reduced eigenvalue", minimum_eigenvalue)
    print("maximum rational bit length", maximum_bits)
    print("certificate", OUTPUT, "bytes", OUTPUT.stat().st_size)


if __name__ == "__main__":
    main()
