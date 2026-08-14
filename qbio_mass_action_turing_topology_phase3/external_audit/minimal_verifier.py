#!/usr/bin/env python3
"""Minimal exact verifier for the external PARTITION reduction examples."""
from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp


def partition_signs(numbers: list[int]) -> list[tuple[int, ...]]:
    return [s for s in itertools.product((-1, 1), repeat=len(numbers))
            if sum(a * t for a, t in zip(numbers, s)) == 0]


def hurwitz_determinants(matrix: sp.Matrix) -> list[sp.Expr]:
    lam = sp.symbols("lambda")
    coefficients = matrix.charpoly(lam).all_coeffs()
    n = matrix.rows
    a = [sp.Integer(1)] + coefficients[1:]
    hurwitz = sp.zeros(n)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            index = 2 * i - j
            if 0 <= index <= n:
                hurwitz[i - 1, j - 1] = a[index]
    return [sp.factor(hurwitz[:r, :r].det()) for r in range(1, n + 1)]


def family(numbers: list[int]) -> tuple[int, int, sp.Matrix, sp.Rational, sp.Matrix]:
    k = math.isqrt(len(numbers)) + 1
    while k * k <= len(numbers):
        k += 1
    m = k * k
    padded = numbers + [0] * (m - len(numbers))
    a = sp.Matrix(padded)
    gamma = int((a.T * a)[0])
    beta = sp.Rational(1) - sp.Rational(1, 2 * m * (1 + gamma))
    Q = sp.eye(m) + a * a.T
    return k, m, a, beta, Q


def yes_matrix(numbers: list[int], signs: list[int]) -> sp.Matrix:
    k, m, a, beta, Q = family(numbers)
    padded_signs = signs + [1] * (m - len(signs))
    if any(t not in (-1, 1) for t in signs):
        raise ValueError("signs must be +/-1")
    if sum(x * t for x, t in zip(numbers, signs)) != 0:
        raise ValueError("sign vector is not a partition witness")
    r = (sp.Integer(1) + beta) / 2
    t = sp.Matrix(padded_signs)
    x = r * t
    y = -r * t
    return (-k * Q).row_join(y).col_join(x.T.row_join(sp.Matrix([[k * beta]])))


def verify(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    numbers = data.get("numbers")
    expected = data.get("expected")
    if not isinstance(numbers, list) or not numbers or any(type(a) is not int or a <= 0 for a in numbers):
        raise ValueError("numbers must be a nonempty list of positive integers")
    solutions = partition_signs(numbers)
    actual = "YES" if solutions else "NO"
    if actual != expected:
        raise AssertionError(f"source enumeration gives {actual}, expected {expected}")
    result: dict[str, object] = {
        "file": str(path),
        "source_status": actual,
        "solution_count": len(solutions),
    }
    if actual == "YES":
        signs = data.get("signs")
        if not isinstance(signs, list) or len(signs) != len(numbers):
            raise ValueError("YES file requires a full signs list")
        matrix = yes_matrix(numbers, signs)
        deltas = hurwitz_determinants(matrix)
        if not all(delta > 0 for delta in deltas):
            raise AssertionError("constructed open-cube matrix is not exactly Hurwitz")
        k, m, a, beta, Q = family(numbers)
        r = (sp.Integer(1) + beta) / 2
        if not (0 < r < 1):
            raise AssertionError("witness is not in the open cube")
        result.update({
            "dimension": matrix.rows,
            "beta": str(beta),
            "interior_scale": str(r),
            "hurwitz_determinants": [str(x) for x in deltas],
        })
    return result


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: minimal_verifier.py instance.json")
    result = verify(Path(sys.argv[1]))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
