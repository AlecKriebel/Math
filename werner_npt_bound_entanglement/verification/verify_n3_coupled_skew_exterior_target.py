#!/usr/bin/env python3
"""Exact checks for the coupled two-/three-skew exterior reduction.

Only Python's standard library and rational arithmetic are used.
"""

from fractions import Fraction as F
from itertools import combinations


ORDER = ((0, 0), (0, 1), (1, 0), (1, 1))


def basis(word):
    return {word: F(1)}


def tensor_two(left, right):
    return {
        (a, b): x * y
        for a, x in left.items()
        for b, y in right.items()
    }


def swap_sites(key, sites):
    left, right = list(key[0]), list(key[1])
    for site in sites:
        left[site], right[site] = right[site], left[site]
    return tuple(left), tuple(right)


def inner(left, right):
    return sum(left.get(key, F(0)) * value for key, value in right.items())


def product_i_minus_f_entry(left, right, sites):
    sites = tuple(sites)
    value = F(0)
    for size in range(len(sites) + 1):
        for subset in combinations(sites, size):
            moved = {
                swap_sites(key, subset): coefficient
                for key, coefficient in right.items()
            }
            value += (-1) ** size * inner(left, moved)
    return value


def feature_groups(left, right):
    columns = {
        (a, b): tensor_two(left[a], right[b])
        for a, b in ORDER
    }
    q2 = [[F(0) for _ in range(4)] for _ in range(4)]
    q3 = [[F(0) for _ in range(4)] for _ in range(4)]
    for row, ab in enumerate(ORDER):
        for column, cd in enumerate(ORDER):
            q2[row][column] = F(1, 9) * sum(
                (
                    product_i_minus_f_entry(
                        columns[ab], columns[cd], pair
                    )
                    for pair in combinations(range(3), 2)
                ),
                F(0),
            )
            q3[row][column] = F(1, 9) * product_i_minus_f_entry(
                columns[ab], columns[cd], range(3)
            )
    return q2, q3


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def main():
    # The sector collapse is an exact coefficient identity.
    n, s, p, t = F(7), F(11), F(13), F(17)
    j2 = F(3, 4) * n - F(1, 2) * s + F(1, 4) * p
    j3 = F(1, 8) * (n - s + p - t)
    w2 = F(1, 3) * s - F(2, 9) * p + F(1, 9) * t
    assert j2 + 2 * j3 == n - F(9, 4) * w2

    # Inserting the shifted determinant leaves precisely one square.
    mu = F(4, 9)
    singular_1, singular_2 = F(7), F(5)
    root_p, root_q = F(3), F(2)
    g11 = mu - root_p**2
    g22 = mu - root_q**2
    cross = F(2, 9) + root_p * root_q
    pair_mass = (
        singular_1**2 * g11
        + singular_2**2 * g22
        + 2 * singular_1 * singular_2 * cross
    )
    target = mu * (
        singular_1**2
        + singular_2**2
        + singular_1 * singular_2
    )
    assert target - pair_mass == (
        singular_1 * root_p - singular_2 * root_q
    ) ** 2

    # Canonical common-plane equality and the matched-slack obstruction.
    left = [basis((0, 0, 0)), basis((0, 0, 1))]
    right = [basis((1, 1, 0)), basis((1, 1, 1))]
    q2, q3 = feature_groups(left, right)
    q = add(q2, q3)
    expected_q = [
        [F(1, 9), 0, 0, 0],
        [0, F(4, 9), F(-1, 3), 0],
        [0, F(-1, 3), F(4, 9), 0],
        [0, 0, 0, F(1, 9)],
    ]
    assert q == expected_q

    # Partial-transpose crossing: p=q=1/9, G12=1/3.
    slack_p = q[0][0]
    slack_q = q[3][3]
    matched = q[0][3]
    crossed = q[1][2]
    assert slack_p == slack_q == F(1, 9)
    assert abs(crossed) == F(1, 3)
    assert abs(crossed) == F(2, 9) + F(1, 9)
    assert matched == 0
    assert abs(crossed - matched) > F(2, 9)

    print(
        "verified exact sector collapse, shifted square, canonical "
        "equality, and matched-slack obstruction"
    )


if __name__ == "__main__":
    main()
