#!/usr/bin/env python3
"""Full-coefficient exclusion of the kappa=16, delta=2 {2,0} row."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, d, k, m, n, lam = sp.symbols("a d k m n lam")
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


def coefficient(value, p_degree, q_degree, r_degree):
    return sp.Poly(sp.expand(value), p, q, r).coeff_monomial(
        p**p_degree * q**q_degree * r**r_degree
    )


def homogeneous_coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p**index * q ** (degree - index))
        for index in range(degree, -1, -1)
    ]


# Complete E7 family.  The k=2 Hilbert--Burch column is
# (Nu,Nv,Nt)=(5p+q,-p-5q,3(a-d)).  Its degree-raised copies pN,qN
# span the r^0 kernel, so no E7 tangent has been omitted.
h = p**2 + 4 * p * q + q**2
R = a * p**3 + 3 * a * p**2 * q + 3 * d * p * q**2 + d * q**3
Nu = 5 * p + q
Nv = -p - 5 * q
Nt = 3 * (a - d)
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


# The earliest E6 coefficient kills the genuine r^1 E7 tangent.  Exact
# delta=2 on this family is a+d != 0, so the displayed cubic cannot vanish.
C_ad = (
    (a + 2 * d) * (p**3 + 3 * p**2 * q)
    + (2 * a + d) * (3 * p * q**2 + q**3)
)
E6_r3 = sp.Poly(E[6], r).coeff_monomial(r**3)
assert zero(E6_r3 - 12 * k**2 * C_ad)
assert coefficient(C_ad, 3, 0, 0) == a + 2 * d
assert coefficient(C_ad, 0, 3, 0) == 2 * a + d
print("PASS E6 r^3 kills the k=2 r^1 tangent on a+d != 0")


# After k=0, the remaining r coefficient kills both degree-raised E7
# tangents W=mp+nq and both r^2 coefficients of H2_1,H2_2.
E6_after_k = sp.Poly(sp.expand(E[6].subs(k, 0)), r)
E6_r1 = E6_after_k.coeff_monomial(r)
e6r = [sp.factor(item / 12) for item in homogeneous_coefficients(E6_r1, 5)]
assert zero(e6r[0] - 2 * m**2 * (a + 2 * d))
assert zero(e6r[5] - 2 * n**2 * (2 * a + d))

# Exceptional endpoint a+2d=0: exactness gives d != 0.  The listed
# coefficients successively give n=0, x5=y5=0, and m=0.
special_left = [sp.factor(item.subs({a: -2 * d, n: 0})) for item in e6r]
assert zero(special_left[1] - 2 * d * (x[5] - y[5]))
assert zero(special_left[4] - d * (7 * x[5] - y[5]))
assert zero(
    special_left[2]
    - 2 * d * (-9 * m**2 + 7 * x[5] - 7 * y[5])
)

# The symmetric endpoint 2a+d=0.
special_right = [sp.factor(item.subs({d: -2 * a, m: 0})) for item in e6r]
assert zero(special_right[1] + a * (x[5] - 7 * y[5]))
assert zero(special_right[4] + 2 * a * (x[5] - y[5]))
assert zero(
    special_right[3]
    + 2 * a * (9 * n**2 + 7 * x[5] - 7 * y[5])
)

# Once m=n=0, the x5,y5 system has rank two at every nonzero (a,d).
e6r_zero_W = [item.subs({m: 0, n: 0}) for item in e6r[1:5]]
matrix_xy, rhs_xy = sp.linear_eq_to_matrix(e6r_zero_W, (x[5], y[5]))
assert rhs_xy == sp.zeros(4, 1)
assert zero(
    matrix_xy.extract((0, 1), (0, 1)).det()
    + 8 * a * (a + 2 * d)
)
assert zero(
    matrix_xy.extract((2, 3), (0, 1)).det()
    + 8 * d * (2 * a + d)
)
high_solution = {k: 0, m: 0, n: 0, x[5]: 0, y[5]: 0}
print("PASS E6 r^1 kills W and both quadratic r coefficients")


# With all higher r-dependence gone, E6 is the homogeneous M1 system.
# The two minors guard rank four across a+d != 0, and the polynomial
# kernel includes the a=d specialization without division.
E6_constant = sp.expand(E[6].subs(high_solution))
eq6_constant = homogeneous_coefficients(E6_constant, 6)
unknown6 = (x[3], x[4], y[3], y[4], ell[8])
M6, rhs6 = sp.linear_eq_to_matrix(eq6_constant, unknown6)
assert rhs6 == sp.zeros(7, 1)
assert zero(
    M6.extract((1, 2, 4, 5), (0, 1, 2, 4)).det()
    - 34560 * (a - d) * (a + d) ** 2
)
assert zero(
    M6.extract((1, 2, 3, 4), (0, 1, 2, 4)).det()
    - 34560 * (a + d) ** 2 * (13 * a - d)
)
kernel6 = sp.Matrix([5, 1, -1, -5, 3 * (a - d)])
assert M6 * kernel6 == sp.zeros(7, 1)
e6_solution = {
    **high_solution,
    x[3]: 5 * lam,
    x[4]: lam,
    y[3]: -lam,
    y[4]: -5 * lam,
    ell[8]: 3 * (a - d) * lam,
}
assert zero(E[6].subs(e6_solution))
print("PASS complete E6 solve, including a=d and a!=d branches")


# If lam=0, E5 is a rank-two constant syzygy in L13,L23.  Hence the
# entire third column of L is zero.  The two minors again cover every
# exact point.
E5_after_E6 = sp.expand(E[5].subs(e6_solution))
E5_lam_zero = E5_after_E6.subs(lam, 0)
eq5_lam_zero = homogeneous_coefficients(E5_lam_zero, 5)
M5_zero, rhs5_zero = sp.linear_eq_to_matrix(
    eq5_lam_zero, (ell[2], ell[5])
)
assert rhs5_zero == sp.zeros(6, 1)
assert zero(
    M5_zero.extract((1, 2), (0, 1)).det()
    + 288 * a * (a + 2 * d)
)
assert zero(
    M5_zero.extract((3, 4), (0, 1)).det()
    + 288 * d * (2 * a + d)
)
assert L.subs(e6_solution).subs(lam, 0)[:, 2] == sp.Matrix(
    [ell[2], ell[5], 0]
)
print("PASS lam=0 forces a zero third column of the linear part")


# In the only non-plane-exit branch, a=d != 0 and lam != 0.  This is the
# full E5 solve; no binary H3/H2 or remaining linear coefficient was
# deleted before the solve.
E5_equal = sp.expand(E5_after_E6.subs(d, a))
eq5_equal = homogeneous_coefficients(E5_equal, 5)
unknown5 = (
    ell[2], ell[5], t[0], t[1], t[2],
    v[0], v[1], v[2], v[3],
)
M5, _ = sp.linear_eq_to_matrix(eq5_equal, unknown5)
pivot_columns = (0, 1, 2, 3, 5, 7)
assert zero(
    M5[:, pivot_columns].det() + 59719680 * a**4 * lam**4
)
e5_solution = {
    ell[2]: (
        -sp.Rational(3, 10) * lam * u[0]
        + sp.Rational(11, 10) * lam * u[1]
        - sp.Rational(7, 2) * lam * u[2]
        + sp.Rational(15, 2) * lam * u[3]
    ),
    ell[5]: (
        sp.Rational(3, 2) * lam * u[0]
        - sp.Rational(1, 2) * lam * u[1]
        + sp.Rational(11, 2) * lam * u[2]
        - sp.Rational(33, 2) * lam * u[3]
        + lam * v[1]
        - 3 * lam * v[3]
    ),
    t[0]: t[2],
    t[1]: 2 * t[2],
    v[0]: -u[0] / 5 + u[1] / 15 + v[1] / 3,
    v[2]: -5 * u[2] + 15 * u[3] + 3 * v[3],
}
assert zero(E5_equal.subs(e5_solution))

# The r coefficient of E4 is independent of every still-free lower
# coefficient and is nonzero on a*lam != 0.
E4_completed = sp.Poly(
    sp.expand(E[4].subs(e6_solution).subs(d, a).subs(e5_solution)), r
)
assert zero(
    E4_completed.coeff_monomial(r)
    - 72 * a * lam**2 * (p + q) ** 3
)
print("PASS a=d full E5 solve and decisive E4 r coefficient")
print("ALL EXACT KAPPA=16 DELTA=2 EXCLUSION CHECKS PASSED")
