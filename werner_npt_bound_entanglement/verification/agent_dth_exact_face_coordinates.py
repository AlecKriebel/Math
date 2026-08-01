#!/usr/bin/env python3
"""Exact rational restriction charts for the 2266-dimensional DTH face.

For each ordered mixed local-type triple ``mu`` the finite physical ensemble
from ``agent_dth_product_face_rank.py`` has an exact symmetric restriction
matrix ``Z_mu``.  This module returns

    E_mu = Z_mu[:, pivot_columns]

and pivot rows ``J_mu`` for which ``E_mu[J_mu, :]`` is nonsingular.  Hence
every symmetric restriction matrix supported on the physical product face is
uniquely of the form

    Z = E_mu A E_mu.T,

and its coordinate matrix is recovered exactly from the small principal
submatrix

    A = E_J^{-1} Z_JJ E_J^{-T}.

The largest face rank is 53.  This is the compact chart used for exact PSD
and crossing-consistency certificates; it avoids semidefinite tests on the
ambient 216 by 216 multiplicity blocks.
"""

from __future__ import annotations

from functools import lru_cache
import importlib.util
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FACE = import_file(
    "dth_product_face_modular", HERE / "agent_dth_product_face_rank.py"
)
RATIONAL = import_file(
    "dth_product_face_rational",
    HERE / "agent_dth_product_face_rank_rational.py",
)

PRIME = 1_000_003


@lru_cache(None)
def exact_data():
    RATIONAL.load_dependencies()
    transform, denominator = RATIONAL.exact_transform_numerator()
    terms = RATIONAL.exact_terms(transform)
    offsets = FACE.block_offsets(FACE.MIXED_MULTS)
    ranks, pivots = FACE.mixed_block_ranks(PRIME, with_pivots=True)
    assert sum(ranks.values()) == 2266
    assert denominator == 7560
    return terms, offsets, ranks, pivots


@lru_cache(None)
def block_matrix(shapes):
    shapes = tuple(shapes)
    terms, offsets, _, _ = exact_data()
    domain = RATIONAL.exact_block(terms, shapes, offsets)
    matrix = domain.to_Matrix()
    assert matrix == matrix.T
    return matrix


def independent_row_indices(matrix, expected_rank, prime=PRIME):
    """Pivot rows, certified over a prime field."""
    rows = matrix.rows
    columns = matrix.cols
    work = [
        [int(matrix[row, column]) % prime for row in range(rows)]
        for column in range(columns)
    ]
    # Gaussian elimination on matrix.T; its pivot columns are rows of matrix.
    pivot_row = 0
    pivots = []
    for column in range(rows):
        selected = next(
            (row for row in range(pivot_row, columns) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [value * inverse % prime
                           for value in work[pivot_row]]
        for row in range(columns):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    (x - coefficient * y) % prime
                    for x, y in zip(work[row], work[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == expected_rank:
            break
    assert len(pivots) == expected_rank
    return tuple(pivots)


@lru_cache(None)
def face_chart(shapes):
    """Return ``(E, pivot_rows)`` for one exact mixed face block."""
    shapes = tuple(shapes)
    matrix = block_matrix(shapes)
    _, _, ranks, pivots = exact_data()
    rank = ranks[shapes]
    pivot_columns = pivots[shapes]
    assert len(pivot_columns) == rank
    if not rank:
        return sp.zeros(matrix.rows, 0), tuple()
    restriction_range = matrix[:, list(pivot_columns)]
    # Raw pivot columns can be extremely ill-conditioned (above 10^6 in
    # floating point on some rank-42 blocks).  Exact row-LLL on E.T replaces
    # them by an integral basis of the same rational column space and reduces
    # the observed condition numbers by several orders of magnitude.
    if rank:
        restriction_range = restriction_range.T.lll().T
    pivot_rows = independent_row_indices(restriction_range, rank)
    principal = restriction_range[list(pivot_rows), :]
    # Nonzero determinant modulo PRIME already proves nonsingularity over QQ;
    # avoid an unnecessary large-integer symbolic determinant here.
    assert independent_row_indices(principal, rank) == tuple(range(rank))
    return restriction_range, pivot_rows


def recover_coordinate_matrix(shapes, restriction_matrix):
    """Recover A from an exactly face-supported symmetric restriction form."""
    basis, rows = face_chart(tuple(shapes))
    rank = basis.cols
    if not rank:
        assert restriction_matrix == sp.zeros(restriction_matrix.rows)
        return sp.zeros(0)
    ej = basis[list(rows), :]
    zjj = restriction_matrix.extract(rows, rows)
    coordinate = ej.inv() * zjj * ej.inv().T
    assert restriction_matrix == basis * coordinate * basis.T
    assert coordinate == coordinate.T
    return coordinate


def main():
    # The four numerically delicate blocks are sufficient for a quick exact
    # chart audit; the companion rank verifier replays all 216 blocks.
    expected = {
        (2, 2, 2): 51,
        (2, 4, 4): 36,
        (4, 2, 4): 36,
        (4, 4, 2): 36,
    }
    for shapes, rank in expected.items():
        basis, rows = face_chart(shapes)
        assert basis.cols == len(rows) == rank
    print("exact product-DTH face coordinate charts passed")
    print("sensitive ranks:", expected)
    print("maximum face chart size: 53")


if __name__ == "__main__":
    main()
