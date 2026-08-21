#!/usr/bin/env python3
"""Exact delta=2 Hilbert--Burch stratification in the binary quartic row.

This verifier reconstructs the r^1 E7 matrix from the binary Jacobians.
It checks one decisive maximal minor on every exact-delta=2 incidence
type and checks the three exceptional {2,0} families separately.
"""

from __future__ import annotations

import itertools
import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q = sp.symbols("p q")


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


def jac(f, g):
    return sp.expand(
        sp.diff(f, p) * sp.diff(g, q)
        - sp.diff(f, q) * sp.diff(g, p)
    )


def coefficient_vector(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return sp.Matrix(
        [
            poly.coeff_monomial(p**i * q ** (degree - i))
            for i in range(degree, -1, -1)
        ]
    )


def matrices(h, R):
    """Return the r^2,r^1,r^0 E7 coefficient matrices."""
    P = sp.expand(h * p**2)
    Q = sp.expand(h * q**2)
    alpha = jac(Q, R)
    beta = -jac(P, R)
    gamma = jac(P, Q)
    blocks = (
        ((1,), (1,), ()),
        ((p, q), (p, q), (1,)),
        ((p**2, p * q, q**2), (p**2, p * q, q**2), (p, q)),
    )
    output = []
    for offset, (left, middle, right) in enumerate(blocks):
        columns = (
            tuple(alpha * item for item in left)
            + tuple(beta * item for item in middle)
            + tuple(gamma * item for item in right)
        )
        output.append(
            sp.Matrix.hstack(
                *(coefficient_vector(column, 5 + offset) for column in columns)
            )
        )
    return alpha, beta, gamma, tuple(output)


def maximal_minor(matrix, rows):
    assert matrix.cols == len(rows)
    return sp.factor(matrix.extract(rows, range(matrix.cols)).det())


def gcd3(first, second, third):
    return sp.factor(sp.gcd(sp.gcd(first, second), third))


def total_degree(value):
    return sp.Poly(value, p, q).total_degree()


# ---------------------------------------------------------------------------
# Boundary fixed-divisor orbits.  The displayed minors contain only factors
# that exact delta=2 excludes, so every boundary delta=2 point has shape
# {1,1}; equivalently M1 has full column rank five.
# ---------------------------------------------------------------------------

a, b, c, d = sp.symbols("a b c d")

# h=p^2: either the generic p contribution plus q-contact, or p-order one.
_, _, _, mats = matrices(p**2, a * p**3 + c * p * q**2 + d * q**3)
assert zero(maximal_minor(mats[1], (1, 2, 3, 4, 5)) - 41472 * d**4)
_, _, _, mats = matrices(p**2, a * p**3 + b * p**2 * q + c * p * q**2)
assert zero(maximal_minor(mats[1], (0, 1, 2, 3, 4)) + 1024 * b * c**3)

# h=pq: a doubled contribution at one branch, or one at each branch.
_, _, _, mats = matrices(p * q, a * p**3 + b * p**2 * q)
assert zero(maximal_minor(mats[1], (0, 1, 2, 3, 4)) + 3240 * a**3 * b)
_, _, _, mats = matrices(p * q, b * p**2 * q + c * p * q**2)
assert zero(maximal_minor(mats[1], (1, 2, 3, 4, 5)) - 8 * b**2 * c**2)

# h=p(p+q).  These five rows cover, up to swap: doubled p, doubled p+q,
# the two simple fixed roots, p plus ramification contact, and p+q plus
# ramification contact.
A, B, C, T = sp.symbols("A B C T")
ell = p + q
_, _, _, mats = matrices(p * ell, p**2 * (A * p + B * q))
assert zero(
    maximal_minor(mats[1], (0, 1, 2, 3, 4))
    + 1080 * B * (A - B) ** 2 * (3 * A - 4 * B)
)
_, _, _, mats = matrices(p * ell, ell**2 * (A * p + B * q))
assert zero(
    maximal_minor(mats[1], (0, 1, 2, 3, 4))
    + 648 * B**3 * (5 * A + 4 * B)
)
_, _, _, mats = matrices(p * ell, p * ell * (A * p + B * q))
assert zero(
    maximal_minor(mats[1], (0, 1, 2, 3, 4))
    - 8 * B**2 * (A - B) * (A + 4 * B)
)
_, _, _, mats = matrices(
    p * ell, p * (4 * T * p**2 + 3 * T * p * q + C * q**2)
)
assert zero(
    maximal_minor(mats[1], (1, 2, 3, 4, 5))
    - 72 * C**2 * (C + T) ** 2
)
_, _, _, mats = matrices(
    p * ell, ell * (-4 * B * p**2 + B * p * q + C * q**2)
)
assert zero(
    maximal_minor(mats[1], (1, 2, 3, 4, 5))
    + 648 * C**3 * (5 * B - C)
)
print("PASS every boundary-orbit exact-delta=2 incidence has {1,1} shape")


# ---------------------------------------------------------------------------
# Squarefree interior.  Put
#   h=(p-sq)(sp-q),  s != 0, s^2 != 1.
# This differs from p^2+eta*pq+q^2 by a nonzero scalar and has
# eta=-(s+s^{-1}), hence kappa=eta^2.
# ---------------------------------------------------------------------------

s = sp.symbols("s")
L = p - s * q
M = s * p - q
h_s = sp.expand(L * M)

# One fixed root occurs with multiplicity at least two in R.
_, _, _, mats = matrices(h_s, L**2 * (A * p + B * q))
left_contact = 5 * A * s**2 - 3 * A - 4 * B * s
right_contact = 4 * A * s + 3 * B * s**2 - 5 * B
expected = (
    -216
    * (A + B * s) ** 2
    * (s - 1) ** 2
    * (s + 1) ** 2
    * right_contact
    * left_contact
)
assert zero(maximal_minor(mats[1], (0, 1, 2, 3, 4)) - expected)

# Both simple fixed roots occur in R.
_, _, _, mats = matrices(h_s, h_s * (A * p + B * q))
left_contact = A * s**2 + A - 4 * B * s
right_contact = -4 * A * s + B * s**2 + B
expected = (
    -8
    * s**5
    * (A + B * s)
    * (A * s + B)
    * (s - 1) ** 2
    * (s + 1) ** 2
    * right_contact
    * left_contact
)
assert zero(maximal_minor(mats[1], (0, 1, 2, 3, 4)) - expected)

# One simple fixed root and contact at p=0.  Exact delta=2 removes every
# displayed factor except (s^2-3).  Thus kappa=16/3 is precisely the
# additional {2,0} modulus for this incidence type.
R_root_contact = sp.expand(
    L * (A * p**2 + (1 - 3 * s**2) * T * p * q + 4 * s * T * q**2)
)
_, _, _, mats = matrices(h_s, R_root_contact)
other_root = A + T * s**3 + T * s
chosen_root_simple = -A * s + 3 * T * s**2 - 5 * T
opposite_contact = (
    A * s**2 - 3 * A + 12 * T * s**3 - 4 * T * s
)
expected = (
    72
    * (s - 1) ** 2
    * (s + 1) ** 2
    * (s**2 - 3)
    * other_root**2
    * chosen_root_simple
    * opposite_contact
)
assert zero(maximal_minor(mats[1], (0, 1, 2, 3, 4)) - expected)
for rows in itertools.combinations(range(6), 5):
    assert zero(maximal_minor(mats[1], rows).subs(s**2, 3))

# Both ramification contacts.  There is only one possibly nonzero maximal
# minor because the first and last coefficient rows vanish.  Its two new
# factors are equivalent to kappa=16.
D = sp.symbols("D")
R_two_contacts = sp.expand(
    4 * s * A * p**3
    - 3 * (1 + s**2) * A * p**2 * q
    - 3 * (1 + s**2) * D * p * q**2
    + 4 * s * D * q**3
)
_, _, _, mats = matrices(h_s, R_two_contacts)
root_L = A * s**3 - 3 * A * s - 3 * D * s**2 + D
root_M = -3 * A * s**2 + A + D * s**3 - 3 * D * s
expected = (
    648
    * (s - 1) ** 2
    * (s + 1) ** 2
    * (s**2 - 4 * s + 1)
    * (s**2 + 4 * s + 1)
    * root_M**2
    * root_L**2
)
assert zero(maximal_minor(mats[1], (1, 2, 3, 4, 5)) - expected)
assert all(
    zero(maximal_minor(mats[1], rows))
    for rows in itertools.combinations(range(7), 5)
    if rows != (1, 2, 3, 4, 5)
)
print("PASS squarefree-interior maximal-minor factorization")


# ---------------------------------------------------------------------------
# Doubled nonbranch root h=(p+q)^2.
# ---------------------------------------------------------------------------

# If R contains the doubled fixed root once, exact delta=2 forces this
# minor nonzero.
_, _, _, mats = matrices(
    ell**2, ell * (A * p**2 + B * p * q + C * q**2)
)
assert zero(
    maximal_minor(mats[1], (0, 1, 2, 3, 4))
    + 512 * (A - 2 * B) * (2 * B - C) * (A - B + C) ** 2
)

# Otherwise the doubled fixed root contributes one and one ramification
# contact contributes the second.  The final factor is a genuine {2,0}
# sublocus, not another gcd factor.
_, _, _, mats = matrices(
    ell**2,
    a * p**3 + b * p**2 * q + sp.Rational(3, 2) * d * p * q**2 + d * q**3,
)
expected = (
    576
    * (3 * a - 2 * b)
    * (2 * a - 2 * b + d) ** 2
    * (6 * a - 5 * b + 3 * d)
)
assert zero(maximal_minor(mats[1], (0, 1, 2, 3, 4)) - expected)

d_exceptional = (5 * b - 6 * a) / 3
exceptional_double_R = sp.expand(
    a * p**3
    + b * p**2 * q
    + sp.Rational(3, 2) * d_exceptional * p * q**2
    + d_exceptional * q**3
)
_, _, _, exceptional_double_mats = matrices(ell**2, exceptional_double_R)
double_kernel = sp.Matrix([6, 4, 0, -2, 6 * a - b])
assert exceptional_double_mats[1] * double_kernel == sp.zeros(7, 1)
print("PASS doubled-root exact-delta=2 exceptional {2,0} sublocus")


# ---------------------------------------------------------------------------
# Mandatory literal regressions for all three {2,0} mechanisms.
# ---------------------------------------------------------------------------

# kappa=16, both ramification contacts.  This is the rational example
# mandated by the hostile correction.
h_16 = p**2 + 4 * p * q + q**2
R_16 = p**3 + 3 * p**2 * q + 6 * p * q**2 + 2 * q**3
alpha, beta, gamma, mats_16 = matrices(h_16, R_16)
assert gcd3(alpha, beta, gamma) == 2 * p * q
assert total_degree(gcd3(alpha, beta, gamma)) == 2
assert sp.factor(
    sp.resultant(h_16.subs(q, 1), R_16.subs(q, 1), p)
) == -18
assert tuple(matrix.rank() for matrix in mats_16) == (2, 4, 6)
kernel_16 = sp.Matrix([-5, -1, 1, 5, 3])
assert mats_16[1] * kernel_16 == sp.zeros(7, 1)

# kappa=16/3, one fixed root and one ramification contact.  Work over
# Q(sqrt(3)); eta=4*sqrt(3)/3.
sqrt3 = sp.sqrt(3)
eta_root_contact = 4 * sqrt3 / 3
h_root_contact = p**2 + eta_root_contact * p * q + q**2
R_root_contact_literal = (
    8 * p**2 * q + 12 * sqrt3 * p * q**2 + 12 * q**3
)
alpha, beta, gamma, mats_root_contact = matrices(
    h_root_contact, R_root_contact_literal
)
gcd_root_contact = sp.gcd(
    sp.gcd(
        sp.Poly(alpha, p, q, extension=sqrt3),
        sp.Poly(beta, p, q, extension=sqrt3),
    ),
    sp.Poly(gamma, p, q, extension=sqrt3),
)
assert zero(
    gcd_root_contact.as_expr() - p * (p + sqrt3 * q)
)
assert tuple(matrix.rank() for matrix in mats_root_contact) == (2, 4, 6)
kernel_root_contact = sp.Matrix(
    [-eta_root_contact, -1, 0, 1, 4]
)
assert mats_root_contact[1] * kernel_root_contact == sp.zeros(7, 1)

# kappa=4, doubled fixed root plus one ramification contact.
h_4 = (p + q) ** 2
R_4 = 6 * p**2 * q + 15 * p * q**2 + 10 * q**3
alpha, beta, gamma, mats_4 = matrices(h_4, R_4)
assert gcd3(alpha, beta, gamma) == 2 * p * (p + q)
assert total_degree(gcd3(alpha, beta, gamma)) == 2
assert sp.resultant(h_4.subs(q, 1), R_4.subs(q, 1), p) == 1
assert tuple(matrix.rank() for matrix in mats_4) == (2, 4, 6)
kernel_4 = sp.Matrix([-3, -2, 0, 1, 3])
assert mats_4[1] * kernel_4 == sp.zeros(7, 1)

print("PASS literal kappa=16, 16/3, and 4 {2,0} regressions")
print("ALL EXACT DELTA=2 HILBERT--BURCH STRATIFICATION CHECKS PASSED")
