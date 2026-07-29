#!/usr/bin/env python3
"""Exhaust all balanced generalized-Bell-diagonal reflections at d=4.

All 12,870 sign tables are checked.  Arithmetic is over the Gaussian
integers after clearing the Fourier denominators, so there is no numerical
tolerance.  A direct 64-by-64 SymPy matrix replay independently calibrates
the coefficient formula and its tensor ordering on one sign table.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterable

import sympy as sp


D = 4
I_POWERS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def gadd(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] - right[0], left[1] - right[1]


def gscale(value: tuple[int, int], scalar: int) -> tuple[int, int]:
    return scalar * value[0], scalar * value[1]


def gmul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gproduct(values: Iterable[tuple[int, int]]) -> tuple[int, int]:
    out = (1, 0)
    for value in values:
        out = gmul(out, value)
    return out


def row_fourier(row: tuple[int, int, int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (
            sum(row[b] * I_POWERS[(b * t) % D][0] for b in range(D)),
            sum(row[b] * I_POWERS[(b * t) % D][1] for b in range(D)),
        )
        for t in range(D)
    )


ROW_FOURIER = {
    row: row_fourier(row)
    for row in itertools.product((-1, 1), repeat=D)
}


def unnormalized_residual(
    fourier: tuple[tuple[tuple[int, int], ...], ...],
    a: int,
    c: int,
    p: int,
    r: int,
) -> tuple[int, int]:
    """Return 192 times one residual coefficient.

    The input is |0,a,a+c> and the output is
    |r,r+a+p,a+c+p>.  Each pair coefficient has denominator 4, so the
    cubic has denominator 64.  Multiplication by 192 clears both that
    denominator and the factor 1/3 on the linear term.
    """

    left = (0, 0)
    for t in range(D):
        left = gadd(
            left,
            gproduct(
                (
                    fourier[a][t],
                    fourier[(c - t) % D][p],
                    fourier[(a + p) % D][(r - t) % D],
                )
            ),
        )

    right = (0, 0)
    for u in range(D):
        right = gadd(
            right,
            gproduct(
                (
                    fourier[c][u],
                    fourier[(a + u) % D][r],
                    fourier[(c - r) % D][(p - u) % D],
                )
            ),
        )

    linear = (0, 0)
    if p == 0:
        linear = gadd(linear, fourier[a][r])
    if r == 0:
        linear = gsub(linear, fourier[c][p])
    return gsub(gscale(gsub(left, right), 3), gscale(linear, 16))


def table_fourier(signs: tuple[int, ...]):
    rows = tuple(
        tuple(signs[a * D + b] for b in range(D)) for a in range(D)
    )
    return tuple(ROW_FOURIER[row] for row in rows)


def satisfies_cubic(signs: tuple[int, ...]) -> bool:
    fourier = table_fourier(signs)
    return all(
        unnormalized_residual(fourier, a, c, p, r) == (0, 0)
        for a in range(D)
        for c in range(D)
        for p in range(D)
        for r in range(D)
    )


def direct_matrix_calibration() -> None:
    """Compare all reduced coefficients with a direct tensor matrix."""

    # Exercise every shift and Fourier orientation: all four rows are
    # nonconstant and every one of their Fourier modes is nonzero.
    signs = (
        1, 1, 1, -1,
        1, 1, -1, 1,
        1, -1, -1, -1,
        -1, 1, -1, -1,
    )
    fourier = table_fourier(signs)
    assert sum(signs) == 0
    assert all(value != (0, 0) for row in fourier for value in row)

    h = sp.zeros(D * D)
    imaginary = sp.I
    for a in range(D):
        for x in range(D):
            for t in range(D):
                y = (x + a) % D
                target_x = (x + t) % D
                target_y = (target_x + a) % D
                gaussian = fourier[a][t]
                h[target_x * D + target_y, x * D + y] = (
                    gaussian[0] + imaginary * gaussian[1]
                ) / D

    assert h.conjugate().T == h
    assert h * h == sp.eye(D * D)
    identity = sp.eye(D)
    h1 = sp.kronecker_product(h, identity)
    h2 = sp.kronecker_product(identity, h)
    residual = (
        h1 * h2 * h1
        - h2 * h1 * h2
        - sp.Rational(1, 3) * (h1 - h2)
    )

    represented = {}
    for a in range(D):
        for c in range(D):
            source = a * D + (a + c) % D
            for p in range(D):
                for r in range(D):
                    target = (
                        r * D * D
                        + ((r + a + p) % D) * D
                        + (a + c + p) % D
                    )
                    gaussian = unnormalized_residual(
                        fourier, a, c, p, r
                    )
                    expected = (
                        gaussian[0] + imaginary * gaussian[1]
                    ) / 192
                    assert sp.simplify(residual[target, source] - expected) == 0
                    represented[(target, source)] = expected

    for target in range(D**3):
        for source in range(D**3):
            source_x = source // (D * D)
            if source_x != 0:
                # Global translation gives the same reduced coefficient.
                x = source_x
                shifted_source = tuple(
                    (coordinate - x) % D
                    for coordinate in (
                        source // (D * D),
                        (source // D) % D,
                        source % D,
                    )
                )
                shifted_target = tuple(
                    (coordinate - x) % D
                    for coordinate in (
                        target // (D * D),
                        (target // D) % D,
                        target % D,
                    )
                )
                reduced_source = (
                    shifted_source[0] * D * D
                    + shifted_source[1] * D
                    + shifted_source[2]
                )
                reduced_target = (
                    shifted_target[0] * D * D
                    + shifted_target[1] * D
                    + shifted_target[2]
                )
                expected = represented.get((reduced_target, reduced_source), 0)
            else:
                expected = represented.get((target, source), 0)
            assert sp.simplify(residual[target, source] - expected) == 0


def exhaustive_search() -> tuple[int, int]:
    checked = 0
    solutions = 0
    for negative_positions in itertools.combinations(range(D * D), D * D // 2):
        signs = [1] * (D * D)
        for index in negative_positions:
            signs[index] = -1
        checked += 1
        solutions += satisfies_cubic(tuple(signs))
    return checked, solutions


def main() -> None:
    direct_matrix_calibration()
    print("[ok] direct 64x64 matrix calibration of all reduced coefficients")
    checked, solutions = exhaustive_search()
    assert checked == 12870
    assert solutions == 0
    print(f"[ok] balanced d=4 Bell sign tables checked exactly: {checked}")
    print(f"[ok] exceptional cubic solutions found: {solutions}")
    print("[scope] fixed generalized Bell basis of the stated Weyl pair")
    print("d=4 Bell-diagonal exhaustive verifier: PASS")


if __name__ == "__main__":
    main()
