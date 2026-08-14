#!/usr/bin/env python3
"""Independent exact stress tests for the diagonal-damping theorem.

The bounded census uses a small exact Fraction determinant implementation rather
than a CAS call per minor.  This keeps the replay practical while preserving
exact arithmetic.  Numerical eigenvalues are secondary corroboration only.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

Matrix = tuple[tuple[Fraction, ...], ...]


def as_fraction_matrix(rows: Sequence[Sequence[int | Fraction]]) -> Matrix:
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def determinant(matrix: Matrix) -> Fraction:
    """Exact determinant, specialized for the sizes used most often."""
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    work = [list(row) for row in matrix]
    sign = 1
    det = Fraction(1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            sign *= -1
        pivot_value = work[col][col]
        det *= pivot_value
        for row in range(col + 1, n):
            if work[row][col] == 0:
                continue
            factor = work[row][col] / pivot_value
            for j in range(col + 1, n):
                work[row][j] -= factor * work[col][j]
            work[row][col] = Fraction(0)
    return det if sign > 0 else -det


def principal_submatrix(matrix: Matrix, subset: tuple[int, ...]) -> Matrix:
    return tuple(tuple(matrix[i][j] for j in subset) for i in subset)


def principal_signed_minor(matrix: Matrix, subset: tuple[int, ...]) -> Fraction:
    value = determinant(principal_submatrix(matrix, subset))
    return value if len(subset) % 2 == 0 else -value


def all_signed_minors(matrix: Matrix) -> dict[tuple[int, ...], Fraction]:
    n = len(matrix)
    return {
        subset: principal_signed_minor(matrix, subset)
        for r in range(n + 1)
        for subset in itertools.combinations(range(n), r)
    }


def diagonal_minus_matrix(matrix: Matrix, diagonal: tuple[Fraction, ...]) -> Matrix:
    n = len(matrix)
    return tuple(
        tuple((diagonal[i] if i == j else Fraction(0)) - matrix[i][j] for j in range(n))
        for i in range(n)
    )


def expansion_value_from_coeffs(
    coeffs: dict[tuple[int, ...], Fraction],
    diagonal: tuple[Fraction, ...],
) -> Fraction:
    n = len(diagonal)
    total = Fraction(0)
    for subset, coefficient in coeffs.items():
        chosen = set(subset)
        monomial = Fraction(1)
        for j in range(n):
            if j not in chosen:
                monomial *= diagonal[j]
        total += coefficient * monomial
    return total


def multiscale_diagonal(
    matrix: Matrix,
    witness_subset: tuple[int, ...],
    max_doublings: int = 80,
) -> tuple[tuple[Fraction, ...], int, Fraction]:
    n = len(matrix)
    selected = set(witness_subset)
    if principal_signed_minor(matrix, witness_subset) >= 0:
        raise ValueError("selected subset is not a negative signed minor")
    t = 2
    for _ in range(max_doublings):
        diagonal = tuple(Fraction(t) if j not in selected else Fraction(1, t) for j in range(n))
        value = determinant(diagonal_minus_matrix(matrix, diagonal))
        if value < 0:
            return diagonal, t, value
        t *= 2
    raise AssertionError("multiscale construction failed to isolate a negative coefficient")


def positive_root_numeric(matrix: Matrix, diagonal: tuple[Fraction, ...]) -> float:
    shifted = np.array(
        [[float(matrix[i][j] - (diagonal[i] if i == j else 0)) for j in range(len(matrix))]
         for i in range(len(matrix))],
        dtype=float,
    )
    eig = np.linalg.eigvals(shifted)
    candidates = [float(z.real) for z in eig if abs(z.imag) < 1e-8 and z.real > 1e-10]
    if not candidates:
        # Exact negativity at zero already proves a positive root.  Do not turn a
        # numerical conditioning issue into a mathematical failure.
        return float("nan")
    return max(candidates)


def check_matrix(matrix: Matrix, check_numeric_root: bool = True) -> dict[str, object]:
    n = len(matrix)
    coeffs = all_signed_minors(matrix)
    diagonals = [
        tuple(Fraction(j + 2, j + 1) for j in range(n)),
        tuple(Fraction(2 * j + 3, j + 2) for j in range(n)),
    ]
    for diagonal in diagonals:
        direct = determinant(diagonal_minus_matrix(matrix, diagonal))
        expanded = expansion_value_from_coeffs(coeffs, diagonal)
        if direct != expanded:
            raise AssertionError({"matrix": matrix, "diagonal": diagonal, "direct": direct, "expanded": expanded})

    negatives = [subset for subset, value in coeffs.items() if value < 0]
    report: dict[str, object] = {"dimension": n, "negative_count": len(negatives)}
    if negatives:
        diagonal, t, value = multiscale_diagonal(matrix, negatives[0])
        report.update({"witness_subset": list(negatives[0]), "t": t, "determinant": str(value)})
        if check_numeric_root:
            root = positive_root_numeric(matrix, diagonal)
            if np.isfinite(root):
                report["positive_root"] = root
    else:
        for diagonal in diagonals:
            for lam in (Fraction(1, 7), Fraction(1), Fraction(5)):
                shifted = tuple(x + lam for x in diagonal)
                if expansion_value_from_coeffs(coeffs, shifted) <= 0:
                    raise AssertionError("nonnegative coefficients produced a nonpositive characteristic value")
    return report


def bounded_matrices() -> Iterable[Matrix]:
    for n, values in ((1, range(-4, 5)), (2, range(-2, 3)), (3, (-1, 0, 1))):
        for entries in itertools.product(values, repeat=n * n):
            yield tuple(
                tuple(Fraction(entries[i * n + j]) for j in range(n))
                for i in range(n)
            )


def random_rational_matrix(rng: random.Random, n: int) -> Matrix:
    return tuple(
        tuple(Fraction(rng.randint(-9, 9), rng.randint(1, 7)) for _ in range(n))
        for _ in range(n)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=20260813)
    parser.add_argument("--skip-exhaustive", action="store_true")
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    exhaustive = 0
    exhaustive_negative = 0
    max_t = 0
    if not args.skip_exhaustive:
        for matrix in bounded_matrices():
            report = check_matrix(matrix, check_numeric_root=False)
            exhaustive += 1
            if report["negative_count"]:
                exhaustive_negative += 1
                max_t = max(max_t, int(report["t"]))
                if len(matrix) <= 2:
                    for subset, value in all_signed_minors(matrix).items():
                        if value < 0:
                            _, t, _ = multiscale_diagonal(matrix, subset)
                            max_t = max(max_t, t)

    rng = random.Random(args.seed)
    random_negative = 0
    numerical_roots = 0
    numerical_attempts = 0
    for index in range(args.random):
        n = rng.choice((2, 3, 4, 5))
        matrix = random_rational_matrix(rng, n)
        report = check_matrix(matrix, check_numeric_root=(index < 500))
        if report["negative_count"]:
            random_negative += 1
            max_t = max(max_t, int(report["t"]))
            if index < 500:
                numerical_attempts += 1
                if "positive_root" in report:
                    numerical_roots += 1

    summary = {
        "status": "PASS",
        "exhaustive_matrices": exhaustive,
        "exhaustive_with_negative_signed_minor": exhaustive_negative,
        "random_rational_matrices": args.random,
        "random_seed": args.seed,
        "random_with_negative_signed_minor": random_negative,
        "numerical_root_attempts": numerical_attempts,
        "numerically_confirmed_positive_roots": numerical_roots,
        "maximum_multiscale_t": max_t,
        "counterexample_found": False,
        "scope": "all 1x1 entries [-4,4], all 2x2 entries [-2,2], all 3x3 entries {-1,0,1}, plus random rationals",
    }
    rendered = json.dumps(summary, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
