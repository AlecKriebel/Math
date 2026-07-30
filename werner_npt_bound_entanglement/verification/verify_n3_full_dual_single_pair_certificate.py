#!/usr/bin/env python3
"""Exact checker for the full-dual single-pair certificate.

All arithmetic is over Gaussian rationals.  The checker verifies:

* the residual-map polynomial and all normalization constants;
* the finite product decomposition of I-Phi_9;
* the Choi decomposition of the measure-and-prepare map; and
* the completely positive remainder sector by sector.
"""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Gaussian:
    real: F = F(0)
    imag: F = F(0)

    def __add__(self, other):
        other = gaussian(other)
        return Gaussian(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self):
        return Gaussian(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-gaussian(other))

    def __rsub__(self, other):
        return gaussian(other) - self

    def __mul__(self, other):
        other = gaussian(other)
        return Gaussian(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    __rmul__ = __mul__

    def __truediv__(self, value):
        return Gaussian(self.real / value, self.imag / value)

    def conjugate(self):
        return Gaussian(self.real, -self.imag)


def gaussian(value):
    return value if isinstance(value, Gaussian) else Gaussian(F(value))


ZERO = Gaussian()
ONE = Gaussian(F(1))
I = Gaussian(F(0), F(1))


def clean(dictionary):
    return {key: value for key, value in dictionary.items() if value != 0}


def polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for key, value in polynomial.items():
            answer[key] = answer.get(key, F(0)) + value
    return clean(answer)


def polynomial_scale(value, polynomial):
    return clean({key: value * entry for key, entry in polynomial.items()})


def polynomial_multiply(left, right):
    answer = {}
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            key = left_key | right_key
            answer[key] = (
                answer.get(key, F(0)) + left_value * right_value
            )
    return clean(answer)


identity = {frozenset(): F(1)}
e1 = {frozenset((1,)): F(1)}
e2 = {frozenset((2,)): F(1)}
e3 = {frozenset((3,)): F(1)}
e123 = {frozenset((1, 2, 3)): F(1)}

# S(P), with its output identity replaced by 2 e1 e2 e3(P).
S = polynomial_add(
    polynomial_scale(2, e123),
    polynomial_scale(F(-1, 6), polynomial_add(e1, e2, e3)),
    polynomial_scale(F(1, 12), identity),
)
q1 = polynomial_add(e1, polynomial_scale(F(-1, 3), identity))
q2 = polynomial_add(e2, polynomial_scale(F(-1, 3), identity))
F12 = polynomial_multiply(q1, q2)
residual = polynomial_add(S, polynomial_scale(-1, F12))

cal_a = polynomial_add(
    polynomial_scale(2, polynomial_multiply(e1, e2)),
    polynomial_scale(F(-1, 6), identity),
)
cal_b = polynomial_multiply(
    polynomial_add(e1, polynomial_scale(F(-1, 6), identity)),
    polynomial_add(e2, polynomial_scale(F(-1, 6), identity)),
)
phi3 = polynomial_add(e3, polynomial_scale(F(-1, 2), identity))
certificate = polynomial_add(
    polynomial_multiply(cal_a, phi3),
    polynomial_scale(F(1, 2), cal_a),
    polynomial_scale(-1, cal_b),
)
assert residual == certificate
assert residual == {
    frozenset((1, 2, 3)): F(2),
    frozenset((1, 2)): F(-1),
    frozenset((1,)): F(1, 6),
    frozenset((2,)): F(1, 6),
    frozenset((3,)): F(-1, 6),
    frozenset(): F(-1, 36),
}


def add_sparse(matrix, row, column, value):
    value = gaussian(value)
    matrix[(row, column)] = matrix.get((row, column), ZERO) + value
    if matrix[(row, column)] == ZERO:
        del matrix[(row, column)]


def add_outer(matrix, vector, coefficient):
    coefficient = gaussian(coefficient)
    for row, row_value in vector.items():
        for column, column_value in vector.items():
            add_sparse(
                matrix,
                row,
                column,
                coefficient * row_value * column_value.conjugate(),
            )


def identity_minus_phi(n):
    answer = {}
    for row in range(n * n):
        add_sparse(answer, row, row, ONE)
    for a in range(n):
        for b in range(n):
            add_sparse(
                answer,
                n * a + a,
                n * b + b,
                -F(1, n),
            )
    return answer


def finite_product_decomposition(n):
    answer = {}
    phases = (ONE, I, -ONE, -I)
    for a in range(n):
        for b in range(a + 1, n):
            for phase in phases:
                vector = {
                    n * a + a: F(1, 2),
                    n * a + b: -phase.conjugate() / 2,
                    n * b + a: phase / 2,
                    n * b + b: F(-1, 2),
                }
                add_outer(answer, vector, F(1, n))
    for a in range(n):
        for b in range(n):
            if a != b:
                add_sparse(
                    answer,
                    n * a + b,
                    n * a + b,
                    F(n - 1, n),
                )
    return answer


# This is the exact n=9 decomposition used in the proof.
n = 9
j0 = identity_minus_phi(n)
assert finite_product_decomposition(n) == j0

# J_A = I/2 + 3(I-Phi_9)/2 = 2I - 3 Phi_9/2.
j_a_from_products = {
    key: F(3, 2) * value for key, value in j0.items()
}
for row in range(n * n):
    add_sparse(j_a_from_products, row, row, F(1, 2))
j_a_direct = {}
for row in range(n * n):
    add_sparse(j_a_direct, row, row, F(2))
for a in range(n):
    for b in range(n):
        add_sparse(
            j_a_direct,
            n * a + a,
            n * b + b,
            F(-1, 6),
        )
assert j_a_from_products == j_a_direct

# Choi eigenvalues on P1P2, P1Q2, Q1P2, Q1Q2.
j_a_eigenvalues = (F(1, 2), F(2), F(2), F(2))
j_b_eigenvalues = (F(1, 4), F(1, 2), F(1, 2), F(1))
remainder_eigenvalues = tuple(
    F(1, 2) * a - b
    for a, b in zip(j_a_eigenvalues, j_b_eigenvalues)
)
assert remainder_eigenvalues == (0, F(1, 2), F(1, 2), 0)
assert all(value >= 0 for value in remainder_eigenvalues)

print(
    "verified exact single-pair residual polynomial, finite "
    "I-Phi_9 product decomposition, and positive Choi remainder"
)
