#!/usr/bin/env python3
"""Exact verifier for the cofactor factor-floor obstruction.

The calculation takes place in Q(sqrt(2)), implemented below using only
the Python standard library.
"""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Qsqrt2:
    rational: F = F(0)
    radical: F = F(0)

    @staticmethod
    def coerce(value):
        if isinstance(value, Qsqrt2):
            return value
        return Qsqrt2(F(value), F(0))

    def __add__(self, other):
        other = self.coerce(other)
        return Qsqrt2(
            self.rational + other.rational,
            self.radical + other.radical,
        )

    __radd__ = __add__

    def __neg__(self):
        return Qsqrt2(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Qsqrt2(
            self.rational * other.rational
            + 2 * self.radical * other.radical,
            self.rational * other.radical
            + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        denominator = (
            other.rational * other.rational
            - 2 * other.radical * other.radical
        )
        numerator = self * Qsqrt2(other.rational, -other.radical)
        return Qsqrt2(
            numerator.rational / denominator,
            numerator.radical / denominator,
        )

    def __eq__(self, other):
        other = self.coerce(other)
        return (
            self.rational == other.rational
            and self.radical == other.radical
        )


ZERO = Qsqrt2()
ONE = Qsqrt2(F(1))
INV_SQRT2 = Qsqrt2(F(0), F(1, 2))


def zeros(rows, cols):
    return [[ZERO for _ in range(cols)] for _ in range(rows)]


def identity(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = ONE
    return out


def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    c = Qsqrt2.coerce(c)
    return [[c * value for value in row] for row in a]


def outer(x):
    return [[x[i] * x[j] for j in range(len(x))] for i in range(len(x))]


def inner(x, a, y):
    return sum(
        (
            x[i] * a[i][j] * y[j]
            for i in range(len(x))
            for j in range(len(y))
        ),
        ZERO,
    )


def multiply(a, b):
    out = zeros(len(a), len(b[0]))
    for i in range(len(a)):
        for k in range(len(b)):
            if a[i][k] == ZERO:
                continue
            for j in range(len(b[0])):
                out[i][j] = out[i][j] + a[i][k] * b[k][j]
    return out


def rank(a):
    work = [row[:] for row in a]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (i for i in range(pivot_row, rows) if work[i][col] != ZERO),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][col]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for i in range(rows):
            if i == pivot_row:
                continue
            value = work[i][col]
            if value != ZERO:
                work[i] = [
                    work[i][j] - value * work[pivot_row][j]
                    for j in range(cols)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def polynomial_in_matrix(matrix, coefficients):
    """Evaluate coefficients[0] I + coefficients[1] M + ... ."""
    n = len(matrix)
    out = zeros(n, n)
    power = identity(n)
    for coefficient in coefficients:
        out = add(out, scale(coefficient, power))
        power = multiply(power, matrix)
    return out


def idx(k, a, b):
    return 9 * k + 3 * a + b


def physical_trace_replace(r, site):
    reduced = zeros(6, 6)
    if site == 1:
        for k in range(2):
            for b in range(3):
                for ell in range(2):
                    for d in range(3):
                        reduced[3 * k + b][3 * ell + d] = sum(
                            (
                                r[idx(k, a, b)][idx(ell, a, d)]
                                for a in range(3)
                            ),
                            ZERO,
                        )
    else:
        for k in range(2):
            for a in range(3):
                for ell in range(2):
                    for c in range(3):
                        reduced[3 * k + a][3 * ell + c] = sum(
                            (
                                r[idx(k, a, b)][idx(ell, c, b)]
                                for b in range(3)
                            ),
                            ZERO,
                        )

    out = zeros(18, 18)
    for k in range(2):
        for a in range(3):
            for b in range(3):
                for ell in range(2):
                    for c in range(3):
                        for d in range(3):
                            if site == 1 and a == c:
                                out[idx(k, a, b)][idx(ell, c, d)] = (
                                    reduced[3 * k + b][3 * ell + d]
                                )
                            if site == 2 and b == d:
                                out[idx(k, a, b)][idx(ell, c, d)] = (
                                    reduced[3 * k + a][3 * ell + c]
                                )
    return out


def physical_marginal(r, site):
    out = zeros(3, 3)
    if site == 1:
        for a in range(3):
            for c in range(3):
                out[a][c] = sum(
                    (
                        r[idx(k, a, b)][idx(k, c, b)]
                        for k in range(2)
                        for b in range(3)
                    ),
                    ZERO,
                )
    else:
        for b in range(3):
            for d in range(3):
                out[b][d] = sum(
                    (
                        r[idx(k, a, b)][idx(k, a, d)]
                        for k in range(2)
                        for a in range(3)
                    ),
                    ZERO,
                )
    return out


def auxiliary_marginal(r):
    out = zeros(2, 2)
    for k in range(2):
        for ell in range(2):
            out[k][ell] = sum(
                (
                    r[idx(k, a, b)][idx(ell, a, b)]
                    for a in range(3)
                    for b in range(3)
                ),
                ZERO,
            )
    return out


def endpoint(r):
    e1 = physical_trace_replace(r, 1)
    e2 = physical_trace_replace(r, 2)
    rho_k = auxiliary_marginal(r)
    e12 = zeros(18, 18)
    for k in range(2):
        for a in range(3):
            for b in range(3):
                for ell in range(2):
                    for c in range(3):
                        for d in range(3):
                            if a == c and b == d:
                                e12[idx(k, a, b)][idx(ell, c, d)] = (
                                    rho_k[k][ell]
                                )
    return add(add(scale(4, e12), scale(-2, e1)), add(scale(-2, e2), r))


a_vector = [ZERO for _ in range(18)]
a_vector[idx(0, 0, 0)] = ONE
a_vector[idx(1, 1, 1)] = INV_SQRT2
a_vector[idx(1, 2, 2)] = INV_SQRT2

b_vector = [ZERO for _ in range(18)]
b_vector[idx(0, 0, 1)] = ONE
b_vector[idx(1, 0, 2)] = ONE

t = F(1, 100)
r = add(scale(1 - t / 2, outer(a_vector)), scale(t / 2, outer(b_vector)))

assert auxiliary_marginal(r) == identity(2)

rho1 = physical_marginal(r, 1)
rho2 = physical_marginal(r, 2)
expected_rho1 = [
    [Qsqrt2(F(1) + t / 2), ZERO, ZERO],
    [ZERO, Qsqrt2(F(1, 2) - t / 4), ZERO],
    [ZERO, ZERO, Qsqrt2(F(1, 2) - t / 4)],
]
expected_rho2 = [
    [Qsqrt2(F(1) - t / 2), ZERO, ZERO],
    [ZERO, Qsqrt2(F(1, 2) + t / 4), ZERO],
    [ZERO, ZERO, Qsqrt2(F(1, 2) + t / 4)],
]
assert rho1 == expected_rho1
assert rho2 == expected_rho2

d = (F(4) - t * t) ** 3 / F(1024)
m = endpoint(r)

x = [ZERO for _ in range(18)]
x[idx(0, 0, 0)] = Qsqrt2(F(-2))
x[idx(1, 1, 1)] = INV_SQRT2
x[idx(1, 2, 2)] = INV_SQRT2

two_i_minus_r = add(scale(2, identity(18)), scale(-1, r))
factor_residual = add(m, scale(-6 * d, two_i_minus_r))

assert inner(x, identity(18), x) == Qsqrt2(F(5))
assert inner(x, m, x) == Qsqrt2(F(3) + 4 * t)
assert inner(x, two_i_minus_r, x) == Qsqrt2((F(18) + t) / 2)

expected_negative = F(-34470066248354597, 102400000000000000)
value = inner(x, factor_residual, x)
assert value == Qsqrt2(expected_negative)
assert value.rational < 0 and value.radical == 0

# The same separating vector does not violate the live scalar floor.
g = t * (2 - t)
scalar_residual = add(m, scale(-3 * g * d, identity(18)))
scalar_value = inner(x, scalar_residual, x)
assert scalar_value.radical == 0 and scalar_value.rational > 0

# Two rank-one anchors with exactly the same physical marginals but
# different endpoint spectra.
c_vector = [ZERO for _ in range(18)]
c_vector[idx(0, 0, 0)] = INV_SQRT2
c_vector[idx(0, 1, 1)] = INV_SQRT2
c_vector[idx(1, 0, 2)] = INV_SQRT2
c_vector[idx(1, 2, 0)] = INV_SQRT2

r_a = outer(a_vector)
r_c = outer(c_vector)
assert auxiliary_marginal(r_a) == identity(2)
assert auxiliary_marginal(r_c) == identity(2)
expected_common_marginal = [
    [ONE, ZERO, ZERO],
    [ZERO, Qsqrt2(F(1, 2)), ZERO],
    [ZERO, ZERO, Qsqrt2(F(1, 2))],
]
for site in (1, 2):
    assert physical_marginal(r_a, site) == expected_common_marginal
    assert physical_marginal(r_c, site) == expected_common_marginal

m_a = endpoint(r_a)
m_c = endpoint(r_c)

# Exact eigenspace multiplicities.  The matrices are real symmetric, so
# these kernel dimensions and annihilating polynomials determine the
# displayed spectra.
for value, multiplicity in ((2, 7), (3, 4), (4, 5)):
    assert 18 - rank(add(m_a, scale(-value, identity(18)))) == multiplicity
assert 18 - rank(polynomial_in_matrix(m_a, (2, -4, 1))) == 2
annihilator_a = polynomial_in_matrix(
    m_a,
    # (x-2)(x-3)(x-4)(x^2-4x+2)
    (-48, 148, -146, 64, -13, 1),
)
assert annihilator_a == zeros(18, 18)

for value, multiplicity in ((1, 1), (2, 2), (3, 6), (4, 3)):
    assert 18 - rank(add(m_c, scale(-value, identity(18)))) == multiplicity
assert 18 - rank(polynomial_in_matrix(m_c, (5, -5, 1))) == 6
annihilator_c = polynomial_in_matrix(
    m_c,
    # (x-1)(x-2)(x-3)(x-4)(x^2-5x+5)
    (120, -370, 449, -275, 90, -15, 1),
)
assert annihilator_c == zeros(18, 18)

# Sharp diagonal-pencil audit at a = 9/25.  This is the rational
# Pythagorean specialization
# D=E_00, Z=(3/5)E_11+(4/5)E_22.
u_vector = [ZERO for _ in range(18)]
u_vector[idx(0, 0, 0)] = ONE
u_vector[idx(1, 1, 1)] = Qsqrt2(F(3, 5))
u_vector[idx(1, 2, 2)] = Qsqrt2(F(4, 5))
r_u = outer(u_vector)
assert auxiliary_marginal(r_u) == identity(2)
expected_u_marginal = [
    [ONE, ZERO, ZERO],
    [ZERO, Qsqrt2(F(9, 25)), ZERO],
    [ZERO, ZERO, Qsqrt2(F(16, 25))],
]
assert physical_marginal(r_u, 1) == expected_u_marginal
assert physical_marginal(r_u, 2) == expected_u_marginal

m_u = endpoint(r_u)
support = (idx(0, 0, 0), idx(1, 1, 1), idx(1, 2, 2))
h_u = [[m_u[i][j] for j in support] for i in support]
assert h_u == [
    [ONE, Qsqrt2(F(3, 5)), Qsqrt2(F(4, 5))],
    [Qsqrt2(F(3, 5)), Qsqrt2(F(73, 25)), Qsqrt2(F(12, 25))],
    [Qsqrt2(F(4, 5)), Qsqrt2(F(12, 25)), Qsqrt2(F(52, 25))],
]

x_parameter = F(144, 625)
assert polynomial_in_matrix(
    h_u,
    (
        -16 * x_parameter,
        8 + 8 * x_parameter,
        -6,
        1,
    ),
) == zeros(3, 3)

delta = 2 * x_parameter
h_shift = add(h_u, scale(-delta, identity(3)))
leading_one = h_shift[0][0]
leading_two = (
    h_shift[0][0] * h_shift[1][1]
    - h_shift[0][1] * h_shift[1][0]
)
leading_three = (
    h_shift[0][0]
    * (h_shift[1][1] * h_shift[2][2] - h_shift[1][2] * h_shift[2][1])
    - h_shift[0][1]
    * (h_shift[1][0] * h_shift[2][2] - h_shift[1][2] * h_shift[2][0])
    + h_shift[0][2]
    * (h_shift[1][0] * h_shift[2][1] - h_shift[1][1] * h_shift[2][0])
)
for principal_minor in (leading_one, leading_two, leading_three):
    assert (
        principal_minor.radical == 0
        and principal_minor.rational > 0
    )

# Outside the displayed support block the endpoint is diagonal and its
# entries are at least two, hence strictly exceed delta.
complement = tuple(i for i in range(18) if i not in support)
for i in complement:
    for j in range(18):
        if j != i:
            assert m_u[i][j] == ZERO
    assert m_u[i][i].radical == 0
    assert m_u[i][i].rational >= 2 > delta

print("exact cofactor factor-floor obstruction passed")
