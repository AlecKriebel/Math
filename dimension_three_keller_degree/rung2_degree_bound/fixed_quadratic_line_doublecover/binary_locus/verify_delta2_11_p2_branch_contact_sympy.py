#!/usr/bin/env python3
"""Exact exclusion of the h=p^2, q-contact, exact-delta=2 {1,1} row."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, C, D = sp.symbols("A C D")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


def jac(first, second):
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def binary(coefficients_, degree):
    return sum(
        coefficients_[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


def contact_matrix(P, Q, R, N1, N2):
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
    for tangent in (N1, N2):
        assert zero(
            alpha * tangent[0]
            + beta * tangent[1]
            + gamma * tangent[2]
        )
    N = tuple(
        sp.expand(s * N1[index] + t * N2[index])
        for index in range(3)
    )
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([r * N[0], r * N[1], R])
    H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * N[2]])
    determinant = sp.Poly(
        sp.expand(
            (
                z * H2.jacobian(variables)
                + z**2 * H3.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    assert zero(determinant.coeff_monomial(z**7))
    E6r = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**6)), r
    ).coeff_monomial(r)
    lifted = []
    for equation in coefficients(E6r, 5):
        poly = sp.Poly(equation, s, t)
        lifted.append(
            sp.expand(
                poly.coeff_monomial(s**2) * X
                + poly.coeff_monomial(s * t) * Y
                + poly.coeff_monomial(t**2) * Z
                + poly.coeff_monomial(1)
            )
        )
    return sp.Matrix(
        [
            [
                equation.coeff(variable)
                for variable in (X, Y, Z, x5, y5)
            ]
            for equation in lifted
        ]
    )


P, Q = p**4, p**2 * q**2
R = A * p**3 + C * p * q**2 + D * q**3
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == 2 * p * q
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(D, 0), beta.subs(D, 0)), gamma
    )
) == 2 * p**2 * q

# On C*D*Lambda != 0, a single exact maximal minor makes the lifted
# contact map injective.
Lambda = 27 * A * D**2 + 4 * C**3
N1 = (
    36 * D**2 * p**2,
    4 * C**2 * p**2 - 6 * C * D * p * q + 18 * D**2 * q**2,
    Lambda * p,
)
N2 = (
    -24 * C * D * p**2,
    18 * A * D * p**2 + 4 * C**2 * p * q - 12 * C * D * q**2,
    Lambda * q,
)
contact = contact_matrix(P, Q, R, N1, N2)
assert zero(
    contact.extract((0, 1, 2, 3, 4), range(5)).det()
    + 71663616 * C**2 * D**6 * Lambda**3
)

# Lambda=0 is recomputed in a fresh basis and remains injective for C!=0.
A_lambda = -4 * C**3 / (27 * D**2)
R_lambda = sp.expand(R.subs(A, A_lambda))
N1_lambda = (
    2 * p**2,
    2 * C**2 * p**2 / (9 * D**2)
    - C * p * q / (3 * D)
    + q**2,
    0,
)
N2_lambda = (
    0,
    2 * p**2 / (3 * D),
    2 * C * p / (3 * D) + q,
)
contact_lambda = contact_matrix(
    P, Q, R_lambda, N1_lambda, N2_lambda
)
assert zero(
    contact_lambda.extract((0, 1, 2, 3, 4), range(5)).det()
    + 12288 * C**2
)
print("PASS generic and Lambda=0 injective E6 contact charts")


# At C=0,A*D!=0 the contact rank is four, but its kernel line misses
# the Veronese cone.
R_c0 = A * p**3 + D * q**3
N1_c0 = (4 * p**2 / (3 * A), 2 * q**2 / (3 * A), p)
N2_c0 = (0, 2 * p**2 / (3 * D), q)
contact_c0 = contact_matrix(P, Q, R_c0, N1_c0, N2_c0)
kernel_c0 = sp.Matrix([0, 9 * A * D / 4, 0, 0, 1])
assert all(zero(value) for value in contact_c0 * kernel_c0)
assert zero(
    contact_c0.extract((0, 1, 2, 4), (0, 1, 2, 3)).det()
    - 8192 / (9 * A**2)
)
assert zero(
    kernel_c0[1] ** 2
    - kernel_c0[0] * kernel_c0[2]
    - 81 * A**2 * D**2 / 16
)

# At the endpoint A=C=0, the rank-three kernel meets the Veronese in
# exactly one line, giving the mandatory R=D*q^3 survivor.
R_endpoint = D * q**3
N1_endpoint = (2 * p**2, q**2, 0)
N2_endpoint = (0, 2 * p**2 / (3 * D), q)
contact_endpoint = contact_matrix(
    P, Q, R_endpoint, N1_endpoint, N2_endpoint
)
K1 = sp.Matrix([1, 0, 0, 1, 0])
K2 = sp.Matrix([0, 3 * D / 2, 0, 0, 1])
assert all(zero(value) for value in contact_endpoint * K1)
assert all(zero(value) for value in contact_endpoint * K2)
assert zero(
    contact_endpoint.extract((0, 2, 4), (0, 1, 2)).det() + 512
)
lam, mu = sp.symbols("lam mu")
cone_vector = lam * K1 + mu * K2
assert zero(
    cone_vector[1] ** 2
    - cone_vector[0] * cone_vector[2]
    - sp.Rational(9, 4) * D**2 * mu**2
)
print("PASS C=0 Veronese split and unique R=D*q^3 E6 survivor")


# ---------------------------------------------------------------------------
# Full lower solve at R=D*q^3.
# ---------------------------------------------------------------------------

k = sp.symbols("k")
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
tt = sp.symbols("t0:3")
x = sp.symbols("x0:5")
y = sp.symbols("y0:5")
ell = sp.symbols("l0:9")
H4 = sp.Matrix([P, Q, 0])
H3 = sp.Matrix(
    [
        binary(u, 3) + 2 * k * r * p**2,
        binary(v, 3) + k * r * q**2,
        D * q**3,
    ]
)
H2 = sp.Matrix(
    [
        binary(x[:3], 2)
        + r * (x[3] * p + x[4] * q)
        + k**2 * r**2,
        binary(y[:3], 2) + r * (y[3] * p + y[4] * q),
        binary(tt, 2),
    ]
)
L = sp.Matrix(3, 3, ell)
weighted = sp.Poly(
    sp.expand(
        (
            L
            + z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
E = {
    degree: sp.expand(weighted.coeff_monomial(z**degree))
    for degree in range(9)
}
assert zero(E[8])
assert zero(E[7])
assert zero(sp.Poly(E[6], r).coeff_monomial(r))

e6_solution = {
    x[3]: k * (sp.Rational(3, 2) * u[0] - v[2]),
    x[4]: k * u[1],
    y[3]: k * (
        -tt[1] / (3 * D) + sp.Rational(3, 2) * v[0]
    ),
    y[4]: k * v[1],
    ell[8]: k * tt[0],
    u[2]: 0,
}
assert zero(E[6].subs(e6_solution))
E6constant = sp.Poly(E[6], r).coeff_monomial(1)
unknown6 = (
    x[3], x[4], y[3], y[4], ell[8],
    *tt, *u, *v,
)
M6, _ = sp.linear_eq_to_matrix(
    coefficients(E6constant, 6), unknown6
)
assert zero(
    M6.extract((1, 2, 3, 4, 5, 6), (0, 1, 2, 3, 4, 10)).det()
    + 124416 * D**5 * k
)

E5after = sp.Poly(sp.expand(E[5].subs(e6_solution)), r)
expected_E5r = -sp.Rational(3, 2) * k**2 * q**2 * (
    -6 * D * p**2 * v[0]
    + 3 * D * q**2 * u[0]
    - 6 * D * q**2 * v[2]
    + 4 * p**2 * tt[1]
)
assert zero(E5after.coeff_monomial(r) - expected_E5r)
e5_high = {
    tt[1]: sp.Rational(3, 2) * D * v[0],
    u[0]: 2 * v[2],
}
E5constant = sp.expand(E5after.coeff_monomial(1).subs(e5_high))
unknown5 = (x[1], y[1], ell[2], ell[5], ell[6])
M5, rhs5 = sp.linear_eq_to_matrix(
    coefficients(E5constant, 5), unknown5
)
assert zero(
    M5.extract((1, 2, 3, 4, 5), range(5)).det()
    - 5184 * D**4 * k**3
)
left = M5.T.nullspace()
assert len(left) == 1
assert zero((left[0].T * rhs5)[0] + 3 * D * k * v[0] ** 2)

e5_solution = {
    tt[1]: 0,
    u[0]: 2 * v[2],
    v[0]: 0,
    x[1]: u[1] * v[2],
    y[1]: v[1] * v[2],
    ell[2]: k * (x[0] - v[2] ** 2),
    ell[5]: k * y[0],
    ell[6]: tt[0] * v[2],
}
assert zero(E[5].subs(e6_solution).subs(e5_solution))
M0 = sp.factor(
    (k * ell[0] - v[2] * ell[2]).subs(e5_solution)
)
M3 = sp.factor(
    (k * ell[3] - v[2] * ell[5]).subs(e5_solution)
)
E4done = sp.expand(E[4].subs(e6_solution).subs(e5_solution))
expected_E4 = D * (6 * M3 * p**2 * q**2 - 3 * M0 * q**4)
assert zero(E4done - expected_E4)
Ldone = L.subs(e6_solution).subs(e5_solution)
assert all(
    zero(value)
    for value in (
        Ldone * sp.Matrix([k, 0, -v[2]])
        - sp.Matrix([M0, M3, 0])
    )
)
assert zero(
    sp.Poly(expected_E4, p, q).coeff_monomial(p**2 * q**2)
    - 6 * D * M3
)
assert zero(
    sp.Poly(expected_E4, p, q).coeff_monomial(q**4)
    + 3 * D * M0
)
print("PASS full R=D*q^3 E6/E5 solve and E4 linear-part kernel")
print("ALL P2 BRANCH-CONTACT {1,1} EXCLUSION CHECKS PASSED")
