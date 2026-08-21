#!/usr/bin/env python3
"""Exact checks for the fixed-linear mixed-divisor {1,1} delta=2 leaf."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
a, b, c = sp.symbols("a b c")
x, y, lam, mu = sp.symbols("x y lam mu")
variables = (p, q, r)


def zero(value: sp.Expr) -> bool:
    return sp.cancel(sp.expand(value)) == 0


def jac2(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def jac3(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in variables]
                for value in (first, second, third)
            ]
        ).det()
    )


def contact_data(P: sp.Expr, Q: sp.Expr, R: sp.Expr):
    alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
    first = tuple(sp.cancel(sp.diff(form, q) / p) for form in (P, Q, R))
    direction = lambda form: sp.diff(form, q) - sp.Rational(1, 4) * sp.diff(
        form, p
    )
    second = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
    for tangent in (first, second):
        assert zero(
            alpha * tangent[0]
            + beta * tangent[1]
            + gamma * tangent[2]
        )
    gradient = sp.Matrix(
        [
            [sp.diff(form, p), sp.diff(form, q)]
            for form in (P, Q, R)
        ]
    )
    basis = sp.Matrix.hstack(sp.Matrix(first), sp.Matrix(second))
    change = sp.Matrix([[4 * p, p], [-4 * q, 0]])
    assert all(zero(value) for value in gradient - basis * change)
    assert change.det() == 4 * p * q

    tangent = tuple(
        sp.expand(x * first[index] + y * second[index])
        for index in range(3)
    )
    curvature = sp.expand(
        jac3(P, r * tangent[1], r * tangent[2])
        + jac3(r * tangent[0], Q, r * tangent[2])
        + jac3(r * tangent[0], r * tangent[1], R)
    )
    residual = sp.Poly(
        sp.expand(
            sp.Poly(curvature, r).coeff_monomial(r)
            - lam * alpha
            - mu * beta
        ),
        p,
        q,
    )
    equations = [
        sp.factor(
            residual.coeff_monomial(p ** (5 - index) * q**index)
        )
        for index in range(6)
    ]
    return alpha, beta, gamma, first, second, tangent, equations


def lifted_matrix(equations: list[sp.Expr]) -> sp.Matrix:
    xx, xy, yy = sp.symbols("xx xy yy")
    lifted = [
        sp.expand(value).subs({x**2: xx, x * y: xy, y**2: yy})
        for value in equations
    ]
    matrix, rhs = sp.linear_eq_to_matrix(
        lifted, (xx, xy, yy, lam, mu)
    )
    assert rhs == sp.zeros(len(equations), 1)
    return matrix


# First endpoint chart: a3=0, normalized to A=pq^2 and
# B=p^3+p^2q+q^3.
P1 = p**2 * q**2
Q1 = p * (p**3 + p**2 * q + q**3)
R1 = p * (c * p**2 + sp.Rational(3, 4) * c * p * q + q**2)
_, _, _, _, _, _, equations_one = contact_data(P1, Q1, R1)
assert zero(equations_one[0] + sp.Rational(3, 8) * y**2 * (49 * c - 16))

gb_one_y0 = sp.groebner(
    [value.subs({y: 0, x: 1}) for value in equations_one],
    lam,
    mu,
    c,
    order="lex",
)
assert gb_one_y0.polys[0].as_expr() == 1

matrix_one = lifted_matrix(equations_one)
special_one = matrix_one.subs(c, sp.Rational(16, 49))
assert special_one.rank() == 4
kernel_one = special_one.nullspace()
assert len(kernel_one) == 1
expected_kernel_one = sp.Matrix(
    [
        -sp.Rational(6, 419),
        -sp.Rational(141, 838),
        sp.Rational(4, 419),
        -sp.Rational(35, 419),
        1,
    ]
)
assert all(zero(value) for value in kernel_one[0] - expected_kernel_one)
assert (
    sp.factor(
        kernel_one[0][1] ** 2
        - kernel_one[0][0] * kernel_one[0][2]
    )
    == sp.Rational(19977, 702244)
)
print("PASS first endpoint chart has no projective contact")


# Second endpoint chart: a3=1,b3=0.
A = q**2 * (a * p + q)
B = p**3 + p**2 * q + b * p * q**2
P, Q = p * A, p * B
R = p * (c * p**2 + sp.Rational(3, 4) * c * p * q + q**2)
alpha, beta, gamma, Np, Nq, tangent, equations = contact_data(P, Q, R)
for form in (alpha, beta, gamma):
    assert not sp.denom(sp.cancel(form / (p * q))).has(p, q)
print("PASS mixed {1,1} Hilbert--Burch tangent")


# The y=0 projective chart has exactly two components.
y_zero = [
    sp.together(value.subs({y: 0, x: 1})).as_numer_denom()[0]
    for value in equations
]
gb_y_zero = sp.groebner(y_zero, lam, mu, a, b, c, order="lex")
expected_last = (6 * b * c - 72 * b + 7) * (
    9 * b * c**2 - 48 * b * c - 6 * c + 16
)
assert zero(gb_y_zero.polys[-1].as_expr() - expected_last)

b_first = sp.Rational(7, 6) / (12 - c)
a_first = 9 * (c - 8) * (c - 4) / (2 * (c - 12))
lam_first = -9 * c * (c - 4) / (c - 12)
mu_first = 7 / (c - 12)
branch_first = {
    a: a_first,
    b: b_first,
    lam: lam_first,
    mu: mu_first,
    x: 1,
    y: 0,
}
assert all(zero(value.subs(branch_first)) for value in equations)
line_first = 3 * (c - 8) * p - q
for form in (alpha, beta, gamma):
    quotient = sp.cancel(form.subs(branch_first) / (p * q * line_first))
    assert not sp.denom(quotient).has(p, q)

b_second = 2 * (3 * c - 8) / (3 * c * (3 * c - 16))
a_second = 9 * c * (3 * c**2 - 128) / (
    8 * (3 * c - 16) * (3 * c - 8)
)
lam_second = -9 * c * (3 * c**2 - 64 * c + 128) / (
    4 * (3 * c - 16) * (3 * c - 8)
)
mu_second = -4 * (3 * c - 8) / (c * (3 * c - 16))
branch_second = {
    a: a_second,
    b: b_second,
    lam: lam_second,
    mu: mu_second,
    x: 1,
    y: 0,
}
assert all(zero(value.subs(branch_second)) for value in equations)
quadratic_second = (
    27 * c**3 * p**2
    + 144 * c**2 * p * q
    - 1152 * c * p**2
    - 864 * c * p * q
    + 48 * c * q**2
    - 128 * q**2
)
for form in (alpha, beta, gamma):
    quotient = sp.cancel(
        form.subs(branch_second) / (p * q * quadratic_second)
    )
    assert not sp.denom(quotient).has(p, q)
assert sp.Poly(quadratic_second, p, q).total_degree() == 2

# The only denominator of the second component not excluded directly by
# its defining factor is c=8/3,b=0; it has no contact.
gb_second_endpoint = sp.groebner(
    [
        value.subs(
            {
                y: 0,
                x: 1,
                c: sp.Rational(8, 3),
                b: 0,
            }
        )
        for value in equations
    ],
    lam,
    mu,
    a,
    order="lex",
)
assert gb_second_endpoint.polys[0].as_expr() == 1
print("PASS y=0 contact components both have larger gcd")


# On y!=0 put y=1.  The first coefficient gives H=0.
H = a * c - 16 * a - 48 * b * c + 6 * c + 64
assert zero(equations[0] + sp.Rational(3, 8) * y**2 * H)
asol = sp.cancel((48 * b * c - 6 * c - 64) / (c - 16))
D = 24 * b * c - 3 * c - 32
G = (
    15 * b * c**3
    - 288 * b * c**2
    + 1536 * b * c
    - 2048 * b
    - 8 * c**2
    + 176 * c
    - 768
)
V = (
    408 * b**2 * c**2
    - 6528 * b**2 * c
    + 27648 * b**2
    - 171 * b * c**2
    + 2768 * b * c
    - 12032 * b
    + 18 * c**2
    - 296 * c
    + 1328
)

matrix = lifted_matrix(equations).subs(a, asol)
rows = [1, 2, 3, 4]
columns = [0, 1, 3, 4]
square = matrix.extract(rows, columns)
assert zero(
    square.det(method="domain-ge")
    + D**2 * G / (16 * (c - 16) ** 2)
)

xx_value = 3 * (4 * b - 1) * (c - 16) / (16 * D)
xy_value = 3 * (24 * b - 5) * (c - 8) / (4 * D)
lam_value = (24 * b - 5) * (
    84 * b * c**2
    - 576 * b * c
    - 33 * c**2
    + 464 * c
    - 1536
) / (4 * (c - 16) * D)
mu_value = b * (42 * b * c - 288 * b - 9 * c + 64) / (4 * D)
kernel = sp.Matrix([xx_value, xy_value, 1, lam_value, mu_value])
assert all(zero(value) for value in matrix * kernel)
assert zero(
    xy_value**2
    - xx_value
    - sp.Rational(3, 4) * V / D**2
)
print("PASS y!=0 contact is the exact curve V=0 on the generic chart")


# D=0 or G=0 creates an extra common factor, so neither belongs to exact
# delta=2.
b_D = (3 * c + 32) / (24 * c)
a_D = sp.factor(asol.subs(b, b_D))
assert a_D == 0
for form in (alpha, beta, gamma):
    quotient = sp.cancel(form.subs({a: a_D, b: b_D}) / (p * q**2))
    assert not sp.denom(quotient).has(p, q)

K = 15 * c**3 - 288 * c**2 + 1536 * c - 2048
N = 8 * c**2 - 176 * c + 768
assert sp.resultant(K, N, c) == 2**23 * 5**2
b_G = sp.cancel(N / K)
a_G = sp.cancel(asol.subs(b, b_G))
line_G = (
    15 * c**2 * p
    - 192 * c * p
    + 4 * c * q
    + 512 * p
    - 64 * q
)
for form in (alpha, beta, gamma):
    quotient = sp.cancel(
        form.subs({a: a_G, b: b_G}) / (p * q * line_G)
    )
    assert not sp.denom(quotient).has(p, q)
print("PASS both generic rank-drop divisors route to higher gcd")


# The r^2 coefficient of E5 uses only the displayed top contact data.
# Verify this before any specialization while retaining every possible
# lower integration constant.
u_full = sp.symbols("u_full0:4")
v_full = sp.symbols("v_full0:4")
w_full = sp.symbols("w_full0:3")
aa_full = sp.symbols("aa_full0:3")
bb_full = sp.symbols("bb_full0:3")
xp_full, xq_full, yp_full, yq_full = sp.symbols(
    "xp_full xq_full yp_full yq_full"
)
ell_full = sp.symbols("ell_full0:9")
binary_cubic = (p**3, p**2 * q, p * q**2, q**3)
binary_quadratic = (p**2, p * q, q**2)
U0_full = sum(
    u_full[index] * binary_cubic[index] for index in range(4)
)
V0_full = sum(
    v_full[index] * binary_cubic[index] for index in range(4)
)
T0_full = sum(
    w_full[index] * binary_quadratic[index] for index in range(3)
)
A0_full = sum(
    aa_full[index] * binary_quadratic[index] for index in range(3)
)
B0_full = sum(
    bb_full[index] * binary_quadratic[index] for index in range(3)
)
H4_full = sp.Matrix((P, Q, 0))
H3_full = sp.Matrix(
    (
        U0_full + r * tangent[0],
        V0_full + r * tangent[1],
        R,
    )
)
H2_full = sp.Matrix(
    (
        A0_full
        + r * (xp_full * p + xq_full * q)
        - lam * r**2 / 2,
        B0_full
        + r * (yp_full * p + yq_full * q)
        - mu * r**2 / 2,
        T0_full + r * tangent[2],
    )
)
L_full = sp.Matrix(3, 3, ell_full)
full_determinant = sp.Poly(
    sp.expand(
        (
            L_full
            + z * H2_full.jacobian(variables)
            + z**2 * H3_full.jacobian(variables)
            + z**3 * H4_full.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
bare_H3 = sp.Matrix((r * tangent[0], r * tangent[1], R))
bare_H2 = sp.Matrix((-lam * r**2 / 2, -mu * r**2 / 2, r * tangent[2]))
bare_determinant = sp.Poly(
    sp.expand(
        (
            z * bare_H2.jacobian(variables)
            + z**2 * bare_H3.jacobian(variables)
            + z**3 * H4_full.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
for index in range(4):
    monomial = z**5 * p ** (3 - index) * q**index * r**2
    assert zero(
        full_determinant.coeff_monomial(monomial)
        - bare_determinant.coeff_monomial(monomial)
    )

x_value = xy_value
top_substitution = {
    a: asol,
    x: x_value,
    y: 1,
    lam: lam_value,
    mu: mu_value,
}
S = tuple(sp.factor(value.subs(top_substitution)) for value in tangent)
H4 = sp.Matrix((P.subs(a, asol), Q, 0))
H3 = sp.Matrix((r * S[0], r * S[1], R))
H2 = sp.Matrix((-lam_value * r**2 / 2, -mu_value * r**2 / 2, r * S[2]))
top_determinant = sp.Poly(
    sp.expand(
        (
            z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
obstruction_numerators = []
for index in range(4):
    coefficient = sp.cancel(
        top_determinant.coeff_monomial(
            z**5 * p ** (3 - index) * q**index * r**2
        )
    )
    obstruction_numerators.append(
        sp.factor(coefficient.as_numer_denom()[0])
    )

resultant_zero = sp.factor(
    sp.resultant(V, obstruction_numerators[0], b)
)
resultant_one = sp.factor(
    sp.resultant(V, obstruction_numerators[1], b)
)
expected_zero = (
    2687385600
    * (c - 16) ** 6
    * (c - 8) ** 6
    * (57 * c**2 - 960 * c + 4096)
)
expected_one = (
    2902376448
    * (c - 16) ** 8
    * (c - 8) ** 6
    * (
        11925 * c**4
        - 398990 * c**3
        + 5022128 * c**2
        - 28184576 * c
        + 59506688
    )
)
assert zero(resultant_zero - expected_zero)
assert zero(resultant_one - expected_one)
residual_zero = 57 * c**2 - 960 * c + 4096
residual_one = (
    11925 * c**4
    - 398990 * c**3
    + 5022128 * c**2
    - 28184576 * c
    + 59506688
)
assert sp.resultant(residual_zero, residual_one, c) == 20654497726464
assert zero(V.subs(c, 8) - 16 * (4 * b - 1) * (24 * b - 7))
assert D.subs({b: sp.Rational(7, 24), c: 8}) == 0
assert G.subs({b: sp.Rational(1, 4), c: 8}) == 0
print("PASS generic contact curve has an unavoidable E5 obstruction")


# The c=16 endpoint is not covered by solving H for a.
c16 = {b: sp.Rational(5, 24), c: 16, y: 1}
equations_16 = [sp.factor(value.subs(c16)) for value in equations]
gb_16 = sp.groebner(equations_16, x, lam, mu, a, order="lex")
Q_a = 9 * a**2 - 68 * a + 144
assert gb_16.reduce(a * Q_a)[1] == 0

# a=0 has an additional q in the gcd.
for form in (alpha, beta, gamma):
    quotient = sp.cancel(
        form.subs({a: 0, b: sp.Rational(5, 24), c: 16}) / (p * q**2)
    )
    assert not sp.denom(quotient).has(p, q)

x_16 = (9 * a - 32) / 96
lam_16 = -(19 * a - 64) / 32
mu_16 = 15 * a / 1024 - sp.Rational(15, 256)
endpoint_contact = {
    b: sp.Rational(5, 24),
    c: 16,
    y: 1,
    x: x_16,
    lam: lam_16,
    mu: mu_16,
}
for value in equations:
    numerator = sp.cancel(value.subs(endpoint_contact)).as_numer_denom()[0]
    assert sp.rem(sp.Poly(numerator, a), sp.Poly(Q_a, a)).is_zero

S16 = tuple(sp.factor(value.subs(endpoint_contact)) for value in tangent)
H4_16 = sp.Matrix(
    (
        P.subs({b: sp.Rational(5, 24), c: 16}),
        Q.subs({b: sp.Rational(5, 24), c: 16}),
        0,
    )
)
H3_16 = sp.Matrix(
    (
        r * S16[0],
        r * S16[1],
        R.subs({b: sp.Rational(5, 24), c: 16}),
    )
)
H2_16 = sp.Matrix(
    (-lam_16 * r**2 / 2, -mu_16 * r**2 / 2, r * S16[2])
)
determinant_16 = sp.Poly(
    sp.expand(
        (
            z * H2_16.jacobian(variables)
            + z**2 * H3_16.jacobian(variables)
            + z**3 * H4_16.jacobian(variables)
        ).det()
    ),
    z,
    p,
    q,
    r,
)
coefficient_16 = determinant_16.coeff_monomial(z**5 * p**3 * r**2)
remainder_16 = sp.rem(
    sp.Poly(sp.expand(coefficient_16), a), sp.Poly(Q_a, a)
).as_expr()
assert zero(remainder_16 - sp.Rational(5, 16) * (3 * a - 10))
assert sp.resultant(Q_a, 3 * a - 10, a) == 156
print("PASS c=16 endpoint is higher-gcd or obstructed at E5")

print("ALL FIXED-LINEAR MIXED {1,1} DELTA2 SYMPY CHECKS PASSED")
