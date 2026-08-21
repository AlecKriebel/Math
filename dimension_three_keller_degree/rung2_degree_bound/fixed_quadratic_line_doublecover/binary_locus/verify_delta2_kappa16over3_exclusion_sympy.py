#!/usr/bin/env python3
"""Full-coefficient exclusion of the kappa=16/3 delta=2 {2,0} row."""

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


# Rational representative of kappa=B^2/(AC)=16/3.
h = (p + q) * (3 * p + q)
R = (p + q) * (a * p**2 + 2 * b * p * q + b * q**2)
Nu, Nv, Nt = 4 * p + q, -3 * q, a - b
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

# Exact open set: b(a-b)(a+3b) != 0.  The literal point a=0,b=1
# guards gcd degree two and the polynomial Hilbert--Burch kernel.
def jac(first, second):
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


alpha = jac(h * q**2, R)
beta = -jac(h * p**2, R)
gamma = jac(h * p**2, h * q**2)
literal = {a: 0, b: 1}
literal_gcd = sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(literal), beta.subs(literal)),
        gamma,
    )
)
assert literal_gcd == 2 * p * (p + q)
kernel = sp.Matrix([4, 1, 0, -3, a - b])

# Earliest E6 kills the genuine r^1 tangent because b != 0.
expected_r3 = (
    6 * k**2 * (p + q)
    * (
        2 * a * p * q + a * q**2
        + 3 * b * p**2 + 4 * b * p * q + 2 * b * q**2
    )
)
assert zero(sp.Poly(E[6], r).coeff_monomial(r**3) - expected_r3)
assert sp.Poly(expected_r3 / (6 * k**2 * (p + q)), p, q).coeff_monomial(
    p**2
) == 3 * b
print("PASS exact open and E6 r^3 tangent obstruction")


# After k=0, solve the r coefficient without generic divisions.
E6_r1 = sp.Poly(sp.expand(E[6].subs(k, 0)), r).coeff_monomial(r)
e = homogeneous_coefficients(E6_r1, 5)
assert zero(e[0] + 12 * b * (-3 * m**2 + 4 * y[5]))
assert zero(e[5] - 12 * n**2 * (a + 2 * b))

# b != 0 gives y5=3m^2/4.  If a+2b != 0, n=0 and the four
# middle equations are a rank-two system in x5 and X=m^2.
X = sp.symbols("X")
middle = [
    sp.expand(
        item.subs(y[5], sp.Rational(3, 4) * m**2)
        .subs(n, 0)
        .subs(m**2, X)
    )
    for item in e[1:5]
]
M_middle, rhs_middle = sp.linear_eq_to_matrix(middle, (x[5], X))
assert rhs_middle == sp.zeros(4, 1)
assert zero(
    M_middle.extract((2, 3), (0, 1)).det()
    - 192 * (a - b) * (a + 2 * b)
)

# On a=-2b the endpoint gives no n equation, so retain the full middle
# system.  These three equations give x5=3m^2/4, then n=0, then m=0.
special = [
    sp.factor(
        item.subs(
            {a: -2 * b, y[5]: sp.Rational(3, 4) * m**2}
        )
    )
    for item in e
]
assert zero(special[4] - 3 * b * (-3 * m**2 + 4 * x[5]))
assert zero(
    special[3]
    - 12 * b * (-sp.Rational(21, 4) * m**2 + 3 * n**2 + 7 * x[5])
)
assert zero(
    special[1]
    - 18 * b * (-5 * m**2 + 4 * m * n + 4 * x[5])
)
high_solution = {k: 0, m: 0, n: 0, x[5]: 0, y[5]: 0}
print("PASS E6 r^1 kills both r^0 tangents and quadratic r terms")


# Constant E6 is the homogeneous M1 system.  Two minors cover b != 0;
# the polynomial kernel remains valid on every exact divisor.
E6c = sp.expand(E[6].subs(high_solution))
eq6c = homogeneous_coefficients(E6c, 6)
unknown6 = (x[3], x[4], y[3], y[4], ell[8])
M6, rhs6 = sp.linear_eq_to_matrix(eq6c, unknown6)
assert rhs6 == sp.zeros(7, 1)
assert M6 * kernel == sp.zeros(7, 1)
assert zero(
    M6.extract((0, 1, 4, 5), (0, 2, 3, 4)).det()
    - 2304 * b**2 * (11 * a + 25 * b)
)
assert zero(
    M6.extract((0, 1, 2, 5), (0, 1, 2, 4)).det()
    - 20736 * b * (a - 5 * b) * (a + 2 * b)
)
e6_solution = {
    **high_solution,
    x[3]: 4 * lam,
    x[4]: lam,
    y[3]: 0,
    y[4]: -3 * lam,
    ell[8]: (a - b) * lam,
}
assert zero(E[6].subs(e6_solution))
print("PASS complete E6 kernel solve")


# If lambda=0, E5 forces L13=L23=0; with L33=0 this contradicts
# invertibility.  The two minors cover b != 0.
E5zero = sp.expand(E[5].subs(e6_solution).subs(lam, 0))
eq5zero = homogeneous_coefficients(E5zero, 5)
M5, rhs5 = sp.linear_eq_to_matrix(eq5zero, (ell[2], ell[5]))
assert rhs5 == sp.zeros(6, 1)
assert zero(M5.extract((0, 1), (0, 1)).det() + 432 * a * b)
assert zero(M5.extract((3, 4), (0, 1)).det() + 144 * b * (a + 2 * b))
assert L.subs(e6_solution).subs(lam, 0)[:, 2] == sp.Matrix(
    [ell[2], ell[5], 0]
)

# If lambda != 0, exactness includes a-b != 0, so L33 is nonzero and
# the separately proved plane-field exit applies.
assert e6_solution[ell[8]] == (a - b) * lam
print("PASS lambda split: singular column or nonzero plane-exit normal")
print("ALL EXACT KAPPA=16/3 DELTA=2 EXCLUSION CHECKS PASSED")
