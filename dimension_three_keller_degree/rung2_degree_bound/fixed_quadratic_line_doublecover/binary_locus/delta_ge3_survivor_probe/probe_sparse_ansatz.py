#!/usr/bin/env python3
"""Probe the sparse quartic ansatz H3=(0,0,R), H2=0 exactly.

The script first solves E6 and E5 as a linear system in the nine entries of
the linear part.  It then tests whether the determinant survives on that
linear space and, when it does, prints the remaining E3/E2 equations.
"""

from __future__ import annotations

import sympy as sp

p, q, r, t = sp.symbols("p q r t")
ell = sp.symbols("l0:9")
coords = (p, q, r)
L = sp.Matrix(3, 3, ell)


def homogeneous_coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    ]


def analyze(label, h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + t**2 * sp.Matrix([0, 0, R]).jacobian(coords)
                + t**3 * sp.Matrix([P, Q, 0]).jacobian(coords)
            ).det()
        ),
        t,
    )
    equations = []
    for degree in (6, 5):
        equations.extend(homogeneous_coefficients(weighted.coeff_monomial(t**degree), degree))
    matrix, rhs = sp.linear_eq_to_matrix(equations, ell)
    assert rhs == sp.zeros(matrix.rows, 1)
    nullspace = matrix.nullspace()
    parameters = sp.symbols(f"{label}_s0:{len(nullspace)}")
    vector = sum(
        (parameter * basis for parameter, basis in zip(parameters, nullspace)),
        sp.zeros(9, 1),
    )
    Lnormal = sp.Matrix(3, 3, vector)
    det_normal = sp.factor(Lnormal.det())
    remaining = {}
    substitution = dict(zip(ell, vector))
    for degree in (3, 2):
        remaining[degree] = tuple(
            sp.factor(value.subs(substitution))
            for value in homogeneous_coefficients(weighted.coeff_monomial(t**degree), degree)
            if sp.expand(value.subs(substitution)) != 0
        )
    print(f"{label}: h={sp.factor(h)} R={sp.factor(R)}")
    print(f"  rank(E6,E5)={matrix.rank()} nullity={len(nullspace)}")
    print(f"  Lnormal={Lnormal}")
    print(f"  det(Lnormal)={det_normal}")
    print(f"  E3={remaining[3]}")
    print(f"  E2={remaining[2]}")
    return det_normal, remaining


def main():
    branches = (
        ("D3_P2_A", p**2, p**2 * (p + q)),
        ("D3_P2_B", p**2, p * (p**2 + q**2)),
        ("D3_PQ", p * q, p**3),
        ("D3_PELL_1", p * (p + q), p**3),
        ("D3_PELL_2", p * (p + q), p**2 * (p + q)),
        ("D4_DOUBLE_H", (p + q) ** 2, (p + q) ** 3),
        ("D4_DOUBLE_Q", (p + q) ** 2, 2 * p**3 + 3 * p**2 * q - q**3),
        ("D4_DOUBLE_P", (p + q) ** 2, p**3 - 3 * p * q**2 - 2 * q**3),
        ("D4_DOUBLE_MIX", (p + q) ** 2, 2 * p**3 + 3 * p**2 * q + 3 * p * q**2 + 2 * q**3),
    )
    for branch in branches:
        analyze(*branch)


if __name__ == "__main__":
    main()
