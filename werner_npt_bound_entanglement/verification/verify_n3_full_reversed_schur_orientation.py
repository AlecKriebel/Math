#!/usr/bin/env python3
"""Dependency-free exact audit of the reversed-Schur orientation identity."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

G = tuple[F, F]
Z: G = (F(0), F(0))
O: G = (F(1), F(0))


def g(re: int | F = 0, im: int | F = 0) -> G:
    return (F(re), F(im))


def add(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def neg(x: G) -> G:
    return (-x[0], -x[1])


def sub(x: G, y: G) -> G:
    return add(x, neg(y))


def mul(x: G, y: G) -> G:
    return (x[0] * y[0] - x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def conj(x: G) -> G:
    return (x[0], -x[1])


def div(x: G, y: G) -> G:
    denominator = y[0] * y[0] + y[1] * y[1]
    numerator = mul(x, conj(y))
    return (numerator[0] / denominator, numerator[1] / denominator)


def matmul(a: list[list[G]], b: list[list[G]]) -> list[list[G]]:
    return [
        [
            sum_g(mul(a[i][k], b[k][j]) for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def sum_g(values) -> G:
    out = Z
    for value in values:
        out = add(out, value)
    return out


def dagger(a: list[list[G]]) -> list[list[G]]:
    return [
        [conj(a[j][i]) for j in range(len(a))]
        for i in range(len(a[0]))
    ]


def trace(a: list[list[G]]) -> G:
    return sum_g(a[i][i] for i in range(len(a)))


def det2(a: list[list[G]]) -> G:
    return sub(mul(a[0][0], a[1][1]), mul(a[0][1], a[1][0]))


def inv2(a: list[list[G]]) -> list[list[G]]:
    determinant = det2(a)
    return [
        [div(a[1][1], determinant), div(neg(a[0][1]), determinant)],
        [div(neg(a[1][0]), determinant), div(a[0][0], determinant)],
    ]


def permutation_sign(p: tuple[int, ...]) -> int:
    inversions = sum(
        p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))
    )
    return -1 if inversions % 2 else 1


def determinant(a: list[list[G]]) -> G:
    n = len(a)
    return sum_g(
        (lambda term, sign: term if sign == 1 else neg(term))(
            product(a[i][p[i]] for i in range(n)),
            permutation_sign(p),
        )
        for p in permutations(range(n))
    )


def product(values) -> G:
    out = O
    for value in values:
        out = mul(out, value)
    return out


def block(a, b, c, d):
    return [
        a[0] + b[0],
        a[1] + b[1],
        c[0] + d[0],
        c[1] + d[1],
    ]


def hs_squared(a: list[list[G]]) -> G:
    return sum_g(mul(conj(value), value) for row in a for value in row)


def scalar_matrix(left: list[list[G]], right: list[list[G]]):
    return matmul(left, right)


# Section 1: a generic exact positive block matrix.
# Diagonal square entries make the normalized coherences rational.
a = [[g(4), Z], [Z, g(9)]]
d = [[g(16), Z], [Z, g(25)]]
b = [
    [g(F(1, 10)), g(F(1, 10), F(1, 10))],
    [g(F(1, 5), F(-1, 10)), g(F(-1, 10))],
]
k = block(a, b, dagger(b), d)
kgamma = block(a, dagger(b), b, d)

# Sylvester's criterion, checked exactly.
for size in range(1, 5):
    minor = determinant([row[:size] for row in k[:size]])
    assert minor[1] == 0 and minor[0] > 0

ainv = inv2(a)
dinv = inv2(d)

ordinary_trace = trace(matmul(dinv, matmul(dagger(b), matmul(ainv, b))))
reversed_trace = trace(matmul(dinv, matmul(b, matmul(ainv, dagger(b)))))
det_ad = mul(det2(a), det2(d))

orientation_identity_rhs = add(
    determinant(k),
    mul(det_ad, sub(ordinary_trace, reversed_trace)),
)
assert determinant(kgamma) == orientation_identity_rhs

# Normalized square roots are diag(2,3) and diag(4,5).
ainv_sqrt = [[g(F(1, 2)), Z], [Z, g(F(1, 3))]]
dinv_sqrt = [[g(F(1, 4)), Z], [Z, g(F(1, 5))]]
x = matmul(ainv_sqrt, matmul(b, dinv_sqrt))
z = matmul(ainv_sqrt, matmul(dagger(b), dinv_sqrt))
assert hs_squared(x) == ordinary_trace
assert hs_squared(z) == reversed_trace
assert mul(det_ad, sub(hs_squared(x), hs_squared(z))) == sub(
    determinant(kgamma), determinant(k)
)

i2 = [[O, Z], [Z, O]]
xdagger_x = matmul(dagger(x), x)
schur_slack = det2([
    [sub(i2[i][j], xdagger_x[i][j]) for j in range(2)]
    for i in range(2)
])
assert mul(det_ad, schur_slack) == determinant(k)
assert mul(
    det_ad,
    sub(schur_slack, sub(hs_squared(z), hs_squared(x))),
) == determinant(kgamma)

# Section 2: exact abstract obstruction K = I/2 + |Phi_2><Phi_2|.
a_star = [[g(F(3, 2)), Z], [Z, g(F(1, 2))]]
d_star = [[g(F(1, 2)), Z], [Z, g(F(3, 2))]]
b_star = [[Z, O], [Z, Z]]
k_star = block(a_star, b_star, dagger(b_star), d_star)
kgamma_star = block(a_star, dagger(b_star), b_star, d_star)

assert determinant(k_star) == g(F(5, 16))
assert determinant(kgamma_star) == g(F(-27, 16))

# Work without irrational square roots for the obstruction.
ordinary_star = trace(
    matmul(inv2(d_star), matmul(dagger(b_star), matmul(inv2(a_star), b_star)))
)
reversed_star = trace(
    matmul(inv2(d_star), matmul(b_star, matmul(inv2(a_star), dagger(b_star))))
)
det_ad_star = mul(det2(a_star), det2(d_star))
gamma_star = div(determinant(k_star), det_ad_star)
eta_star = sub(reversed_star, ordinary_star)
assert det_ad_star == g(F(9, 16))
assert gamma_star == g(F(5, 9))
assert eta_star == g(F(32, 9))
assert div(determinant(kgamma_star), det_ad_star) == sub(
    gamma_star, eta_star
)

# Section 3: the phase-Hermitian automatic chart has zero defect.
a_chart = [[g(2), g(F(1, 4))], [g(F(1, 4)), g(3)]]
d_chart = [[g(4), g(F(-1, 5))], [g(F(-1, 5)), g(5)]]
h_chart = [[g(F(1, 20)), g(F(1, 30), F(1, 40))],
           [g(F(1, 30), F(-1, 40)), g(F(-1, 25))]]
b_chart = [[mul(g(0, 1), value) for value in row] for row in h_chart]
ordinary_chart = trace(
    matmul(inv2(d_chart), matmul(dagger(b_chart), matmul(inv2(a_chart), b_chart)))
)
reversed_chart = trace(
    matmul(inv2(d_chart), matmul(b_chart, matmul(inv2(a_chart), dagger(b_chart))))
)
assert ordinary_chart == reversed_chart

print(
    "verified full reversed-Schur determinant identity, normalized "
    "orientation reduction, exact abstract obstruction, and automatic chart"
)
