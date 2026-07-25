#!/usr/bin/python3
"""Exact checks for WORKING_CUSPIDAL_CUBIC_CURVE_EXIT.md."""

from __future__ import annotations

import sympy as sp

p, q, r, scale = sp.symbols("p q r scale")
lam, alpha, beta, gamma, eta = sp.symbols(
    "lambda alpha beta gamma eta"
)
u, v, w, kappa, rho = sp.symbols("u v w kappa rho")
variables = (p, q, r)


def jacobian_map(H: sp.Matrix) -> sp.Matrix:
    return H.jacobian(variables)


def theta(H: sp.Matrix) -> sp.Matrix:
    return -p * H.diff(p) - q * H.diff(q) + 3 * r * H.diff(r)


A = sp.Matrix([p**2 * q, p**3, q**3])
Ap = A.diff(p)
Aq = A.diff(q)
S = sp.Matrix([2 * q, 3 * p, 0])
T = sp.Matrix([p**2, 0, 3 * q**2])
N = sp.Matrix([3 * p * q**2, -2 * q**3, -p**3])
Delta = Ap.cross(Aq)

assert Delta == 3 * p * N
assert S.cross(T) == 3 * N
assert Ap == p * S
assert Aq == T

H4 = r * A
kernel_vector = sp.Matrix([-p, -q, 3 * r])
expected_adjugate = r * kernel_vector * Delta.T / 3
assert jacobian_map(H4).adjugate() == expected_adjugate

# Complete degree-eight syzygy family.
qa, qb, qc, la, lb, ma, mb = sp.symbols(
    "qa qb qc la lb ma mb"
)
Q = qa * p**2 + qb * p * q + qc * q**2
ell = la * p + lb * q
m = ma * p + mb * q
H3_degree_eight = S * (Q + r * ell + eta * r**2) + T * (m + beta * r)
assert sp.expand(N.dot(theta(H3_degree_eight))) == 0

# The H2-independent r=0 obstruction.
a0, b0, c0, d0, e0 = sp.symbols("a0 b0 c0 d0 e0")
Q0 = a0 * p**2 + b0 * p * q + c0 * q**2
m0 = d0 * p + e0 * q
V0 = Q0 * S + m0 * T
normal_minor = sp.factor(
    sp.Matrix.hstack(V0.diff(p), V0.diff(q), A).det()
)
expected_minor = -18 * q * (
    d0 * p**3
    + (e0 - a0) * p**2 * q
    - b0 * p * q**2
    - c0 * q**3
) ** 2
assert sp.expand(normal_minor - expected_minor) == 0

# Raw degree-seven system after V=lambda*A, but before its compatibility
# conditions have been imposed.
H3_pre = (
    lam * A
    + r * ((alpha * p + gamma * q) * S + beta * T)
    + eta * r**2 * S
)
quadratic_monomials = [p**2, p * q, p * r, q**2, q * r, r**2]
c = sp.symbols("c0:18")
H2_general = sp.Matrix(
    [
        sum(c[6 * component + j] * quadratic_monomials[j]
            for j in range(6))
        for component in range(3)
    ]
)
degree_seven_raw = sp.Poly(
    sp.expand(
        (
            scale * jacobian_map(H2_general)
            + scale**2 * jacobian_map(H3_pre)
            + scale**3 * jacobian_map(H4)
        ).det()
    ),
    scale,
).coeff_monomial(scale**7)
poly7 = sp.Poly(degree_seven_raw, p, q, r)
expected_monomials7 = [
    (6, 0, 1),
    (5, 1, 1),
    (5, 0, 2),
    (4, 2, 1),
    (4, 1, 2),
    (4, 0, 3),
    (3, 3, 1),
    (3, 2, 2),
    (2, 4, 1),
    (2, 3, 2),
    (2, 2, 3),
    (1, 5, 1),
    (1, 4, 2),
    (1, 3, 3),
    (0, 5, 2),
    (0, 4, 3),
    (0, 3, 4),
]
assert poly7.monoms() == expected_monomials7
matrix7, rhs7 = sp.linear_eq_to_matrix(poly7.coeffs(), c)

expected_matrix7 = sp.zeros(17, 18)
for row, entries in {
    0: [(12, 2)],
    1: [(13, 2)],
    2: [(14, -2)],
    3: [(0, -6), (15, 2)],
    4: [(16, -2)],
    5: [(17, -6)],
    6: [(1, -6), (6, 4)],
    7: [(2, 6)],
    8: [(3, -6), (7, 4)],
    9: [(4, 6), (8, -4)],
    10: [(5, 18)],
    11: [(9, 4)],
    12: [(10, -4)],
    13: [(11, -12)],
}.items():
    for column, entry in entries:
        expected_matrix7[row, column] = entry

assert matrix7 == expected_matrix7
assert matrix7.rank() == 14
assert matrix7.row_join(rhs7).rank() == 15

expected_left_kernel = []
for row in (14, 15, 16):
    vector = sp.zeros(17, 1)
    vector[row] = 1
    expected_left_kernel.append(vector)
left_kernel = matrix7.T.nullspace()
assert left_kernel == expected_left_kernel
compatibility = [
    sp.factor((vector.T * rhs7)[0]) for vector in left_kernel
]
assert compatibility == [
    -6 * gamma**2,
    -36 * eta * gamma,
    -30 * eta**2,
]

# The full four-parameter H2 family after gamma=eta=0.
D2A = (
    alpha**2 * A.diff(p, 2)
    + 2 * alpha * beta * A.diff(p).diff(q)
    + beta**2 * A.diff(q, 2)
)
H3 = lam * A + r * (alpha * Ap + beta * Aq)
H2 = (
    (u * Ap + v * Aq) / 3
    + r * D2A / 2
    + (w * q + kappa * r) * S / 3
)
degree_seven = sp.Poly(
    sp.expand(
        (
            scale * jacobian_map(H2)
            + scale**2 * jacobian_map(H3)
            + scale**3 * jacobian_map(H4)
        ).det()
    ),
    scale,
).coeff_monomial(scale**7)
assert sp.expand(degree_seven) == 0

coefficient_vector = []
for component in H2:
    polynomial = sp.Poly(component, p, q, r)
    coefficient_vector.extend(
        polynomial.coeff_monomial(monomial)
        for monomial in quadratic_monomials
    )
parameter_jacobian = sp.Matrix(coefficient_vector).jacobian((u, v, w, kappa))
assert parameter_jacobian.rank() == 4

# Raw degree-six system with a completely arbitrary linear part.
l = sp.symbols("l0:9")
L_general = sp.Matrix(3, 3, l)
weighted_general = (
    L_general
    + scale * jacobian_map(H2)
    + scale**2 * jacobian_map(H3)
    + scale**3 * jacobian_map(H4)
)
degree_six_raw = sp.Poly(
    sp.expand(weighted_general.det()), scale
).coeff_monomial(scale**6)
poly6 = sp.Poly(degree_six_raw, p, q, r)
expected_monomials6 = [
    (5, 0, 1),
    (4, 1, 1),
    (4, 0, 2),
    (3, 2, 1),
    (2, 3, 1),
    (2, 2, 2),
    (1, 4, 1),
    (1, 3, 2),
]
assert poly6.monoms() == expected_monomials6
matrix6, rhs6 = sp.linear_eq_to_matrix(poly6.coeffs(), l)
expected_matrix6 = sp.Matrix(
    [
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -3],
        [-3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -3, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, -6, 0, 0, 0],
    ]
)
expected_rhs6 = sp.Matrix(
    [
        0,
        beta * (-3 * beta * lam + 2 * v),
        -3 * beta**3,
        -2 * (-3 * alpha * beta * lam + alpha * v + beta * u),
        -3 * alpha**2 * lam + 2 * alpha * u - 2 * beta * w,
        3 * beta * (3 * alpha**2 + 2 * kappa),
        2 * alpha * w,
        -6 * alpha * (alpha**2 + kappa),
    ]
)
assert matrix6 == expected_matrix6
assert all(
    sp.expand(actual - expected) == 0
    for actual, expected in zip(rhs6, expected_rhs6)
)
assert matrix6.rank() == 8
assert matrix6.row_join(rhs6).rank() == 8

L0 = sp.Matrix(
    [
        [
            2 * (-3 * alpha * beta * lam + alpha * v + beta * u) / 3,
            (
                3 * alpha**2 * lam
                - 2 * alpha * u
                + 2 * beta * w
                + 2 * rho
            )
            / 3,
            beta * (3 * alpha**2 + 2 * kappa) / 3,
        ],
        [rho, alpha * w, alpha * (alpha**2 + kappa)],
        [0, beta * (-3 * beta * lam + 2 * v), beta**3],
    ]
)
assert all(
    sp.expand(entry) == 0
    for entry in matrix6 * sp.Matrix(list(L0)) - rhs6
)

weighted = (
    L0
    + scale * jacobian_map(H2)
    + scale**2 * jacobian_map(H3)
    + scale**3 * jacobian_map(H4)
)
determinant = sp.Poly(sp.expand(weighted.det()), scale)
for degree in (8, 7, 6):
    assert sp.expand(determinant.coeff_monomial(scale**degree)) == 0

X = (
    (v - 3 * beta * lam) * p**2
    + (3 * alpha * lam - u) * p * q
    - w * q**2
)
expected_five = -sp.Rational(4, 3) * q * (
    X - kappa * q * r
) * (X + kappa * q * r)
assert sp.expand(
    determinant.coeff_monomial(scale**5) - expected_five
) == 0

# The degree-five compatibility specialization and all surviving lower
# coefficients.
final_substitution = {
    kappa: 0,
    w: 0,
    u: 3 * alpha * lam,
    v: 3 * beta * lam,
}
final_determinant = sp.Poly(
    sp.expand(determinant.as_expr().subs(final_substitution)), scale
)
for degree in (8, 7, 6, 5, 4):
    assert sp.expand(
        final_determinant.coeff_monomial(scale**degree)
    ) == 0

square = (rho - 3 * alpha**2 * lam) ** 2
expected_lower = {
    3: -sp.Rational(2, 3) * q**3 * square,
    2: -2 * beta * q**2 * square,
    1: -2 * beta**2 * q * square,
    0: -sp.Rational(2, 3) * beta**3 * square,
}
for degree, expected in expected_lower.items():
    assert sp.expand(
        final_determinant.coeff_monomial(scale**degree) - expected
    ) == 0

print("cuspidal cubic-stratum exit SymPy checks passed")
