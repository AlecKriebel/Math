#!/usr/bin/env python3
"""Exact primary checks for the fixed-linear marked-double delta=2 leaf."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
a0, a1, a2 = sp.symbols("a0 a1 a2")
b0, b1, b2 = sp.symbols("b0 b1 b2")
c0, c1, c2, c3 = sp.symbols("c0 c1 c2 c3")
kappa, tau, lam, mu = sp.symbols("kappa tau lam mu")


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
                [sp.diff(value, variable) for variable in (p, q, r)]
                for value in (first, second, third)
            ]
        ).det()
    )


def coefficient_list(value: sp.Expr, degree: int) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(value), p, q)
    return [
        sp.factor(
            polynomial.coeff_monomial(p ** (degree - index) * q**index)
        )
        for index in range(degree + 1)
    ]


A = a0 * p**3 + a1 * p**2 * q + a2 * p * q**2
B = b0 * p**3 + b1 * p**2 * q + b2 * p * q**2 + q**3
P, Q = p * A, p * B

# The marked divisor has multiplicity two exactly when R is divisible by p^2.
R_general = c0 * p**3 + c1 * p**2 * q + c2 * p * q**2 + c3 * q**3
alpha_general = jac2(Q, R_general)
assert zero(sp.Poly(alpha_general, p).coeff_monomial(1) - 3 * c3 * q**5)
assert zero(
    sp.cancel(alpha_general.subs(c3, 0) / p).subs(p, 0) + c2 * q**4
)
print("PASS marked multiplicity-two normal form")


def data(R: sp.Expr):
    alpha = jac2(Q, R)
    beta = -jac2(P, R)
    gamma = jac2(P, Q)
    forms = (P, Q, R)
    first = tuple(sp.cancel(sp.diff(form, q) / p) for form in forms)
    second = tuple(
        sp.cancel(
            (
                sp.diff(form, p)
                - sp.Rational(1, 3) * q * first[index]
            )
            / p
        )
        for index, form in enumerate(forms)
    )
    assert all(
        not sp.denom(sp.cancel(value)).has(p, q)
        for value in first + second
    )
    for tangent in (first, second):
        assert zero(
            alpha * tangent[0]
            + beta * tangent[1]
            + gamma * tangent[2]
        )
    gradient = sp.Matrix(
        [
            [sp.diff(form, p), sp.diff(form, q)]
            for form in forms
        ]
    )
    basis = sp.Matrix.hstack(sp.Matrix(first), sp.Matrix(second))
    change = sp.Matrix([[sp.Rational(1, 3) * q, p], [p, 0]])
    assert all(zero(value) for value in gradient - basis * change)
    assert change.det() == -p**2

    tangent = tuple(
        sp.expand(kappa * first[index] + tau * second[index])
        for index in range(3)
    )
    curvature = sp.expand(
        jac3(P, r * tangent[1], r * tangent[2])
        + jac3(r * tangent[0], Q, r * tangent[2])
        + jac3(r * tangent[0], r * tangent[1], R)
    )
    K = sp.Poly(curvature, r).coeff_monomial(r)
    residual = sp.expand(K - lam * alpha - mu * beta)
    return alpha, beta, gamma, first, second, coefficient_list(residual, 5)


# R=p^2 q.
Rq = p**2 * q
alpha_q, beta_q, gamma_q, N1_q, N2_q, equations_q = data(Rq)
assert zero(equations_q[5] + sp.Rational(20, 9) * a2 * tau**2)
assert zero(
    equations_q[4]
    - sp.Rational(40, 3) * tau * (a1 * tau + a2 * kappa)
)

# On a2 != 0, tau=0.  The remaining contact conditions are C1=C0=0.
C1 = 40 * a0 * a2 + 5 * a1**2 + 4 * a1 * a2 * b2 - 4 * a2**2 * b1
C0 = 5 * a0 * a1 + 4 * a0 * a2 * b2 - 4 * a2**2 * b0
lam_q = sp.Rational(2, 5) * a2 * kappa**2
mu_q = (15 * a1 + 2 * a2 * b2) * kappa**2 / (5 * a2)
reduced_q = [
    sp.factor(
        sp.cancel(
            value.subs({tau: 0, lam: lam_q, mu: mu_q})
        )
    )
    for value in equations_q
]
assert zero(reduced_q[0] - 12 * kappa**2 * C0 / (5 * a2))
assert zero(reduced_q[1] - 3 * kappa**2 * C1 / (5 * a2))
assert all(zero(value) for value in reduced_q[2:])

b1_q = (40 * a0 * a2 + 5 * a1**2 + 4 * a1 * a2 * b2) / (
    4 * a2**2
)
b0_q = (5 * a0 * a1 + 4 * a0 * a2 * b2) / (4 * a2**2)
G = 4 * a0 * p**2 + a1 * p * q - 2 * a2 * q**2
factor_substitution_q = {b0: b0_q, b1: b1_q}
expected_q = (
    G * ((5 * a1 + 4 * a2 * b2) * p + 10 * a2 * q) / (4 * a2**2),
    -p * G,
    G * (10 * a0 * p**2 - 5 * a1 * p * q - 2 * a2 * q**2) / a2,
)
for actual, expected in zip((alpha_q, beta_q, gamma_q), expected_q):
    assert zero(
        sp.cancel(actual.subs(factor_substitution_q) / p**2) - expected
    )
assert sp.Poly(G, p, q).coeff_monomial(q**2) == -2 * a2
print("PASS R=p^2q generic contact routes to a quadratic extra gcd")

# The a2=0, a1!=0 boundary has only the zero tangent.
assert zero(
    equations_q[4].subs(a2, 0)
    - sp.Rational(40, 3) * a1 * tau**2
)
assert zero(equations_q[3].subs({a2: 0, tau: 0}) - 5 * lam)
assert zero(
    equations_q[2].subs({a2: 0, tau: 0, lam: 0})
    - 6 * a1 * kappa**2
)

# The totally ramified A=p^3 boundary has one contact family.
t = sp.symbols("t")
pure_contact = {
    a0: 1,
    a1: 0,
    a2: 0,
    b0: 0,
    b1: -sp.Rational(2, 75) * t**2,
    b2: t,
    kappa: -sp.Rational(2, 45) * t * tau,
    lam: -sp.Rational(28, 3) * tau**2,
    mu: -sp.Rational(64, 10125) * t**3 * tau**2,
}
assert all(zero(value.subs(pure_contact)) for value in equations_q)

P_pure = P.subs(pure_contact)
Q_pure = Q.subs(pure_contact)
R_pure = Rq
N1_pure = tuple(value.subs(pure_contact) for value in N1_q)
N2_pure = tuple(value.subs(pure_contact) for value in N2_q)
tangent_pure = tuple(
    sp.factor(
        tau
        * (
            N2_pure[index]
            - sp.Rational(2, 45) * t * N1_pure[index]
        )
    )
    for index in range(3)
)
X = sp.Rational(14, 3) * tau**2
Y = sp.Rational(32, 10125) * t**3 * tau**2
H4_top = sp.Matrix([P_pure, Q_pure, 0])
H3_top = sp.Matrix(
    [r * tangent_pure[0], r * tangent_pure[1], R_pure]
)
H2_top = sp.Matrix([X * r**2, Y * r**2, r * tangent_pure[2]])
top_determinant = sp.Poly(
    sp.expand(
        (
            z * H2_top.jacobian((p, q, r))
            + z**2 * H3_top.jacobian((p, q, r))
            + z**3 * H4_top.jacobian((p, q, r))
        ).det()
    ),
    z,
)
assert zero(top_determinant.coeff_monomial(z**7))
assert zero(top_determinant.coeff_monomial(z**6))
expected_E5_r2 = -sp.Rational(4, 30375) * tau**3 * (
    404 * p**3 * t**3
    + 3150 * p**2 * q * t**2
    - 27000 * p * q**2 * t
    - 118125 * q**3
)
assert zero(
    sp.Poly(top_determinant.coeff_monomial(z**5), r).coeff_monomial(r**2)
    - expected_E5_r2
)

# Retain every lower integration constant and verify literal independence
# of the decisive q^3 r^2 coefficient.
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
w = sp.symbols("w0:3")
xr0, xr1, yr0, yr1 = sp.symbols("xr0 xr1 yr0 yr1")
x = sp.symbols("x0:3")
y = sp.symbols("y0:3")
linear = sp.symbols("ell0:9")
binary_cubic = (p**3, p**2 * q, p * q**2, q**3)
binary_quadratic = (p**2, p * q, q**2)
U_full = r * tangent_pure[0] + sum(
    u[index] * binary_cubic[index] for index in range(4)
)
V_full = r * tangent_pure[1] + sum(
    v[index] * binary_cubic[index] for index in range(4)
)
W_full = r * tangent_pure[2] + sum(
    w[index] * binary_quadratic[index] for index in range(3)
)
A_full = (
    X * r**2
    + r * (xr0 * p + xr1 * q)
    + sum(x[index] * binary_quadratic[index] for index in range(3))
)
B_full = (
    Y * r**2
    + r * (yr0 * p + yr1 * q)
    + sum(y[index] * binary_quadratic[index] for index in range(3))
)
full_matrix = (
    sp.Matrix(3, 3, linear)
    + z * sp.Matrix([A_full, B_full, W_full]).jacobian((p, q, r))
    + z**2 * sp.Matrix([U_full, V_full, R_pure]).jacobian((p, q, r))
    + z**3 * H4_top.jacobian((p, q, r))
)
full_determinant = sp.Poly(sp.expand(full_matrix.det()), z, p, q, r)
assert zero(
    full_determinant.coeff_monomial(z**5 * q**3 * r**2)
    - sp.Rational(140, 9) * tau**3
)
print("PASS surviving R=p^2q contact has an unavoidable E5 obstruction")

# R=p^3.
R3 = p**3
alpha_3, beta_3, gamma_3, _, _, equations_3 = data(R3)
assert zero(equations_3[4] + 20 * a2 * tau**2)
assert zero(
    equations_3[3] + 8 * tau * (a1 * tau - 6 * a2 * kappa)
)

# If a2=0, all three minors already contain p^3.
for form in (alpha_3, beta_3, gamma_3):
    assert sp.denom(sp.cancel(form.subs(a2, 0) / p**3)) == 1

# On the exact a2!=0 open, tau=0 and nonzero contact forces C3=0.
lam_3 = 2 * a2 * kappa**2
mu_3 = (-3 * a1 + 2 * a2 * b2) * kappa**2 / a2
C3 = 3 * a1**2 - 4 * a1 * a2 * b2 + 4 * a2**2 * b1
reduced_3 = [
    sp.factor(
        sp.cancel(
            value.subs({tau: 0, lam: lam_3, mu: mu_3})
        )
    )
    for value in equations_3
]
assert zero(reduced_3[0] - 3 * kappa**2 * C3 / a2)
assert all(zero(value) for value in reduced_3[1:])

b1_3 = (4 * a1 * a2 * b2 - 3 * a1**2) / (4 * a2**2)
L = a1 * p + 2 * a2 * q
for form in (alpha_3, beta_3, gamma_3):
    quotient = sp.cancel(form.subs(b1, b1_3) / (p**2 * L))
    assert not sp.denom(quotient).has(p, q)
assert sp.Poly(L, p, q).coeff_monomial(q) == 2 * a2
print("PASS R=p^3 contact routes to an extra linear gcd")
print("ALL FIXED-LINEAR MARKED-DOUBLE DELTA2 SYMPY CHECKS PASSED")
