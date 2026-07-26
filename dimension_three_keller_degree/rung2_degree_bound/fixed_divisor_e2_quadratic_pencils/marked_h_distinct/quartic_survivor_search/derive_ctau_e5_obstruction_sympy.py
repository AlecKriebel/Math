#!/usr/bin/env python3
"""Exact characteristic-zero obstruction for the finite nonzero CTAU chart.

This script starts from the released complete E7 normal form

    H4 = ((x^2+yz)^2, x^2(x^2+yz), 0),
    H3 = (A*x^3, B*x^3, x*((1+k)*x^2+yz)),
    (H2)_3 = T*x^2,

valid for every finite k != 0.  It reconstructs the weighted Jacobian
determinant and certifies the division-free E6/E5 coefficient argument.
"""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, weight, k = sp.symbols("x y z weight k")
A, B, T = sp.symbols("A B T")
xyz = (x, y, z)

mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)

a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")

h = x**2 + y * z
P = h**2
Q = h * x**2
R = x * (h + k * x**2)
U = A * x**3
V = B * x**3
W = T * x**2

H2 = sp.Matrix(
    [
        sum(coefficient * monomial for coefficient, monomial in zip(a, mon2)),
        sum(coefficient * monomial for coefficient, monomial in zip(b, mon2)),
        W,
    ]
)
H3 = sp.Matrix([U, V, R])
H4 = sp.Matrix([P, Q, 0])
L = sp.Matrix(3, 3, ell)

weighted_matrix = (
    L
    + weight * H2.jacobian(xyz)
    + weight**2 * H3.jacobian(xyz)
    + weight**3 * H4.jacobian(xyz)
)
weighted_determinant = sp.Poly(sp.expand(weighted_matrix.det()), weight)


def homogeneous_exponents(degree: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficient_dict(polynomial: sp.Expr, degree: int) -> dict[tuple[int, int, int], sp.Expr]:
    expanded = sp.Poly(sp.expand(polynomial), x, y, z)
    return {
        exponent: sp.factor(
            expanded.coeff_monomial(x ** exponent[0] * y ** exponent[1] * z ** exponent[2])
        )
        for exponent in homogeneous_exponents(degree)
        if expanded.coeff_monomial(
            x ** exponent[0] * y ** exponent[1] * z ** exponent[2]
        )
        != 0
    }


for degree in (9, 8, 7):
    assert weighted_determinant.coeff_monomial(weight**degree) == 0

E6 = weighted_determinant.coeff_monomial(weight**6)
actual_e6 = coefficient_dict(E6, 6)
expected_e6 = {
    (5, 1, 0): 3 * a[1] * k - a[1] - 6 * b[1] * k - 2 * b[1] + 4 * ell[7],
    (5, 0, 1): -3 * a[2] * k + a[2] + 6 * b[2] * k + 2 * b[2] - 4 * ell[8],
    (4, 2, 0): 2 * (3 * a[3] * k - a[3] - 6 * b[3] * k - 2 * b[3]),
    (4, 0, 2): -2 * (3 * a[5] * k - a[5] - 6 * b[5] * k - 2 * b[5]),
    (3, 2, 1): -a[1] - 6 * b[1] * k - 4 * b[1] + 8 * ell[7],
    (3, 1, 2): a[2] + 6 * b[2] * k + 4 * b[2] - 8 * ell[8],
    (2, 3, 1): -2 * (a[3] + 6 * b[3] * k + 4 * b[3]),
    (2, 1, 3): 2 * (a[5] + 6 * b[5] * k + 4 * b[5]),
    (1, 3, 2): -2 * (b[1] - 2 * ell[7]),
    (1, 2, 3): 2 * (b[2] - 2 * ell[8]),
    (0, 4, 2): -4 * b[3],
    (0, 2, 4): 4 * b[5],
}
assert set(actual_e6) == set(expected_e6)
assert all(
    sp.expand(actual_e6[exponent] - expected_e6[exponent]) == 0
    for exponent in expected_e6
)

# These are precisely the ten variables occurring in E6.  The displayed
# triangular coefficient chain proves that they vanish when k != 0.
e6_forced_zero = {
    a[1]: 0,
    a[2]: 0,
    a[3]: 0,
    a[5]: 0,
    b[1]: 0,
    b[2]: 0,
    b[3]: 0,
    b[5]: 0,
    ell[7]: 0,
    ell[8]: 0,
}
all_lower = a + b + ell
assert {
    variable for coefficient in actual_e6.values() for variable in coefficient.free_symbols
}.intersection(set(all_lower)) == set(e6_forced_zero)
assert sp.expand(E6.subs(e6_forced_zero)) == 0

# Saturation certificates for the two nontrivial triangular chains.
# After b1=2*l7 and a1=-12*k*l7, the remaining E6 equation is
# -36*k^2*l7.  The z-chain gives +36*k^2*l8.
y_chain = sp.expand(
    actual_e6[(5, 1, 0)].subs({b[1]: 2 * ell[7], a[1]: -12 * k * ell[7]})
)
z_chain = sp.expand(
    actual_e6[(5, 0, 1)].subs({b[2]: 2 * ell[8], a[2]: -12 * k * ell[8]})
)
assert y_chain == -36 * k**2 * ell[7]
assert z_chain == 36 * k**2 * ell[8]

E5 = weighted_determinant.coeff_monomial(weight**5)
actual_e5_reduced = coefficient_dict(sp.expand(E5.subs(e6_forced_zero)), 5)
expected_e5_reduced = {
    (4, 1, 0): (3 * k - 1) * ell[1] - (6 * k + 2) * ell[4],
    (4, 0, 1): -(3 * k - 1) * ell[2] + (6 * k + 2) * ell[5],
    (2, 2, 1): -ell[1] - (6 * k + 4) * ell[4],
    (2, 1, 2): ell[2] + (6 * k + 4) * ell[5],
    (0, 3, 2): -2 * ell[4],
    (0, 2, 3): 2 * ell[5],
}
assert set(actual_e5_reduced) == set(expected_e5_reduced)
assert all(
    sp.expand(actual_e5_reduced[exponent] - expected_e5_reduced[exponent]) == 0
    for exponent in expected_e5_reduced
)

e5_forced_zero = {ell[1]: 0, ell[2]: 0, ell[4]: 0, ell[5]: 0}
assert sp.expand(E5.subs(e6_forced_zero).subs(e5_forced_zero)) == 0

singular_linear_part = sp.expand(L.det().subs(e6_forced_zero).subs(e5_forced_zero))
assert singular_linear_part == 0

# The released E7 normal-form cover used q and r.  Record its exact
# denominator-recovery certificate here so no exceptional finite k != 0
# can be lost when this obstruction is attached to that normal form.
q = 9 * k**2 + 6 * k - 1
r = 3 * k - 1
assert sp.resultant(q, r, k) == 18
assert sp.expand(sp.Rational(1, 2) * q - sp.Rational(3, 2) * (k + 1) * r) == 1
assert sp.gcd(q, r) == 1

print("CTAU_E5_SYMPY_PASS_6C1D4A")
print("finite k != 0: E6 forces 10 coefficients; E5 forces det(L)=0")
