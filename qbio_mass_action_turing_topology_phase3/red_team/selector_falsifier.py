#!/usr/bin/env python3
"""Independent exact audit of the Boolean principal-submatrix selector."""
from __future__ import annotations

import itertools
import json
import random
from fractions import Fraction
from typing import Sequence

Matrix = tuple[tuple[Fraction, ...], ...]


def det(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    work = [list(row) for row in matrix]
    sign = 1
    value = Fraction(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            sign *= -1
        p = work[col][col]
        value *= p
        for row in range(col + 1, n):
            if work[row][col] == 0:
                continue
            factor = work[row][col] / p
            for j in range(col + 1, n):
                work[row][j] -= factor * work[col][j]
            work[row][col] = Fraction(0)
    return value if sign > 0 else -value


def main() -> int:
    rng = random.Random(20260813)
    matrices = 0
    selectors = 0
    for n in range(1, 8):
        for _ in range(120):
            A: Matrix = tuple(
                tuple(Fraction(rng.randint(-7, 7), rng.randint(1, 5)) for _ in range(n))
                for _ in range(n)
            )
            for bits in itertools.product((0, 1), repeat=n):
                chosen = tuple(i for i, bit in enumerate(bits) if bit)
                # Build I-S-SAS directly from the definition.
                M = tuple(
                    tuple(
                        (Fraction(1) if i == j else Fraction(0))
                        - (Fraction(bits[i]) if i == j else Fraction(0))
                        - Fraction(bits[i] * bits[j]) * A[i][j]
                        for j in range(n)
                    )
                    for i in range(n)
                )
                lhs = det(M)
                principal = tuple(tuple(A[i][j] for j in chosen) for i in chosen)
                rhs = det(principal)
                if len(chosen) % 2:
                    rhs = -rhs
                if lhs != rhs:
                    raise AssertionError({"n": n, "bits": bits, "lhs": str(lhs), "rhs": str(rhs)})
                if not chosen and lhs != 1:
                    raise AssertionError("empty selector was not exactly 1")
                selectors += 1
            matrices += 1
    print(json.dumps({
        "status": "PASS",
        "random_rational_matrices": matrices,
        "boolean_selectors_checked": selectors,
        "empty_selector_negative": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
