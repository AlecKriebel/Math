#!/usr/bin/env python3
"""Exact verifier for the orthogonal-triple 3/4 equality construction.

The arithmetic field is Q(sqrt(2), sqrt(3), i), implemented directly
over fractions.  No floating-point arithmetic or external package is
used.
"""

from fractions import Fraction as F
from itertools import combinations, product


class K:
    """Element of Q(sqrt(2), sqrt(3), i) in its standard 8-term basis."""

    __slots__ = ("c",)

    def __init__(self, value=0):
        if isinstance(value, K):
            self.c = value.c
        elif isinstance(value, tuple):
            self.c = value
        else:
            self.c = (F(value),) + (F(0),) * 7

    @staticmethod
    def basis(index):
        coefficients = [F(0)] * 8
        coefficients[index] = F(1)
        return K(tuple(coefficients))

    def __add__(self, other):
        other = K(other)
        return K(tuple(x + y for x, y in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-K(other))

    def __rsub__(self, other):
        return K(other) - self

    def __mul__(self, other):
        other = K(other)
        out = [F(0)] * 8
        for left, x in enumerate(self.c):
            if not x:
                continue
            a, b, q = left & 1, (left >> 1) & 1, (left >> 2) & 1
            for right, y in enumerate(other.c):
                if not y:
                    continue
                aa = a + (right & 1)
                bb = b + ((right >> 1) & 1)
                qq = q + ((right >> 2) & 1)
                coefficient = x * y
                if aa == 2:
                    coefficient *= 2
                    aa = 0
                if bb == 2:
                    coefficient *= 3
                    bb = 0
                if qq == 2:
                    coefficient *= -1
                    qq = 0
                out[aa + 2 * bb + 4 * qq] += coefficient
        return K(tuple(out))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, F)):
            return K(tuple(x / other for x in self.c))
        raise TypeError("only rational division is needed")

    def conjugate(self):
        return K(tuple(x if index < 4 else -x for index, x in enumerate(self.c)))

    def __eq__(self, other):
        return self.c == K(other).c

    def __repr__(self):
        return f"K{self.c}"


SQRT2 = K.basis(1)
SQRT3 = K.basis(2)
IMAG = K.basis(4)
ZERO = K(0)
ONE = K(1)


def zeros(rows, cols):
    return [[ZERO for _ in range(cols)] for _ in range(rows)]


def matrix_add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def matrix_scale(c, a):
    return [[c * value for value in row] for row in a]


def vectorize(a):
    return [a[i][j] for i in range(len(a)) for j in range(len(a[0]))]


def inner(x, y):
    return sum(a.conjugate() * b for a, b in zip(x, y))


def outer(x, y):
    return [[a * b.conjugate() for b in y] for a in x]


def tensor_vectors(x, y):
    return [a * b for a in x for b in y]


def partial_trace(a, n, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(n) if i not in traced)
    rem_words = list(product(range(2), repeat=len(remaining)))
    tr_words = list(product(range(2), repeat=len(traced)))
    out = zeros(2 ** len(remaining), 2 ** len(remaining))

    def index(word):
        value = 0
        for digit in word:
            value = 2 * value + digit
        return value

    for row_index, row_remaining in enumerate(rem_words):
        for col_index, col_remaining in enumerate(rem_words):
            value = ZERO
            for trace_word in tr_words:
                row = [0] * n
                col = [0] * n
                for position, site in enumerate(remaining):
                    row[site] = row_remaining[position]
                    col[site] = col_remaining[position]
                for position, site in enumerate(traced):
                    row[site] = trace_word[position]
                    col[site] = trace_word[position]
                value += a[index(row)][index(col)]
            out[row_index][col_index] = value
    return out


def hs_inner(a, b):
    return sum(
        a[i][j].conjugate() * b[i][j]
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def endpoint_form(a, b, n):
    value = ZERO
    sites = tuple(range(n))
    for size in range(n + 1):
        coefficient = K(F(-1, 2) ** size)
        for traced in combinations(sites, size):
            value += coefficient * hs_inner(
                partial_trace(a, n, traced),
                partial_trace(b, n, traced),
            )
    return value


def main():
    identity = [[ONE, ZERO], [ZERO, ONE]]
    x_pauli = [[ZERO, ONE], [ONE, ZERO]]
    y_pauli = [[ZERO, -IMAG], [IMAG, ZERO]]
    inverse_sqrt_two = SQRT2 / 2
    coefficient = (SQRT2 * SQRT3) / 4  # sqrt(3/8)

    u_matrix = matrix_scale(inverse_sqrt_two, identity)
    v_matrix = matrix_scale(inverse_sqrt_two, x_pauli)
    w_matrix = matrix_scale(
        inverse_sqrt_two,
        matrix_add(
            matrix_add(
                matrix_scale(coefficient, identity),
                matrix_scale(IMAG * coefficient, x_pauli),
            ),
            matrix_scale(K(F(1, 2)), y_pauli),
        ),
    )

    u = vectorize(u_matrix)
    v = vectorize(v_matrix)
    w = vectorize(w_matrix)
    assert inner(u, u) == ONE
    assert inner(v, v) == ONE
    assert inner(w, w) == ONE
    assert inner(u, v) == ZERO

    a2 = outer(w, w)
    b2 = outer(u, v)
    assert endpoint_form(a2, a2, 2) == K(F(3, 8))
    assert endpoint_form(b2, b2, 2) == K(F(1, 2))
    assert endpoint_form(a2, b2, 2) == IMAG * K(F(3, 8))

    zero_flag = [ONE, ZERO]
    one_flag = [ZERO, ONE]
    w3 = tensor_vectors(zero_flag, w)
    u3 = tensor_vectors(one_flag, u)
    v3 = tensor_vectors(one_flag, v)
    assert inner(w3, w3) == ONE
    assert inner(u3, u3) == ONE
    assert inner(v3, v3) == ONE
    assert inner(w3, u3) == ZERO
    assert inner(w3, v3) == ZERO
    assert inner(u3, v3) == ZERO

    a3 = outer(w3, w3)
    b3 = outer(u3, v3)
    qa = endpoint_form(a3, a3, 3)
    qb = endpoint_form(b3, b3, 3)
    crossed = endpoint_form(a3, b3, 3)
    assert qa == K(F(3, 16))
    assert qb == K(F(1, 4))
    assert crossed == -IMAG * K(F(3, 16))
    assert crossed.conjugate() * crossed == K(F(3, 4)) * qa * qb

    # Exact scalar audit of the proof's final inequality.
    t = F(3, 8)
    determinant_modulus = F(1, 2)
    assert F(3, 8) * (F(1, 4) + F(1, 2) * determinant_modulus**2) - t**2 == 0
    assert (8 * t - 3) ** 2 == 0

    print(
        "verified: exact orthonormal three-qubit triple saturates "
        "|B_3|^2 = (3/4) Q_3(P_w) Q_3(|u><v|)"
    )


if __name__ == "__main__":
    main()
