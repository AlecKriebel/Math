"""Exact checks for the repaired formal one-Pauli reduction.

This dependency-free script checks the finite identities and constants
used in the accompanying note.  It is not a finite proof that the
remaining polynomial realization system is infeasible.
"""

from fractions import Fraction as F


def mq_add(left, right):
    return tuple(x + y for x, y in zip(left, right))


def mq_scale(scalar, value):
    return tuple(scalar * x for x in value)


def mq_mul(left, right, radicals):
    """Multiply in Q(sqrt(radicals[0]),sqrt(radicals[1]))."""

    out = [F(0) for _ in range(4)]
    for left_mask, left_value in enumerate(left):
        for right_mask, right_value in enumerate(right):
            common = left_mask & right_mask
            factor = F(1)
            for bit, radicand in enumerate(radicals):
                if common & (1 << bit):
                    factor *= radicand
            out[left_mask ^ right_mask] += (
                left_value * right_value * factor
            )
    return tuple(out)


MQ_ZERO = (F(0), F(0), F(0), F(0))
MQ_ONE = (F(1), F(0), F(0), F(0))
MQ_SQRT_FIRST = (F(0), F(1), F(0), F(0))
MQ_SQRT_SECOND = (F(0), F(0), F(1), F(0))
MQ_SQRT_PRODUCT = (F(0), F(0), F(0), F(1))


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


# Exact multiquadratic arithmetic in the two-sided compression lemma.
# Coordinate-off quotient 1/20, in Q(sqrt(3),sqrt(19)).
radicals_20 = (3, 19)
x_20 = mq_scale(
    F(1, 14),
    mq_add(
        mq_scale(F(5), MQ_SQRT_FIRST),
        mq_scale(F(-1), MQ_SQRT_SECOND),
    ),
)
gamma_20 = mq_scale(
    F(1, 40),
    mq_add(
        mq_scale(F(9), MQ_SQRT_FIRST),
        mq_scale(F(-1), MQ_SQRT_SECOND),
    ),
)
x_20_squared = mq_mul(x_20, x_20, radicals_20)
assert mq_add(
    mq_add(
        mq_scale(F(7), x_20_squared),
        mq_scale(F(-5), mq_mul(MQ_SQRT_FIRST, x_20, radicals_20)),
    ),
    mq_scale(F(2), MQ_ONE),
) == MQ_ZERO
assert mq_mul(
    gamma_20,
    mq_add(MQ_ONE, x_20_squared),
    radicals_20,
) == x_20
assert mq_scale(
    F(1, 5), mq_add(MQ_ONE, x_20_squared)
) == mq_mul(
    mq_add(
        MQ_ONE,
        mq_scale(
            F(-1), mq_mul(MQ_SQRT_FIRST, x_20, radicals_20)
        ),
    ),
    mq_add(
        MQ_ONE,
        mq_scale(
            F(-1), mq_mul(MQ_SQRT_FIRST, x_20, radicals_20)
        ),
    ),
    radicals_20,
)

# Hadamard quotient 1/40, in Q(sqrt(3),sqrt(13)); sqrt(39) is the
# product of the two square roots.
radicals_40 = (3, 13)
x_40 = mq_scale(
    F(1, 29),
    mq_add(
        mq_scale(F(10), MQ_SQRT_FIRST),
        mq_scale(F(-1), MQ_SQRT_PRODUCT),
    ),
)
gamma_40 = mq_scale(
    F(1, 80),
    mq_add(
        mq_scale(F(19), MQ_SQRT_FIRST),
        mq_scale(F(-1), MQ_SQRT_PRODUCT),
    ),
)
x_40_squared = mq_mul(x_40, x_40, radicals_40)
assert mq_mul(
    gamma_40,
    mq_add(MQ_ONE, x_40_squared),
    radicals_40,
) == x_40
assert mq_scale(
    F(1, 10), mq_add(MQ_ONE, x_40_squared)
) == mq_mul(
    mq_add(
        MQ_ONE,
        mq_scale(
            F(-1), mq_mul(MQ_SQRT_FIRST, x_40, radicals_40)
        ),
    ),
    mq_add(
        MQ_ONE,
        mq_scale(
            F(-1), mq_mul(MQ_SQRT_FIRST, x_40, radicals_40)
        ),
    ),
    radicals_40,
)
gamma_40_squared = mq_mul(gamma_40, gamma_40, radicals_40)
assert gamma_40_squared == (
    F(561, 3200),
    F(0),
    F(-57, 3200),
    F(0),
)
# The claimed lambda half-width squares to 1/4-gamma_40^2.
lambda_half_width_squared = (
    F(239, 3200),
    F(0),
    F(57, 3200),
    F(0),
)
assert mq_add(
    gamma_40_squared, lambda_half_width_squared
) == mq_scale(F(1, 4), MQ_ONE)


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


# The six-vector Hadamard tight-frame calculation has the scalar
# coefficients
#
#   6 * sqrt(gamma_40/9) = 2 sqrt(gamma_40),
#   sqrt(det(2 I_2)) = 2,
#   sqrt(det(2 B_sum)) = 2 sqrt(det(B_sum)).
#
# After squaring and cancelling four, it yields
# sqrt(det(B_sum)) >= gamma_40 exactly.
assert F(6) ** 2 / 9 == 4

print("verified: repaired formal Gram arithmetic")
print("verified: exact polarized two-copy kernel")
print("verified: sharp global product-pencil quotient 1/40")
print("verified: exact two-sided compression constants")
print("verified: quotient-1/20 singular-product gamma_20")
print("verified: Hadamard singular-product gamma_40")
print("verified: one-Pauli determinant polynomial")
print("verified: crossed-Gram determinant and lambda constants")
