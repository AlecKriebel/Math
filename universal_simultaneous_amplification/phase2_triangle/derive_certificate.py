#!/usr/bin/env python3
"""Independent exact derivation for complete-support weighted triangles.

This script does not import ``src.exact_markov``.  It builds the six transient
dB equations directly from the update definition, solves them over
``QQ(r,x,y)``, and verifies the invariant factorization and sign-certificate
identities used in ``triangle_classification.md``.
"""

from __future__ import annotations

from itertools import permutations
from typing import Sequence, Tuple

import sympy as sp


r = sp.symbols("r", positive=True)
x, y = sp.symbols("x y", positive=True)
a, b, c = sp.symbols("a b c", positive=True)


def build_six_state_system(
    weights: Sequence[Sequence[sp.Expr]],
) -> Tuple[sp.Matrix, sp.Matrix]:
    """Return the state-change system for (F1,F2,F3,G1,G2,G3).

    ``Fi`` is fixation probability from the singleton mutant at vertex ``i``.
    ``Gi`` is fixation probability when vertex ``i`` is the unique resident.
    Every equation has been multiplied by three.  Self transitions are omitted.
    """

    matrix = sp.zeros(6, 6)
    rhs = sp.zeros(6, 1)

    # Singleton Fi.  Its death has scaled probability 1 and leads to extinction.
    # If resident j dies, mutant i wins against the third vertex k with the
    # displayed scaled probability and the resulting doubleton is Gk.
    for i in range(3):
        matrix[i, i] = 1
        for j in range(3):
            if j == i:
                continue
            k = 3 - i - j
            gain = sp.cancel(r * weights[i][j] / (r * weights[i][j] + weights[j][k]))
            matrix[i, i] += gain
            matrix[i, 3 + k] -= gain

    # Doubleton Gi.  Death of resident i has scaled probability 1 and fixes.
    # If mutant j dies, resident i can replace it, leaving singleton k.
    for i in range(3):
        j, k = [vertex for vertex in range(3) if vertex != i]
        lose_j = sp.cancel(weights[i][j] / (r * weights[j][k] + weights[i][j]))
        lose_k = sp.cancel(weights[i][k] / (r * weights[j][k] + weights[i][k]))
        row = 3 + i
        matrix[row, row] = 1 + lose_j + lose_k
        matrix[row, k] -= lose_j
        matrix[row, j] -= lose_k
        rhs[row, 0] = 1

    return matrix, rhs


def elementary(edge_a: sp.Expr, edge_b: sp.Expr, edge_c: sp.Expr):
    s1 = edge_a + edge_b + edge_c
    s2 = edge_a * edge_b + edge_a * edge_c + edge_b * edge_c
    s3 = edge_a * edge_b * edge_c
    return s1, s2, s3


def sign_polynomials(edge_a: sp.Expr, edge_b: sp.Expr, edge_c: sp.Expr):
    """Return A,D,E,H from the proof certificate."""

    s1, s2, s3 = elementary(edge_a, edge_b, edge_c)
    A = 3 * s3 * (s1 * s2 - 9 * s3)
    D = 12 * s1**3 * s3 - 45 * s1 * s2 * s3 + 4 * s2**3 - 27 * s3**2
    E = 4 * s2 * (3 * s1**2 * s2 - 3 * s1 * s3 - 8 * s2**2)
    H = sp.expand(A * (r - 1) ** 4 + D * r * (r - 1) ** 2 + E * r**2)
    return tuple(map(sp.expand, (A, D, E, H)))


def denominator_polynomial(edge_a: sp.Expr, edge_b: sp.Expr, edge_c: sp.Expr):
    """Return the homogeneous symmetric polynomial P in the exact denominator."""

    s1, s2, s3 = elementary(edge_a, edge_b, edge_c)
    coefficient_5 = 12 * s1 * s2 * s3 - 36 * s3**2
    coefficient_4 = (
        12 * s1**3 * s3
        - 56 * s1 * s2 * s3
        + 12 * s2**3
        + 72 * s3**2
    )
    coefficient_3 = (
        -24 * s1**3 * s3
        + 12 * s1**2 * s2**2
        + 80 * s1 * s2 * s3
        - 24 * s2**3
        - 90 * s3**2
    )
    return sp.expand(
        9 * s3**2 * (r**6 + 1)
        + coefficient_5 * (r**5 + r)
        + coefficient_4 * (r**4 + r**2)
        + coefficient_3 * r**3
    )


def formula_difference(edge_a: sp.Expr, edge_b: sp.Expr, edge_c: sp.Expr):
    """Return rho_dB(weighted triangle)-rho_dB(K3)."""

    _, _, _, H = sign_polynomials(edge_a, edge_b, edge_c)
    P = denominator_polynomial(edge_a, edge_b, edge_c)
    return sp.cancel(-r * (r - 1) * H / (3 * (r + 1) * P))


def local_denominator_product(edge_a: sp.Expr, edge_b: sp.Expr, edge_c: sp.Expr):
    edges = (edge_a, edge_b, edge_c)
    return sp.prod(r * edges[i] + edges[j] for i, j in permutations(range(3), 2))


def verify_sum_of_squares_identities() -> None:
    s1, s2, s3 = elementary(a, b, c)
    X, Y, Z = a * b, a * c, b * c

    square_gap_1 = sp.Rational(1, 2) * (
        (a - b) ** 2 + (a - c) ** 2 + (b - c) ** 2
    )
    square_gap_2 = sp.Rational(1, 2) * (
        (X - Y) ** 2 + (X - Z) ** 2 + (Y - Z) ** 2
    )
    weighted_gap = c * (a - b) ** 2 + b * (a - c) ** 2 + a * (b - c) ** 2
    cubic_gap = (
        s2 * square_gap_2
        + 3 * (Z * (X - Y) ** 2 + Y * (X - Z) ** 2 + X * (Y - Z) ** 2)
    )

    assert sp.expand(s1**2 - 3 * s2 - square_gap_1) == 0
    assert sp.expand(s2**2 - 3 * s1 * s3 - square_gap_2) == 0
    assert sp.expand(s1 * s2 - 9 * s3 - weighted_gap) == 0
    assert sp.expand(s2**3 - 27 * s3**2 - cubic_gap) == 0

    A, D, E, _ = sign_polynomials(a, b, c)
    D_certificate = (
        12 * s1 * s3 * (s1**2 - 3 * s2)
        + 3 * s2 * (s2**2 - 3 * s1 * s3)
        + (s2**3 - 27 * s3**2)
    )
    E_certificate = 4 * s2 * (
        3 * s2 * (s1**2 - 3 * s2) + (s2**2 - 3 * s1 * s3)
    )
    assert sp.expand(A - 3 * s3 * weighted_gap) == 0
    assert sp.expand(D - D_certificate) == 0
    assert sp.expand(E - E_certificate) == 0


def main() -> None:
    # Scale invariance lets us normalize w_12=1, w_13=x, w_23=y.
    normalized_weights = ((0, 1, x), (1, 0, y), (x, y, 0))
    matrix, rhs = build_six_state_system(normalized_weights)

    # Strict diagonal dominance is encoded by M*1=1: every diagonal entry is
    # one plus the sum of the magnitudes of the nonpositive off-diagonal entries.
    assert matrix * sp.ones(6, 1) == sp.ones(6, 1)

    solution = matrix.inv(method="DM") * rhs
    rho = sp.cancel(sum(solution[index, 0] for index in range(3)) / 3)
    baseline = sp.cancel(2 * r / (3 * (r + 1)))
    derived_difference = sp.cancel(rho - baseline)
    certified_difference = formula_difference(1, x, y)
    assert sp.cancel(derived_difference - certified_difference) == 0

    # P is positive because it is a positive local-denominator product times
    # one third of the determinant of a strictly diagonally dominant M-matrix.
    generic_weights = ((0, a, b), (a, 0, c), (b, c, 0))
    generic_matrix, _ = build_six_state_system(generic_weights)
    determinant = sp.cancel(generic_matrix.det(method="domain-ge"))
    P = denominator_polynomial(a, b, c)
    local_product = local_denominator_product(a, b, c)
    assert sp.cancel(determinant - 3 * P / local_product) == 0

    A, D, E, H = sign_polynomials(a, b, c)
    assert sp.expand(H - (A * (r - 1) ** 4 + D * r * (r - 1) ** 2 + E * r**2)) == 0
    verify_sum_of_squares_identities()

    assert sp.expand(H.subs({a: 1, b: 1, c: 1})) == 0
    assert sp.factor(P.subs({a: 1, b: 1, c: 1})) == 9 * (r + 1) ** 2 * (r**2 + 3 * r + 1) ** 2

    print("[EXACTLY COMPUTED] solved all six transient dB equations over QQ(r,x,y)")
    print("[CERTIFIED IDENTITY] rho-rho_K3 = -r(r-1)H/[3(r+1)P]")
    print("[CERTIFIED IDENTITY] H = A(r-1)^4 + D*r(r-1)^2 + E*r^2")
    print("[CERTIFIED POSITIVITY] P = local_product*det(M)/3 > 0")
    print("[CERTIFIED SOS] A,D,E are nonnegative; E is strict off a=b=c")
    print("[PROVED] every nonuniform positive weighted triangle is a strict dB suppressor for r>1")


if __name__ == "__main__":
    main()
