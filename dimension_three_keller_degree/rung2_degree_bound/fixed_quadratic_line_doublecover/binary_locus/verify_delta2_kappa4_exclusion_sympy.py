#!/usr/bin/env python3
"""Full-coefficient exclusion of the doubled-root kappa=4 {2,0} row."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, b, k, m, n, lam = sp.symbols("a b k m n lam")
variables = (p, q, r)
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
x = sp.symbols("x0:6")
y = sp.symbols("y0:6")
ell = sp.symbols("l0:9")


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


def binary(coefficients, degree):
    return sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


def homogeneous_coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p**index * q ** (degree - index))
        for index in range(degree, -1, -1)
    ]


h = (p + q) ** 2
d = (5 * b - 6 * a) / 3
R = a * p**3 + b * p**2 * q + sp.Rational(3, 2) * d * p * q**2 + d * q**3
Nu, Nv, Nt = 6 * p + 4 * q, -2 * q, 6 * a - b
W = m * p + n * q
S = sp.Rational(1, 2) * k * r**2 + W * r
H4 = sp.Matrix([h * p**2, h * q**2, 0])
H3 = sp.Matrix([binary(u, 3) + Nu * S, binary(v, 3) + Nv * S, R])
H2 = sp.Matrix(
    [
        binary(x[:3], 2) + r * (x[3] * p + x[4] * q) + x[5] * r**2,
        binary(y[:3], 2) + r * (y[3] * p + y[4] * q) + y[5] * r**2,
        binary(t, 2) + Nt * S,
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

# Exact open is b(3a-2b) != 0.  E6 r^3 has a nonzero p^2q
# coefficient because b != 0, hence k=0.
expected_r3 = -k**2 * (
    6 * a * p**3 - 18 * a * p * q**2 - 12 * a * q**3
    - 4 * b * p**3 - 18 * b * p**2 * q
    - 33 * b * p * q**2 - 22 * b * q**3
)
assert zero(sp.Poly(E[6], r).coeff_monomial(r**3) - expected_r3)
assert sp.Poly(expected_r3 / (-k**2), p, q).coeff_monomial(
    p**2 * q
) == -18 * b
print("PASS exact-open E6 r^3 tangent obstruction")


# Solve E6 r after k=0, including 6a+11b=0.
E6r = sp.Poly(sp.expand(E[6].subs(k, 0)), r).coeff_monomial(r)
e = homogeneous_coefficients(E6r, 5)
assert zero(e[0] - 4 * (3 * a - 2 * b) * (-m**2 + y[5]))
assert zero(e[5] - 4 * n**2 * (6 * a + 11 * b))

# Generic endpoint: y5=m^2, n=0.  The middle system in x5,X=m^2
# has rank two; the second minor handles the only zero of the first.
X = sp.symbols("X")
middle = [
    sp.expand(
        item.subs(y[5], m**2).subs(n, 0).subs(m**2, X)
    )
    for item in e[1:5]
]
Mmid, rhsmid = sp.linear_eq_to_matrix(middle, (x[5], X))
assert rhsmid == sp.zeros(4, 1)
assert zero(
    Mmid.extract((2, 3), (0, 1)).det()
    - 4 * (6 * a + 11 * b) * (18 * a + b)
)
assert zero(
    Mmid.extract((0, 1), (0, 1)).det()
    - 16 * (27 * a**2 + 12 * a * b - 2 * b**2)
)
assert zero(
    Mmid.extract((0, 1), (0, 1)).det().subs(a, -b / 18)
    + sp.Rational(124, 3) * b**2
)

# Special endpoint 6a+11b=0: three explicit equations give
# x5=4m^2, n=0, then m=0.
special = [
    sp.factor(item.subs(a, -sp.Rational(11, 6) * b).subs(y[5], m**2))
    for item in e
]
assert zero(special[4] - 16 * b * (-4 * m**2 + x[5]))
assert zero(
    special[3] - 4 * b * (-56 * m**2 + 9 * n**2 + 14 * x[5])
)
assert zero(
    special[1] - 2 * b * (-59 * m**2 + 30 * m * n + 11 * x[5])
)
high = {k: 0, m: 0, n: 0, x[5]: 0, y[5]: 0}
print("PASS endpoint-safe E6 r^1 elimination")


# Constant E6 has exactly the polynomial kernel N.
E6c = sp.expand(E[6].subs(high))
eq6 = homogeneous_coefficients(E6c, 6)
unknown6 = (x[3], x[4], y[3], y[4], ell[8])
M6, rhs6 = sp.linear_eq_to_matrix(eq6, unknown6)
kernel = sp.Matrix([6, 4, 0, -2, 6 * a - b])
assert rhs6 == sp.zeros(7, 1)
assert M6 * kernel == sp.zeros(7, 1)
assert zero(
    M6.extract((0, 1, 2, 3), (0, 2, 3, 4)).det()
    - 64 * b * (3 * a - 2 * b) ** 2
)
e6sol = {
    **high,
    x[3]: 6 * lam,
    x[4]: 4 * lam,
    y[3]: 0,
    y[4]: -2 * lam,
    ell[8]: (6 * a - b) * lam,
}
assert zero(E[6].subs(e6sol))
print("PASS complete E6 kernel solve")


# Lambda zero gives a zero third column.
E5zero = sp.expand(E[5].subs(e6sol).subs(lam, 0))
M5z, rhs5z = sp.linear_eq_to_matrix(
    homogeneous_coefficients(E5zero, 5), (ell[2], ell[5])
)
assert rhs5z == sp.zeros(6, 1)
assert zero(M5z.extract((0, 1), (0, 1)).det() - 12 * a * (3 * a - 2 * b))
assert zero(
    M5z.extract((0, 2), (0, 1)).det()
    - 4 * (3 * a - 2 * b) * (9 * a + b)
)


# If lambda != 0 and 6a-b != 0, the plane-field exit applies.  The only
# residual branch is a=b/6; exactness then says b != 0.
E5res = sp.expand(E[5].subs(e6sol).subs(a, b / 6))
eq5res = homogeneous_coefficients(E5res, 5)
unknown5 = (
    ell[2], ell[5], t[0], t[1], t[2],
    v[0], v[1], v[2], v[3],
)
M5, _ = sp.linear_eq_to_matrix(eq5res, unknown5)
pivots = (0, 1, 2, 3, 5, 7)
assert zero(M5[:, pivots].det() + 36864 * b**4 * lam**4)
e5sol = {
    ell[2]: (
        -12 * lam * u[0] + 14 * lam * u[1] - 15 * lam * u[2]
        + sp.Rational(27, 2) * lam * u[3]
    ),
    ell[5]: (
        6 * lam * u[0] - 5 * lam * u[1] + 6 * lam * u[2]
        - 6 * lam * u[3] + 4 * lam * v[1] - 3 * lam * v[3]
    ),
    t[0]: t[2] / 4,
    t[1]: t[2],
    v[0]: (
        u[0] - sp.Rational(5, 6) * u[1] + u[2] - u[3]
        + sp.Rational(5, 6) * v[1] - sp.Rational(1, 2) * v[3]
    ),
    v[2]: -u[2] / 2 + sp.Rational(3, 4) * u[3] + sp.Rational(3, 2) * v[3],
}
assert zero(E5res.subs(e5sol))
E4done = sp.Poly(
    sp.expand(E[4].subs(e6sol).subs(a, b / 6).subs(e5sol)), r
)
assert zero(
    E4done.coeff_monomial(r) - 6 * b * lam**2 * (p + 2 * q) ** 3
)
print("PASS lambda split and residual E5/E4 contradiction")
print("ALL EXACT KAPPA=4 DELTA=2 EXCLUSION CHECKS PASSED")
