#!/usr/bin/env python3
"""Exact audit of the unequal-singular balanced physical example."""

from __future__ import annotations

from fractions import Fraction as F

# Elements of Q(sqrt(2)) are represented by a + b sqrt(2).
Q2 = tuple[F, F]


def q2(a: int | F = 0, b: int | F = 0) -> Q2:
    return (F(a), F(b))


def add(x: Q2, y: Q2) -> Q2:
    return (x[0] + y[0], x[1] + y[1])


def mul(x: Q2, y: Q2) -> Q2:
    return (
        x[0] * y[0] + 2 * x[1] * y[1],
        x[0] * y[1] + x[1] * y[0],
    )


def basis_entry(
    u_left: tuple[int, ...],
    v_left: tuple[int, ...],
    u_right: tuple[int, ...],
    v_right: tuple[int, ...],
) -> F:
    value = F(1)
    for ul, vl, ur, vr in zip(u_left, v_left, u_right, v_right):
        direct = int(ul == ur and vl == vr)
        swapped = int(ul == vr and vl == ur)
        value *= direct - F(1, 2) * swapped
    return value


u = [(0, 0, 0), (1, 1, 1)]
v = [(0, 0, 2), (1, 1, 0)]
k = [
    [
        basis_entry(u[a], v[b], u[c], v[d])
        for c in range(2)
        for d in range(2)
    ]
    for a in range(2)
    for b in range(2)
]
assert k == [
    [F(1, 4), 0, 0, 0],
    [0, F(1, 2), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, F(1, 4)],
]

# Squared filter entries.  Only their products enter the filtered K.
# R^2 = diag(2^(1/4),2^(-1/4)),
# S^2 = diag(2^(-1/4),2^(1/4)).
# Products on (00,01,10,11) are (1,sqrt(2),1/sqrt(2),1).
filter_products = [q2(1), q2(0, 1), q2(0, F(1, 2)), q2(1)]
filtered_diagonal = [
    mul(filter_products[index], q2(k[index][index]))
    for index in range(4)
]
assert filtered_diagonal == [
    q2(F(1, 4)),
    q2(0, F(1, 2)),
    q2(0, F(1, 2)),
    q2(F(1, 4)),
]

first_marginal = [
    add(filtered_diagonal[0], filtered_diagonal[1]),
    add(filtered_diagonal[2], filtered_diagonal[3]),
]
second_marginal = [
    add(filtered_diagonal[0], filtered_diagonal[2]),
    add(filtered_diagonal[1], filtered_diagonal[3]),
]
assert first_marginal[0] == first_marginal[1]
assert second_marginal[0] == second_marginal[1]

# Squared singular values of the physical singlet coefficient are
# sqrt(2) and 1/sqrt(2), hence their ratio squared is 2.
singular_square_large = q2(0, 1)
singular_square_small = q2(0, F(1, 2))
assert singular_square_large == mul(q2(2), singular_square_small)
assert mul(singular_square_large, singular_square_small) == q2(1)

# Only the first dyad survives a one-site trace (at the third site).
# Therefore Q_3 = (a^2+b^2) - a^2/2 = sqrt(2).
q_value = add(
    mul(q2(F(1, 2)), singular_square_large), singular_square_small
)
assert q_value == q2(0, 1)

print(
    "verified exact physical compression, determinant-one balancing, "
    "unequal singular values, and Q3 = sqrt(2)"
)
