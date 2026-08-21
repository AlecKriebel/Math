#!/usr/bin/env python3
"""Exact E6/E5 exclusion on the h=p^2, simple-fixed-root {1,1} row."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, B, C = sp.symbols("A B C")
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


def binary(coefficients, degree):
    return sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


def lifted_contact_matrix(P, Q, R, N1, N2):
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


def signed_kernel_minors(matrix):
    submatrix = matrix.extract((0, 1, 2, 3), range(5))
    return sp.Matrix(
        [
            sp.factor(
                (-1) ** column
                * submatrix[
                    :,
                    [index for index in range(5) if index != column],
                ].det()
            )
            for column in range(5)
        ]
    )


# ---------------------------------------------------------------------------
# Basis-free contact divisor on the exact open B*C != 0.
# ---------------------------------------------------------------------------

P, Q = p**4, p**2 * q**2
R = p * (A * p**2 + B * p * q + C * q**2)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == 2 * p**2
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(A, 0), beta.subs(A, 0)),
        gamma,
    )
) == 2 * p**2
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(B, 0), beta.subs(B, 0)),
        gamma,
    )
) == 2 * p**2 * q
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(C, 0), beta.subs(C, 0)),
        gamma,
    )
) == 2 * p**3

Delta = 4 * A * C - B**2
N1 = (
    16 * C * p**2,
    -2 * q * (3 * B * p - 2 * C * q),
    3 * Delta * p,
)
N2 = (
    -8 * B * p**2,
    2 * q * (6 * A * p - B * q),
    3 * Delta * q,
)
for N in (N1, N2):
    assert zero(alpha * N[0] + beta * N[1] + gamma * N[2])

contact = lifted_contact_matrix(P, Q, R, N1, N2)
kernel = sp.Matrix(
    [
        24 * A * C + B**2,
        -B * C,
        -32 * C**2,
        576 * C**2 * Delta,
        -9 * Delta * (32 * A * C + B**2),
    ]
)
assert all(zero(value) for value in contact * kernel)
common = 36864 * B * C * Delta**2
assert all(
    zero(value)
    for value in signed_kernel_minors(contact) - common * kernel
)
# The third signed minor is nonzero on B*C*Delta != 0, so the contact
# matrix has rank exactly four there.  Its kernel line meets the
# Veronese cone Y^2=XZ precisely on the displayed divisor.
assert zero(kernel[1] ** 2 - kernel[0] * kernel[2]
            - 3 * C**2 * (256 * A * C + 11 * B**2))
assert zero(
    Delta.subs(A, -11 * B**2 / (256 * C))
    + sp.Rational(75, 64) * B**2
)
print("PASS signed-minor/Veronese certificate for 256*A*C+11*B^2")


# Delta=0 is inside the exact open and must not be lost to the preceding
# basis.  A fresh polynomial tangent basis gives another rank-four line,
# whose Veronese obstruction is 225*B^2.
A_delta = B**2 / (4 * C)
R_delta = sp.expand(R.subs(A, A_delta))
N1_delta = (8 * C * p**2, -3 * B * p * q + 2 * C * q**2, 0)
N2_delta = (0, 2 * p * q, B * p + 2 * C * q)
alpha_delta = sp.expand(alpha.subs(A, A_delta))
beta_delta = sp.expand(beta.subs(A, A_delta))
for N in (N1_delta, N2_delta):
    assert zero(alpha_delta * N[0] + beta_delta * N[1] + gamma * N[2])
contact_delta = lifted_contact_matrix(
    P, Q, R_delta, N1_delta, N2_delta
)
kernel_delta = sp.Matrix([8, 15 * B, 0, 192 * C**2, -27 * B**2])
assert all(zero(value) for value in contact_delta * kernel_delta)
common_delta = 4096 * B * C**4
assert all(
    zero(value)
    for value in signed_kernel_minors(contact_delta)
    - common_delta * kernel_delta
)
assert zero(
    kernel_delta[1] ** 2
    - kernel_delta[0] * kernel_delta[2]
    - 225 * B**2
)
print("PASS Delta=0 endpoint chart and B=0/C=0 mutations")


# ---------------------------------------------------------------------------
# Mandatory rational survivor and its full E5 obstruction.
# ---------------------------------------------------------------------------

k = sp.symbols("k")
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
tt = sp.symbols("t0:3")
x = sp.symbols("x0:5")
y = sp.symbols("y0:5")
ell = sp.symbols("l0:9")
R0 = p * (-11 * p**2 + 16 * p * q + q**2)
Nu, Nv, Nt = 4 * p**2, 6 * p * q + q**2, 15 * p + 30 * q
H4 = sp.Matrix([P, Q, 0])
H3 = sp.Matrix(
    [binary(u, 3) + k * r * Nu,
     binary(v, 3) + k * r * Nv,
     R0]
)
H2 = sp.Matrix(
    [
        binary(x[:3], 2)
        + r * (x[3] * p + x[4] * q)
        + 6 * k**2 * r**2,
        binary(y[:3], 2)
        + r * (y[3] * p + y[4] * q)
        + 9 * k**2 * r**2,
        binary(tt, 2) + k * r * Nt,
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
    x[3]: k * (-4 * tt[2] + 3 * u[0] + 3 * u[1] + 108 * v[3]),
    x[4]: k * (sp.Rational(3, 2) * u[1] + 6 * u[2] + 6 * v[3]),
    y[3]: 3 * k * (v[0] + v[1]),
    y[4]: k * (
        -sp.Rational(1, 2) * tt[1]
        + 10 * tt[2]
        + sp.Rational(3, 2) * v[1]
        + 6 * v[2]
        - sp.Rational(621, 2) * v[3]
    ),
    ell[8]: k * (
        2 * tt[0] - tt[1] + 113 * tt[2] - 3375 * v[3]
    ),
    u[3]: 0,
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
    M6.extract((0, 1, 2, 3, 4, 6), (0, 1, 2, 3, 4, 11)).det()
    + 49152 * k
)
E5after = sp.Poly(sp.expand(E[5].subs(e6_solution)), r)
expected_E5_r2 = -24 * k**3 * (
    72 * p**3 + 7 * p**2 * q - 11 * p * q**2 + q**3
)
assert zero(E5after.coeff_monomial(r**2) - expected_E5_r2)
assert sp.Poly(expected_E5_r2 / (-24 * k**3), p, q).coeff_monomial(
    p**3
) == 72
print("PASS mandatory rational E6 survivor and full E5 obstruction")
print("ALL P2 SIMPLE-FIXED {1,1} EXCLUSION CHECKS PASSED")
