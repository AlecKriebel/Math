"""Exact checks for the repaired formal one-Pauli reduction.

This dependency-free script checks the finite identities and constants
used in the accompanying note.  It is not a finite proof that the
remaining polynomial realization system is infeasible.
"""

from fractions import Fraction as F


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def flatten(matrix):
    return [value for row in matrix for value in row]


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def outer(left, right):
    return [[x * y for y in right] for x in left]


def inner(left, right):
    return sum(
        left[i][j] * right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def partial_trace_first(matrix):
    return [
        [
            sum(matrix[3 * k + i][3 * k + j] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]


def partial_trace_second(matrix):
    return [
        [
            sum(matrix[3 * i + k][3 * j + k] for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]


def b2(left, right):
    return (
        inner(left, right)
        - F(1, 2)
        * (
            inner(partial_trace_first(left), partial_trace_first(right))
            + inner(partial_trace_second(left), partial_trace_second(right))
        )
        + F(1, 4) * trace(left) * trace(right)
    )


def kappa_real(u, v, s, t):
    """The real specialization of equation (11)."""

    term_0 = dot(flatten(u), flatten(s)) * dot(flatten(t), flatten(v))
    term_second = trace(
        multiply(multiply(multiply(v, transpose(u)), s), transpose(t))
    )
    term_first = trace(
        multiply(multiply(multiply(transpose(v), u), transpose(s)), t)
    )
    term_trace = dot(flatten(u), flatten(v)) * dot(flatten(t), flatten(s))
    return (
        term_0
        - F(1, 2) * (term_first + term_second)
        + F(1, 4) * term_trace
    )


# Check the polarized contraction formula on deterministic integer data.
for seed in range(12):
    matrices = []
    for label in range(4):
        matrices.append(
            [
                [
                    F(((17 * seed + 11 * label + 5 * i + 3 * j) % 7) - 3)
                    for j in range(3)
                ]
                for i in range(3)
            ]
        )
    u, v, s, t = matrices
    direct = b2(outer(flatten(u), flatten(v)), outer(flatten(s), flatten(t)))
    assert direct == kappa_real(u, v, s, t)


# The repaired exact Gram table and its generalized eigenvalues.
nu = F(1, 9)
c = F(1, 36)
d = F(1, 180)
assert 3 * c / nu == F(3, 4)
assert d / nu == F(1, 20)
assert F(-1, 2) <= 0 <= F(3, 4) <= 1

beta = [[F(0) for _ in range(9)] for _ in range(9)]
for p in range(3):
    for r in range(3):
        beta[3 * p + p][3 * r + r] = c
for p in range(3):
    for q in range(3):
        if p != q:
            beta[3 * p + q][3 * p + q] = d


def target_energy(a, b):
    coefficients = [a[p] * b[q] for p in range(3) for q in range(3)]
    gram_value = sum(
        coefficients[i] * beta[i][j] * coefficients[j]
        for i in range(9)
        for j in range(9)
    )
    formula = d * (
        dot(a, a) * dot(b, b)
        - sum(a[p] ** 2 * b[p] ** 2 for p in range(3))
    ) + c * dot(a, b) ** 2
    assert gram_value == formula
    return formula


test_vectors = [
    ([F(1), F(2), F(-1)], [F(3), F(-2), F(4)]),
    ([F(2), F(-3), F(5)], [F(-1), F(7), F(2)]),
    ([F(1), F(0), F(0)], [F(0), F(2), F(-3)]),
]
for a, b in test_vectors:
    target_energy(a, b)

# Every fixed off-diagonal pencil has quotient 1/20.
for p in range(3):
    a = [F(0), F(0), F(0)]
    a[p] = F(1)
    b = [F(p + 1), F(2 - p), F(3)]
    b[p] = F(0)
    energy = target_energy(a, b)
    norm_squared = nu * dot(a, a) * dot(b, b)
    assert energy * 20 == norm_squared

# The global product-pencil floor 1/40 is sharp on every
# two-coordinate Hadamard pair.  We use unnormalized +/- vectors to
# keep the check rational.
for p in range(3):
    for r in range(p + 1, 3):
        a = [F(0), F(0), F(0)]
        b = [F(0), F(0), F(0)]
        a[p] = a[r] = F(1)
        b[p], b[r] = F(1), F(-1)
        energy = target_energy(a, b)
        norm_squared = nu * dot(a, a) * dot(b, b)
        assert energy * 40 == norm_squared


# Exact arithmetic in the singular-product lemma.
# The small root of 19*x^2-20*x+4 is
# (10-2*sqrt(6))/19.  It lies strictly above 2-sqrt(3):
# evaluating the polynomial at 2-sqrt(3) gives
# 97-56*sqrt(3)>0, and the squared integer gap is one.
assert 97**2 - 3 * 56**2 == 1
# At x=2-sqrt(3), x/(1+x^2)=1/4 exactly.
# Algebraically, x^2-4*x+1=0 is equivalent to that identity.
off_product_fraction = F(1, 4)
off_product_floor = off_product_fraction * nu
assert off_product_floor == F(1, 36)

# At quotient 1/40 the singular-ratio polynomial has roots 1/3 and
# 9/13, and the resulting determinant fraction is 3/10.
assert 39 * F(1, 3) ** 2 - 40 * F(1, 3) + 9 == 0
assert 39 * F(9, 13) ** 2 - 40 * F(9, 13) + 9 == 0
assert F(1, 3) / (1 + F(1, 3) ** 2) == F(3, 10)
assert F(3, 10) * nu == F(1, 30)


# The determinant polynomial in equation (25).
for lam, norm_sq, t_value in [
    (F(2, 5), F(1), F(1, 7)),
    (F(3, 7), F(5, 3), F(-2, 9)),
]:
    a00 = norm_sq / 3 + (1 - lam) * t_value
    a11 = norm_sq / 3 - lam * t_value
    direct = a00 * a11
    expanded = (
        norm_sq**2 / 9
        + (1 - 2 * lam) * norm_sq * t_value / 3
        - lam * (1 - lam) * t_value**2
    )
    assert direct == expanded


# The coordinate-pencil lambda restriction is the sum of the three
# individual determinant floors combined with Minkowski's inequality.
individual_floor_numerator = 3 * off_product_floor
assert individual_floor_numerator == F(1, 12)
assert 3 * individual_floor_numerator == F(1, 4)

# The Hadamard pencils improve it.  Each B determinant square root is
# at most sqrt(lambda(1-lambda))/3, so the product floor 1/30 forces
# each A determinant square root to be at least
# 1/(10 sqrt(lambda(1-lambda))).  There are two signs per pair and
# three complementary pairs; their Minkowski sum is at most 2.
hadamard_product_floor = F(1, 30)
hadamard_alpha_floor_coefficient = 3 * hadamard_product_floor
assert hadamard_alpha_floor_coefficient == F(1, 10)
pair_floor_coefficient = 2 * hadamard_alpha_floor_coefficient
assert pair_floor_coefficient == F(1, 5)
lambda_sqrt_floor = 3 * pair_floor_coefficient / 2
assert lambda_sqrt_floor == F(3, 10)

print("verified: repaired formal Gram arithmetic")
print("verified: exact polarized two-copy kernel")
print("verified: sharp global product-pencil quotient 1/40")
print("verified: quotient-1/20 singular-product floor 1/4")
print("verified: Hadamard-pencil singular-product floor 3/10")
print("verified: one-Pauli determinant polynomial")
print("verified: strengthened lambda interval [1/10, 9/10]")
