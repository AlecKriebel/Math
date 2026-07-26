#!/usr/bin/env python3
"""Scratch computation for the D4-DN-2C E7/E6 contact atlas.

This file is exploratory.  The certificate will be rebuilt separately after
the contact charts and specialization loci have been frozen.
"""

from __future__ import annotations

import sympy as sp

p, q, r, w = sp.symbols("p q r w")
source = (p, q, r)


def bracket(f, g):
    return sp.expand(
        sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p)
    )


def determinant(P, Q, R, U, V, T, A, B, L):
    H2 = sp.Matrix((A, B, T))
    H3 = sp.Matrix((U, V, R))
    H4 = sp.Matrix((P, Q, 0))
    return sp.Poly(
        sp.expand(
            (
                L
                + w * H2.jacobian(source)
                + w**2 * H3.jacobian(source)
                + w**3 * H4.jacobian(source)
            ).det()
        ),
        w,
    )


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))

alpha = bracket(Q, R)
beta = -bracket(P, R)
gamma = bracket(P, Q)
common = sp.gcd(sp.gcd(alpha, beta), gamma)
reduced_contact = tuple(sp.factor(item / common) for item in (alpha, beta, gamma))

# Kernel coordinates are derived directly from
# alpha*d_r(U)+beta*d_r(V)+gamma*d_r(T)=0.
d, z, x, y, a, b = sp.symbols("d z x y a b")
U2 = (d + sp.Rational(4, 3) * z) * p + (
    2 * d + sp.Rational(4, 3) * z
) * q
V2 = d * q
T2 = z
U1 = (x + sp.Rational(4, 3) * a) * p**2 + (
    y + 2 * x + sp.Rational(4, 3) * (a + b)
) * p * q + (2 * y + sp.Rational(4, 3) * b) * q**2
V1 = x * p * q + y * q**2
T1 = a * p + b * q

assert sp.expand(
    reduced_contact[0] * U2
    + reduced_contact[1] * V2
    + reduced_contact[2] * T2
) == 0
assert sp.expand(
    reduced_contact[0] * U1
    + reduced_contact[1] * V1
    + reduced_contact[2] * T1
) == 0

# All lower coefficients which can enter E6 are retained.
binary3 = (p**3, p**2 * q, p * q**2, q**3)
binary2 = (p**2, p * q, q**2)
ternary2 = (p**2, p * q, p * r, q**2, q * r, r**2)
uc = sp.symbols("uc0:4")
vc = sp.symbols("vc0:4")
tc = sp.symbols("tc0:3")
ac = sp.symbols("ac0:6")
bc = sp.symbols("bc0:6")
ell = sp.symbols("ell0:9")
U0 = sum(c * m for c, m in zip(uc, binary3))
V0 = sum(c * m for c, m in zip(vc, binary3))
T0 = sum(c * m for c, m in zip(tc, binary2))
A = sum(c * m for c, m in zip(ac, ternary2))
B = sum(c * m for c, m in zip(bc, ternary2))
L = sp.Matrix(3, 3, ell)

lower18 = (
    ac[2],
    ac[4],
    ac[5],
    bc[2],
    bc[4],
    bc[5],
    ell[8],
) + uc + vc + tc

full = determinant(
    P,
    Q,
    R,
    U0 + r * U1 + r**2 * U2,
    V0 + r * V1 + r**2 * V2,
    T0 + r * T1 + r**2 * T2,
    A,
    B,
    L,
)
E6 = sp.Poly(full.coeff_monomial(w**6), p, q, r)


def greedy_independent_indices(matrix):
    rows = []
    columns = []
    rank = 0
    for row in range(matrix.rows):
        for column in range(matrix.cols):
            candidate_rows = rows + [row]
            candidate_columns = columns + [column]
            minor = matrix.extract(candidate_rows, candidate_columns)
            if minor.det() != 0:
                rows = candidate_rows
                columns = candidate_columns
                rank += 1
                break
    return tuple(rows), tuple(columns), rank


def main():
    print("alpha,beta,gamma", alpha, beta, gamma)
    print("reduced", reduced_contact)
    print("E6 monomials", E6.monoms())

    # E6 at r-degree three is independent of all lower coefficients.
    top = tuple(
        (monomial, sp.factor(coefficient))
        for monomial, coefficient in E6.terms()
        if monomial[2] == 3
    )
    print("E6 r3", top)

    E6_dz0 = sp.Poly(E6.as_expr().subs({d: 0, z: 0}), p, q, r)
    equations = E6_dz0.coeffs()
    matrix, rhs = sp.linear_eq_to_matrix(equations, lower18)
    print("full shape", matrix.shape)

    eta = sp.sqrt(-2)
    k, s = sp.symbols("k s")
    plane = {
        a: k,
        b: -sp.Rational(3, 2) * s,
        y: s,
        x: (-(4 + 2 * eta) * k + (3 - 3 * eta) * s) / 9,
    }
    plane_matrix = matrix.subs(plane)
    plane_rhs = rhs.subs(plane)
    sample = plane_matrix.subs({k: 1, s: 0})
    sample_augmented = sample.row_join(plane_rhs.subs({k: 1, s: 0}))
    print("sample ranks", sample.rank(), sample_augmented.rank())
    _, pivcols = sample.rref()
    independent_rows = tuple(
        index
        for index in range(sample.rows)
        if index
        in sp.Matrix(sample.T).rref()[1]
    )
    rank = sample.rank()
    rows = independent_rows[:rank]
    cols = tuple(pivcols[:rank])
    pivot = sp.factor(
        plane_matrix.extract(rows, cols).det(), extension=eta
    )
    print("candidate rows", rows)
    print("candidate cols", cols)
    print("candidate pivot", pivot)

    print("origin ranks", matrix.subs({a: 0, b: 0, x: 0, y: 0}).rank(),
          matrix.subs({a: 0, b: 0, x: 0, y: 0}).row_join(
              rhs.subs({a: 0, b: 0, x: 0, y: 0})
          ).rank())


if __name__ == "__main__":
    main()
