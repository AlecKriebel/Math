#!/usr/bin/python3
"""Exact compatibility checks for the scalar-aligned nodal-cubic stratum.

The fixed linear divisor is

    h = p + k q,

so k=0 is a node preimage and k != 0 is an arbitrary smooth marked point
in this affine normalization chart.  The calculation deliberately keeps k
symbolic; checking only k=-1 would not control the marked-point modulus.
"""

from __future__ import annotations

import sympy as sp

p, q, r, book, k = sp.symbols("p q r book k")
alpha, beta = sp.symbols("alpha beta")
variables = (p, q, r)

A = sp.Matrix([p**2 * q, p * q**2, p**3 + q**3])
Ap = A.diff(p)
Aq = A.diff(q)
Delta = Ap.cross(Aq)
h = p + k * q
H4 = h * A

v_symbols = sp.symbols("v0:12")
binary_cubic_monomials = (p**3, p**2 * q, p * q**2, q**3)
V = sp.Matrix(
    [
        sum(v_symbols[4 * i + j] * binary_cubic_monomials[j]
            for j in range(4))
        for i in range(3)
    ]
)

w_symbols = sp.symbols("w0:18")
quadratic_monomials = (p**2, p * q, q**2, p * r, q * r, r**2)
H2 = sp.Matrix(
    [
        sum(w_symbols[6 * i + j] * quadratic_monomials[j]
            for j in range(6))
        for i in range(3)
    ]
)

H3 = V + r * (alpha * Ap + beta * Aq)
unknowns = (*v_symbols, *w_symbols)


def jacobian_map(H: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [[sp.diff(H[i], variable) for variable in variables] for i in range(3)]
    )


weighted = (
    book * jacobian_map(H2)
    + book**2 * jacobian_map(H3)
    + book**3 * jacobian_map(H4)
)
degree_seven = sp.Poly(sp.expand(weighted.det()), book).coeff_monomial(book**7)
poly_seven = sp.Poly(sp.expand(degree_seven), p, q, r)
equations = [coefficient for _, coefficient in poly_seven.terms()]
matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)

print(f"symbolic marked-point matrix shape: {matrix.shape}")
print(f"symbolic marked-point generic rank: {matrix.rank()}")

left_kernel = matrix.T.nullspace()
compatibility = [sp.factor((vector.T * rhs)[0]) for vector in left_kernel]
expected_left_kernel = [
    sp.Matrix(
        [0, 0, -2 * (2 * k**3 - 1), 0, 3 * k**2, 0, -2 * k, 0, 1,
         0, 0, 0, 0, 0, 0]
    ),
    sp.Matrix(
        [0, 0, -3 * k * (k - 1) * (k**2 + k + 1), 0,
         (4 * k**3 + 1) / 2, 0, -k**2, 0, 0, 0, 1, 0, 0, 0, 0]
    ),
    sp.Matrix([0, 0, 0, 0, k, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
    sp.Matrix(
        [0, 0, -k**3, 0, k**2 / 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ),
]
expected_compatibility = [
    -8 * (
        alpha**2 * k
        + 2 * alpha * beta * k**2
        + beta**2 * k**3
        - 3 * beta**2
    ),
    -4 * (
        2 * alpha**2 * k**2
        + 4 * alpha * beta * k**3
        + 6 * alpha * beta
        + 2 * beta**2 * k**4
        - 9 * beta**2 * k
    ),
    8 * (alpha**2 - 4 * alpha * beta * k + beta**2 * k**2),
    -4 * k * (-2 * alpha**2 + 2 * alpha * beta * k + beta**2 * k**2),
]
assert len(left_kernel) == len(expected_left_kernel)
assert all(
    all(sp.expand(actual[j] - expected[j]) == 0 for j in range(actual.rows))
    for actual, expected in zip(left_kernel, expected_left_kernel)
)
assert all(
    sp.expand(actual - expected) == 0
    for actual, expected in zip(compatibility, expected_compatibility)
)
print("symbolic compatibility generators:")
for polynomial in compatibility:
    print(sp.factor(polynomial))

# If beta=0, the third compatibility equation gives alpha=0.  If beta is
# nonzero, set T=alpha/beta.  The four exact compatibility equations have
# no common point for any marked-point parameter k.
T = sp.symbols("T")
projective_compatibility = [
    sp.expand(item.subs({alpha: T, beta: 1}))
    for item in expected_compatibility
]
projective_basis = sp.groebner(
    projective_compatibility, T, k, order="lex"
).polys
assert [item.as_expr() for item in projective_basis] == [sp.Integer(1)]

# The top Jacobian normal has the expected universal scalar.
expected_normal = sp.Rational(4, 3) * h**2 * Delta
assert all(
    sp.expand(value) == 0
    for value in (H4.diff(p).cross(H4.diff(q)) - expected_normal)
)

# Sample regressions retained for the two initially discovered points.
for sample, expected_rank, expected_groebner in (
    (0, 11, [alpha**2, alpha * beta, beta**2]),
    (-1, 11, [alpha**2, alpha * beta, beta**2]),
):
    sample_matrix = matrix.subs(k, sample)
    sample_rhs = rhs.subs(k, sample)
    assert sample_matrix.rank() == expected_rank
    sample_compatibility = [
        sp.factor((vector.T * sample_rhs)[0])
        for vector in sample_matrix.T.nullspace()
    ]
    basis = sp.groebner(sample_compatibility, alpha, beta).polys
    normalized_basis = [sp.Poly(item, alpha, beta).as_expr() for item in basis]
    assert normalized_basis == expected_groebner

# Once alpha=beta=0, H3 is binary.  The complete degree-seven coefficient
# is the top normal paired with dH2/dr.
binary_H3 = V
binary_weighted = (
    book * jacobian_map(H2)
    + book**2 * jacobian_map(binary_H3)
    + book**3 * jacobian_map(H4)
)
binary_degree_seven = sp.Poly(
    sp.expand(binary_weighted.det()), book
).coeff_monomial(book**7)
expected_binary_degree_seven = expected_normal.dot(H2.diff(r))
assert sp.expand(binary_degree_seven - expected_binary_degree_seven) == 0

# Delta has no syzygy with linear coefficients.  This is the degree-one
# instance of its Hilbert--Burch resolution, checked here from raw
# coefficients over C[p,q,r].
z_symbols = sp.symbols("z0:12")
linear_monomials = (p, q, r, 1)
linear_vector = sp.Matrix(
    [
        sum(z_symbols[4 * i + j] * linear_monomials[j] for j in range(4))
        for i in range(3)
    ]
)
syzygy_equations = [
    coefficient
    for _, coefficient in sp.Poly(
        sp.expand(Delta.dot(linear_vector)), p, q, r
    ).terms()
]
syzygy_matrix, syzygy_rhs = sp.linear_eq_to_matrix(
    syzygy_equations, z_symbols
)
assert syzygy_rhs == sp.zeros(syzygy_matrix.rows, 1)
assert syzygy_matrix.rank() == len(z_symbols)

print("scalar-aligned nodal symbolic SymPy checks passed")
