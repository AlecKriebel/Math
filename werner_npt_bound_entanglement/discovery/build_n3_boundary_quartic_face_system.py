#!/usr/bin/env python3
"""Build the exact rational linear system on the reconstructed SOS face.

The output is diagnostic discovery data.  It combines the exact quartic
with rational range bases reconstructed from a numerical relative-interior
Gram point, and reports the size and sparsity of the remaining affine
Gram problem.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import importlib.util
import os
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "search_n3_boundary_quartic_sos.py"
SPEC = importlib.util.spec_from_file_location("quartic_source", SOURCE)
quartic_source = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(quartic_source)

INPUT = os.environ.get(
    "N3_QUARTIC_GRAM_INPUT",
    "/tmp/n3_boundary_quartic_logdet1e3_grams.npz",
)
MAX_DENOMINATOR = int(os.environ.get("N3_QUARTIC_FACE_DENOMINATOR", "120"))
RANK_TOLERANCE = float(os.environ.get("N3_QUARTIC_FACE_RANK_TOLERANCE", "1e-5"))


def exact_rank(matrix):
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    pivots = []
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
        for row in range(rank + 1, rows):
            if not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                x - scale * y for x, y in zip(work[row], work[rank])
            ]
        pivots.append(column)
        rank += 1
        if rank == rows:
            break
    return rank, pivots


def rational_range_basis(gram):
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    rank = int(np.count_nonzero(eigenvalues > RANK_TOLERANCE))
    if not rank:
        return [[] for _ in range(gram.shape[0])]
    vectors = eigenvectors[:, -rank:]
    projector = vectors @ vectors.T
    exact = [
        [
            Fraction(float(value)).limit_denominator(MAX_DENOMINATOR)
            for value in row
        ]
        for row in projector
    ]
    _, independent_columns = exact_rank(exact)
    assert len(independent_columns) == rank
    basis = [
        [exact[row][column] for column in independent_columns]
        for row in range(len(exact))
    ]
    return basis


def build_system():
    if os.environ.get("N3_QUARTIC_EFFECTIVE"):
        effective_source = HERE / "build_n3_boundary_effective_quartic.py"
        effective_spec = importlib.util.spec_from_file_location(
            "effective_quartic", effective_source
        )
        effective_module = importlib.util.module_from_spec(effective_spec)
        assert effective_spec.loader is not None
        effective_spec.loader.exec_module(effective_module)
        _, _, _, effective = effective_module.build()
        dimension = 55
        target = {}
        for monomial, coefficient in effective.items():
            exponent = [0] * dimension
            for index in monomial:
                exponent[index] += 1
            target[tuple(exponent)] = coefficient
    else:
        _, polynomial = quartic_source.build_quartic()
        dimension = len(polynomial.gens)
        target = {
            exponent: Fraction(int(coefficient.p), int(coefficient.q))
            for exponent, coefficient in polynomial.terms()
        }

    archive = np.load(INPUT, allow_pickle=True)
    monomials = [tuple(map(int, row)) for row in archive["monomials"]]
    blocks = [list(map(int, block)) for block in archive["blocks"]]
    bases = [
        rational_range_basis(
            np.asarray(archive[f"gram_{number}"], dtype=float)
        )
        for number in range(len(blocks))
    ]

    variable_offset = []
    variable_pairs = []
    for block_number, basis in enumerate(bases):
        rank = len(basis[0])
        variable_offset.append(len(variable_pairs))
        variable_pairs.extend(
            (block_number, first, second)
            for first in range(rank)
            for second in range(first, rank)
        )

    rows = defaultdict(lambda: defaultdict(Fraction))
    for block_number, block in enumerate(blocks):
        basis = bases[block_number]
        rank = len(basis[0])
        local_variable = {
            (first, second): variable_offset[block_number] + number
            for number, (first, second) in enumerate(
                (first, second)
                for first in range(rank)
                for second in range(first, rank)
            )
        }
        for local_first, global_first in enumerate(block):
            for local_second in range(local_first, len(block)):
                global_second = block[local_second]
                exponent = [0] * dimension
                for index in monomials[global_first]:
                    exponent[index] += 1
                for index in monomials[global_second]:
                    exponent[index] += 1
                gram_multiplier = 1 if local_first == local_second else 2
                row = rows[tuple(exponent)]
                for first in range(rank):
                    diagonal = (
                        gram_multiplier
                        * basis[local_first][first]
                        * basis[local_second][first]
                    )
                    if diagonal:
                        row[local_variable[first, first]] += diagonal
                    for second in range(first + 1, rank):
                        coefficient = gram_multiplier * (
                            basis[local_first][first]
                            * basis[local_second][second]
                            + basis[local_first][second]
                            * basis[local_second][first]
                        )
                        if coefficient:
                            row[local_variable[first, second]] += coefficient

    all_exponents = set(rows) | set(target)
    equations = [
        (exponent, dict(rows[exponent]), target.get(exponent, Fraction(0)))
        for exponent in all_exponents
        if rows[exponent] or target.get(exponent, Fraction(0))
    ]
    return archive, monomials, blocks, bases, variable_pairs, equations


def main() -> None:
    _, _, blocks, bases, variable_pairs, equations = build_system()
    nonzeros = sum(len(row) for _, row, _ in equations)
    print("input", INPUT)
    print("blocks", len(blocks))
    print("face ranks", sum(len(basis[0]) for basis in bases))
    print("variables", len(variable_pairs))
    print("equations", len(equations))
    print("nonzeros", nonzeros)
    print("maximum row support", max(len(row) for _, row, _ in equations))


if __name__ == "__main__":
    main()
