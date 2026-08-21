#!/usr/bin/env python3
"""Exact stabilizer and top-identity checks for the binary locus."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
variables = (p, q, r)
A, B, C, alpha, beta = sp.symbols(
    "A B C alpha beta", nonzero=True
)
h_general = A * p**2 + B * p * q + C * q**2


def exact_zero(value: sp.Expr) -> bool:
    return sp.cancel(sp.expand(value)) == 0


def jac2(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def jac3(f: sp.Expr, g: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [[sp.diff(entry, var) for var in variables]
             for entry in (f, g, h)]
        ).det()
    )


def homogeneous_monomials(degree: int) -> tuple[sp.Expr, ...]:
    return tuple(
        p**i * q**j * r ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def binary_coefficients(value: sp.Expr, degree: int) -> list[sp.Expr]:
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p**i * q ** (degree - i))
        for i in range(degree, -1, -1)
    ]


# The diagonal source action followed by target renormalization.
transformed_h = sp.expand(
    h_general.subs({p: alpha * p, q: beta * q}, simultaneous=True)
)
expected_h = (
    A * alpha**2 * p**2
    + B * alpha * beta * p * q
    + C * beta**2 * q**2
)
assert exact_zero(transformed_h - expected_h)
kappa = B**2 / (A * C)
kappa_transformed = (B * alpha * beta) ** 2 / (
    (A * alpha**2) * (C * beta**2)
)
assert exact_zero(kappa_transformed - kappa)
print("PASS stabilizer action and interior invariant")


# Full top determinant with general cubic pieces.
cubic = homogeneous_monomials(3)
quadratic = homogeneous_monomials(2)
uc = sp.symbols("u0:10")
vc = sp.symbols("v0:10")
rc = sp.symbols("s0:10")
tc = sp.symbols("t0:6")
U = sum(uc[i] * cubic[i] for i in range(10))
V = sum(vc[i] * cubic[i] for i in range(10))
Rraw = sum(rc[i] * cubic[i] for i in range(10))
T = sum(tc[i] * quadratic[i] for i in range(6))
P = h_general * p**2
Q = h_general * q**2
H4 = sp.Matrix([P, Q, 0])
H3raw = sp.Matrix([U, V, Rraw])
H2top = sp.Matrix([0, 0, T])
Lzero = sp.zeros(3)
weighted_raw = sp.Poly(
    sp.expand(
        (
            Lzero
            + z * H2top.jacobian(variables)
            + z**2 * H3raw.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
E8 = sp.expand(weighted_raw.coeff_monomial(z**8))
assert exact_zero(E8 - 8 * h_general**2 * p * q * sp.diff(Rraw, r))

Rbin = sum(rc[i] * p ** (3 - i) * q**i for i in range(4))
H3bin = sp.Matrix([U, V, Rbin])
weighted_bin = sp.Poly(
    sp.expand(
        (
            Lzero
            + z * H2top.jacobian(variables)
            + z**2 * H3bin.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
E7 = sp.expand(weighted_bin.coeff_monomial(z**7))
expected_E7 = (
    jac2(Q, Rbin) * sp.diff(U, r)
    - jac2(P, Rbin) * sp.diff(V, r)
    + 8 * h_general**2 * p * q * sp.diff(T, r)
)
assert exact_zero(E7 - expected_E7)
print("PASS exact E8 and E7 formulas from the full determinant")

# Universal signed E6 block identity.
d11, d12, d21, d22 = sp.symbols("d11 d12 d21 d22")
b11, b12, b21, b22 = sp.symbols("b11 b12 b21 b22")
a11, a12, a21, a22 = sp.symbols("a11 a12 a21 a22")
u1, u2b, v1b, v2b = sp.symbols("u1 u2b v1b v2b")
w1, w2, t1b, t2b, tau, ell33 = sp.symbols(
    "w1 w2 t1b t2b tau ell33"
)
Dblock = sp.Matrix([[d11, d12], [d21, d22]])
Bblock = sp.Matrix([[b11, b12], [b21, b22]])
Ablock = sp.Matrix([[a11, a12], [a21, a22]])
uvec = sp.Matrix([u1, u2b])
vvec = sp.Matrix([v1b, v2b])
wrow = sp.Matrix([[w1, w2]])
trow = sp.Matrix([[t1b, t2b]])
C3 = sp.Matrix([[d11, d12, 0], [d21, d22, 0], [0, 0, 0]])
B3 = sp.Matrix(
    [[b11, b12, u1], [b21, b22, u2b], [w1, w2, 0]]
)
A3 = sp.Matrix(
    [[a11, a12, v1b], [a21, a22, v2b], [t1b, t2b, tau]]
)
L3 = sp.diag(0, 0, ell33)
abstract_weighted = sp.Poly(
    sp.expand((L3 + z * A3 + z**2 * B3 + z**3 * C3).det()), z
)
abstract_E6 = abstract_weighted.coeff_monomial(z**6)
expected_abstract_E6 = (
    Dblock.det() * ell33
    + sp.trace(Bblock.adjugate() * Dblock) * tau
    - (wrow * Dblock.adjugate() * vvec)[0]
    - (trow * Dblock.adjugate() * uvec)[0]
    - (wrow * Bblock.adjugate() * uvec)[0]
)
assert exact_zero(abstract_E6 - expected_abstract_E6)
print("PASS universal signed E6 block identity")


u2, v2 = sp.symbols("u2 v2")
u1p, u1q, v1p, v1q, t1 = sp.symbols(
    "u1p u1q v1p v1q t1"
)
u0p, u0m, u0q, v0p, v0m, v0q, t0p, t0q = sp.symbols(
    "u0p u0m u0q v0p v0m v0q t0p t0q"
)
Ur = u2 * r**2 + r * (u1p * p + u1q * q) + (
    u0p * p**2 + u0m * p * q + u0q * q**2
)
Vr = v2 * r**2 + r * (v1p * p + v1q * q) + (
    v0p * p**2 + v0m * p * q + v0q * q**2
)
Tr = t1 * r + t0p * p + t0q * q
split_variables = (
    (u2, v2),
    (u1p, u1q, v1p, v1q, t1),
    (u0p, u0m, u0q, v0p, v0m, v0q, t0p, t0q),
)


def split_ranks(h: sp.Expr, R: sp.Expr) -> tuple[int, int, int]:
    p4 = sp.expand(h * p**2)
    q4 = sp.expand(h * q**2)
    equation = sp.expand(
        jac2(q4, R) * Ur
        - jac2(p4, R) * Vr
        + jac2(p4, q4) * Tr
    )
    ranks: list[int] = []
    for power, unknowns in zip((2, 1, 0), split_variables):
        coefficient = sp.Poly(equation, r).coeff_monomial(r**power)
        rows = binary_coefficients(coefficient, 7 - power)
        matrix, rhs = sp.linear_eq_to_matrix(rows, unknowns)
        assert rhs == sp.zeros(len(rows), 1)
        ranks.append(matrix.rank())
    return tuple(ranks)


samples = (
    (p * q, p**3 + q**3, (2, 5, 8), "two branch roots, transverse"),
    (
        p * (p + q),
        p**3 + p**2 * q + q**3,
        (2, 5, 8),
        "one branch root, transverse",
    ),
    (
        p**2 + q**2,
        p**3 + 2 * p**2 * q + 3 * p * q**2 + 4 * q**3,
        (2, 5, 8),
        "interior squarefree, transverse",
    ),
    (
        p**2 + q**2,
        p**3 + p**2 * q + q**3,
        (2, 5, 7),
        "interior transverse special splitting",
    ),
    (
        p**2 + q**2,
        p**3 + q**3,
        (2, 5, 6),
        "interior transverse symmetric splitting",
    ),
    (
        p**2,
        p**3 + p**2 * q + p * q**2 + q**3,
        (2, 5, 7),
        "doubled branch root",
    ),
    (
        (p + q) ** 2,
        p**3 + p**2 * q + p * q**2 + 2 * q**3,
        (2, 5, 7),
        "doubled nonbranch root",
    ),
)
for h_sample, r_sample, expected, label in samples:
    actual = split_ranks(h_sample, r_sample)
    assert actual == expected, (label, actual, expected)
    print(f"PASS E7 split {label}: ranks {actual}")

# This boundary is excluded before applying the Hilbert--Burch and
# power-fibre tables: its ranks do not belong to either table.
assert split_ranks(p * q, 0) == (0, 1, 2)
print("PASS R=0 boundary kept separate from the power fibre")

# A concrete E8/E7/E6 survivor on the exceptional power fibre.  Its lower
# E3 coefficient is nonzero, so it is explicitly not called a Keller map.
H4_witness = sp.Matrix([p**4, p**2 * q**2, 0])
H3_witness = sp.Matrix([0, 0, p**3])
H2_witness = sp.zeros(3, 1)
L_witness = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
witness_weighted = sp.Poly(
    sp.expand(
        (
            L_witness
            + z * H2_witness.jacobian(variables)
            + z**2 * H3_witness.jacobian(variables)
            + z**3 * H4_witness.jacobian(variables)
        ).det()
    ),
    z,
)
assert L_witness.det() == -1
for degree in (8, 7, 6):
    assert exact_zero(witness_weighted.coeff_monomial(z**degree))
assert exact_zero(witness_weighted.coeff_monomial(z**3) + 4 * p**3)
assert not exact_zero(witness_weighted.coeff_monomial(z**3))
print("PASS explicit top-three survivor, rejected at E3")

print("ALL BINARY FIXED-QUADRATIC ORBIT/TOP CHECKS PASSED")
