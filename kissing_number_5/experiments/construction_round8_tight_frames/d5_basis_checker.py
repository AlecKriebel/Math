#!/usr/bin/env python3
"""Exact obstruction to partitioning the oriented D5 roots into bases."""

from __future__ import annotations

import itertools
import math


def oriented_d5_roots() -> list[tuple[int, ...]]:
    roots = []
    for i in range(5):
        for j in range(i + 1, 5):
            for first in (-1, 1):
                for second in (-1, 1):
                    vector = [0] * 5
                    vector[i] = first
                    vector[j] = second
                    roots.append(tuple(vector))
    assert len(roots) == 40
    return roots


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def verify() -> dict[str, object]:
    roots = oriented_d5_roots()
    assert all(dot(root, root) == 2 for root in roots)
    orthogonal_four = next(
        subset
        for subset in itertools.combinations(range(40), 4)
        if all(
            dot(roots[i], roots[j]) == 0
            for i, j in itertools.combinations(subset, 2)
        )
    )

    # If five normalized roots formed an orthonormal basis, the integer
    # matrix A with those roots as rows would satisfy A A^T=2I_5.  Hence
    # det(A)^2=2^5=32.  But det(A) is an integer, and 32 is not an integer
    # square.  Thus no five-root orthogonal set exists.
    determinant_square_for_hypothetical_basis = 2**5
    integer_sqrt = math.isqrt(determinant_square_for_hypothetical_basis)
    assert integer_sqrt**2 < determinant_square_for_hypothetical_basis
    assert (integer_sqrt + 1) ** 2 > determinant_square_for_hypothetical_basis

    return {
        "status": "PASS",
        "oriented_roots": len(roots),
        "explicit_orthogonal_four_indices": list(orthogonal_four),
        "explicit_orthogonal_four": [list(roots[i]) for i in orthogonal_four],
        "maximum_orthogonal_subset_size": 4,
        "five_basis_determinant_square": determinant_square_for_hypothetical_basis,
        "partition_into_eight_bases": False,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
