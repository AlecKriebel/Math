#!/usr/bin/env python3
"""Exact E6 contact certificates on the first delta=1 components."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, b, c, d, kappa, eta = sp.symbols("a b c d kappa eta")
variables = (p, q, r)


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def jac3(f, g, h):
    return sp.expand(
        sp.Matrix(
            [
                [sp.diff(value, variable) for variable in variables]
                for value in (f, g, h)
            ]
        ).det()
    )


def coefficient_vector(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return sp.Matrix(
        [
            poly.coeff_monomial(p**i * q ** (degree - i))
            for i in range(degree, -1, -1)
        ]
    )


def contact_data(h, R, N):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
    u, v, t = N
    assert zero(alpha * u + beta * v + gamma * t)
    curvature = sp.expand(
        jac3(P, r * v, r * t)
        + jac3(r * u, Q, r * t)
        + jac3(r * u, r * v, R)
    )
    assert zero(sp.Poly(curvature, r).coeff_monomial(1))
    K = sp.expand(sp.Poly(curvature, r).coeff_monomial(r))
    matrix = sp.Matrix.hstack(
        coefficient_vector(alpha, 5),
        coefficient_vector(beta, 5),
        coefficient_vector(K, 5),
    )
    return P, Q, alpha, beta, gamma, K, matrix


def minor(matrix, rows):
    return sp.factor(matrix.extract(rows, range(3)).det())


# h=pq, a=0.  A nonzero contact multiplier first forces b=0 and
# then c=0, which is the deeper R=dq^3 stratum.
R_pq = b * p**2 * q + c * p * q**2 + d * q**3
data_pq = contact_data(
    p * q, R_pq, (3 * p**2, q**2, 2 * b * p + c * q)
)
K_pq, matrix_pq = data_pq[-2:]
assert zero(K_pq - 2 * p * q**2 * (
    7 * b * p**2 + 3 * c * p * q - 9 * d * q**2
))
assert zero(minor(matrix_pq, (1, 2, 3)) - 70 * b**3)
assert zero(
    minor(matrix_pq, (2, 3, 4))
    - 6 * c * (54 * b * d + 5 * c**2)
)
assert zero(minor(matrix_pq, (2, 3, 4)).subs(b, 0) - 30 * c**3)
print("PASS delta=1 pq component routes nonzero contact to deeper stratum")


# h=p(p+q), d=0.  Off the other determinant component S=3a-4b=0,
# three literal contact minors force c=b=a=0.
R_d0 = a * p**3 + b * p**2 * q + c * p * q**2
data_d0 = contact_data(
    p * (p + q),
    R_d0,
    (p**2, q * (2 * p + 3 * q), b * p + 2 * c * q),
)
matrix_d0 = data_d0[-1]
S = 3 * a - 4 * b
assert zero(minor(matrix_d0, (0, 3, 4)) + 14 * c**2 * S)
assert zero(minor(matrix_d0, (1, 2, 3)).subs(c, 0) - 30 * b**3)
assert zero(
    minor(matrix_d0, (0, 1, 2)).subs({b: 0, c: 0}) - 486 * a**3
)
print("PASS delta=1 one-branch root component obstruction")


# The ramification-contact component 3a=4b and the fixed-root component
# each have a decisive d^3 minor away from d=0.
R_split = (
    a * p**3 + sp.Rational(3, 4) * a * p**2 * q
    + c * p * q**2 + d * q**3
)
data_split = contact_data(
    p * (p + q),
    R_split,
    (
        6 * p**2,
        -16 * p**2 - 20 * p * q + 2 * q**2,
        (3 * a - 16 * c) * p + 2 * (c - 12 * d) * q,
    ),
)
assert zero(minor(data_split[-1], (3, 4, 5)) - 1944 * d**3)

R_fixed = (
    a * p**3 + b * p**2 * q + (-a + b + d) * p * q**2 + d * q**3
)
data_fixed = contact_data(
    p * (p + q),
    R_fixed,
    (
        -3 * p**2,
        2 * p * q - q**2,
        (-3 * a + b) * p + (a - b + 2 * d) * q,
    ),
)
assert zero(minor(data_fixed[-1], (3, 4, 5)) - 486 * d**3)
print("PASS other one-branch delta=1 components route to intersections")


# The branch-square component has a genuine contact survivor.  Its contact
# minors force c=a=0 when d != 0, rather than killing the tangent.
R_square = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3
N_square = (
    12 * d * p**2,
    -2 * c * p * q + 6 * d * q**2,
    (9 * d * a - c * b) * p + 2 * (3 * d * b - c**2) * q,
)
data_square = contact_data(p**2, R_square, N_square)
matrix_square = data_square[-1]
assert zero(minor(matrix_square, (2, 3, 4)) - 15552 * c * d**4)
assert zero(
    minor(matrix_square, (1, 2, 4))
    + 576 * d**2 * (27 * a * d**2 - 10 * c**3)
)

R_survive = b * p**2 * q + d * q**3
survive = contact_data(
    p**2, R_survive, (2 * p**2, q**2, b * q)
)
alpha_survive, K_survive = survive[2], survive[-2]
assert zero(K_survive + 2 * alpha_survive)

# Complete top-three family.  The chosen invertible L exposes a nonzero E5,
# so this is not promoted to a Keller map.
H4 = sp.Matrix([p**4, p**2 * q**2, 0])
H3 = sp.Matrix(
    [2 * kappa * r * p**2, kappa * r * q**2, R_survive]
)
H2 = sp.Matrix([kappa**2 * r**2, 0, kappa * b * q * r])
L0 = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
weighted = sp.Poly(
    sp.expand(
        (
            L0
            + z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
assert L0.det() == -1
for degree in (8, 7, 6):
    assert zero(weighted.coeff_monomial(z**degree))
assert zero(
    weighted.coeff_monomial(z**5)
    + 4 * p**3 * (b * p**2 + 3 * d * q**2)
)
assert not zero(weighted.coeff_monomial(z**5))
print("PASS exact branch-square E6 survivor, explicitly rejected at E5")


# Interior ramification-contact component 3*a*eta=4*b.  The p^5
# coefficient first forces F=0.  Off the opposite contact component, the
# q^5 coefficient fixes the alpha multiplier, leaving a two-column
# dependence test between beta and K+8*eta^2*alpha.
R_interior_left = (
    a * p**3 + sp.Rational(3, 4) * a * eta * p**2 * q
    + c * p * q**2 + d * q**3
)
N_interior_left = (
    2 * (3 * eta**2 - 8) * p**2 + 4 * eta * p * q,
    -16 * p**2 - 20 * eta * p * q
    + 2 * (eta**2 - 16) * q**2,
    (3 * eta**2 * a - 16 * c) * p
    + 2 * (eta * c - 12 * d) * q,
)
data_interior_left = contact_data(
    p**2 + eta * p * q + q**2,
    R_interior_left,
    N_interior_left,
)
alpha_left, beta_left, K_left = (
    data_interior_left[2],
    data_interior_left[3],
    data_interior_left[-2],
)
alpha_vector = coefficient_vector(alpha_left, 5)
beta_vector = coefficient_vector(beta_left, 5)
K_vector = coefficient_vector(K_left, 5)
F_contact = 7 * a * eta**3 - 48 * a * eta + 48 * c * eta - 64 * d
assert zero(K_vector[0] - 24 * F_contact)
d_contact = sp.Rational(1, 64) * (
    7 * a * eta**3 - 48 * a * eta + 48 * c * eta
)
alpha_contact = alpha_vector.subs(d, d_contact)
beta_contact = beta_vector.subs(d, d_contact)
K_contact = K_vector.subs(d, d_contact)
opposite_contact = 4 * c - 3 * d_contact * eta
assert zero(alpha_contact[5] + opposite_contact)
assert zero(beta_contact[5])
assert zero(K_contact[5] - 8 * eta**2 * opposite_contact)
residual = sp.expand(K_contact + 8 * eta**2 * alpha_contact)


def wedge(vector1, vector2, i, j):
    return sp.factor(vector1[i] * vector2[j] - vector1[j] * vector2[i])


# In the chart a != 0, scale a=1 and write c=tt.  Three literal wedges
# have resultants whose gcd is eta^2, so a contact has eta=0.
tt = sp.symbols("tt")
w12 = sp.cancel(wedge(residual, beta_contact, 1, 2) / eta)
w13 = sp.cancel(wedge(residual, beta_contact, 1, 3) / eta**2)
w34 = sp.cancel(wedge(residual, beta_contact, 3, 4) / eta)
w12_chart = sp.factor(w12.subs({a: 1, c: tt}))
w13_chart = sp.factor(w13.subs({a: 1, c: tt}))
w34_chart = sp.factor(w34.subs({a: 1, c: tt}))
resultant_12_13 = sp.factor(sp.resultant(w12_chart, w13_chart, tt))
resultant_12_34 = sp.factor(sp.resultant(w12_chart, w34_chart, tt))
assert sp.factor(sp.gcd(resultant_12_13, resultant_12_34) - eta**2) == 0

# In the remaining chart a=0, the open opposite-contact condition makes
# c nonzero, so scale c=1.  These incompatible factors again force eta=0.
assert zero(
    wedge(residual, beta_contact, 1, 2).subs({a: 0, c: 1})
    - 192 * eta * (7 * eta**2 - 48)
)
assert zero(
    wedge(residual, beta_contact, 1, 3).subs({a: 0, c: 1})
    - 48 * eta**2 * (13 * eta**2 - 120)
)

# At eta=0, b=d=0 and the normalized tangent really survives:
# K=-2*beta.  A full sparse completion kills E8,E7,E6 but not E5.
R_interior_survive = a * p**3 + c * p * q**2
N_interior_survive = (p**2, p**2 + 2 * q**2, c * p)
interior_survive = contact_data(
    p**2 + q**2, R_interior_survive, N_interior_survive
)
assert zero(interior_survive[-2] + 2 * interior_survive[3])
H4_interior = sp.Matrix(
    [(p**2 + q**2) * p**2, (p**2 + q**2) * q**2, 0]
)
H3_interior = sp.Matrix(
    [
        kappa * r * p**2,
        kappa * r * (p**2 + 2 * q**2),
        R_interior_survive,
    ]
)
H2_interior = sp.Matrix([0, kappa**2 * r**2, kappa * c * p * r])
weighted_interior = sp.Poly(
    sp.expand(
        (
            L0
            + z * H2_interior.jacobian(variables)
            + z**2 * H3_interior.jacobian(variables)
            + z**3 * H4_interior.jacobian(variables)
        ).det()
    ),
    z,
)
for degree in (8, 7, 6):
    assert zero(weighted_interior.coeff_monomial(z**degree))
assert zero(
    weighted_interior.coeff_monomial(z**5)
    + 2 * p * (
        (-3 * a + 4 * c) * p**3 * q
        + c * p * q**3
        + 2 * kappa * (p**2 + q**2) ** 2
    )
)
assert not zero(weighted_interior.coeff_monomial(z**5))
print("PASS interior contact is eta=0; exact survivor rejected at E5")


# Common-root component.  Parameterize the chosen root by L=p-s*q:
# h=L*(s*p-q), R=L*S.  The tangent is the derivative in the direction
# tangent to L=0, divided by L.
s, A, B, C = sp.symbols("s A B C")
common_linear = p - s * q
other_linear = s * p - q
h_common = sp.expand(common_linear * other_linear)
S_common = A * p**2 + B * p * q + C * q**2
R_common = sp.expand(common_linear * S_common)
P_common = sp.expand(h_common * p**2)
Q_common = sp.expand(h_common * q**2)
N_common = tuple(
    sp.cancel(
        (s * sp.diff(value, p) + sp.diff(value, q)) / common_linear
    )
    for value in (P_common, Q_common, R_common)
)
common_data = contact_data(h_common, R_common, N_common)
alpha_common, beta_common, K_common = (
    common_data[2],
    common_data[3],
    common_data[-2],
)
alpha_reduced = sp.cancel(alpha_common / common_linear)
beta_reduced = sp.cancel(beta_common / common_linear)
K_reduced = sp.cancel(K_common / common_linear)
X_common = A * s**2 - 3 * A - 4 * B * s
Y_common = 4 * B * s + 3 * C * s**2 - C
S_at_common = A * s**2 + B * s + C
assert zero(alpha_reduced.subs({p: 1, q: 0}))
assert zero(beta_reduced.subs({p: 1, q: 0}) - X_common)
assert zero(K_reduced.subs({p: 1, q: 0}) + 2 * s * X_common)
assert zero(alpha_reduced.subs({p: 0, q: 1}) + Y_common)
assert zero(beta_reduced.subs({p: 0, q: 1}))
assert zero(K_reduced.subs({p: 0, q: 1}) - 2 * s * Y_common)
assert zero(
    alpha_reduced.subs({p: s, q: 1})
    + (s**2 - 1) * S_at_common
)
assert zero(
    beta_reduced.subs({p: s, q: 1})
    - s**2 * (s**2 - 1) * S_at_common
)
assert zero(
    K_reduced.subs({p: s, q: 1})
    - 12 * s * (s**2 - 1) ** 2 * S_at_common
)
print("PASS common-root contact evaluation routes to a deeper intersection")


# Doubled nonbranch root h=(p+q)^2.  Alpha and beta are divisible by
# p+q, while the contact curvature has the displayed nonzero remainder
# unless R also contains that root (the deeper common-root intersection).
delta_square = a - b + c - d
R_nonbranch_square = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3
N_nonbranch_square = (
    (6 * a - 8 * b + 10 * c - 12 * d) * p**2
    + (-2 * b + 4 * c - 6 * d) * p * q,
    (6 * a - 4 * b + 2 * c) * p * q
    + (12 * a - 10 * b + 8 * c - 6 * d) * q**2,
    ((6 * c - 9 * d) * a - 2 * b**2 + b * c) * p
    + (9 * d * a - (c + 6 * d) * b + 2 * c**2) * q,
)
square_data = contact_data(
    (p + q) ** 2, R_nonbranch_square, N_nonbranch_square
)
assert zero(sp.rem(square_data[2], p + q, p))
assert zero(sp.rem(square_data[3], p + q, p))
assert zero(
    sp.rem(square_data[-2], p + q, p)
    + 324 * q**5 * delta_square**3
)
print("PASS doubled nonbranch-root delta=1 open stratum is E6-obstructed")

print("ALL DELTA=1 E6 CONTACT CERTIFICATES PASSED")
