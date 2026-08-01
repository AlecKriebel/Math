#!/usr/bin/env python3
"""Dependency-free exact audit of the three-slice DTH Fierz identity."""

from fractions import Fraction as F


def epsilon(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def words_except(site):
    for first in range(3):
        for second in range(3):
            out = [None] * 3
            positions = [position for position in range(3) if position != site]
            out[positions[0]], out[positions[1]] = first, second
            yield out


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def norm_squared(vector):
    return dot(vector, vector)


def hodge_integer_action(x, y):
    """Return Dhat_x y=(2 sqrt(2))D_x y exactly."""
    out = [F(0)] * 27
    for p in range(3):
        for q in range(3):
            for r in range(3):
                coefficient = x[index((p, q, r))]
                if not coefficient:
                    continue
                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            value = y[index((i, j, k))]
                            if not value:
                                continue
                            for a in range(3):
                                ep = epsilon(p, a, i)
                                if not ep:
                                    continue
                                for b in range(3):
                                    eq = epsilon(q, b, j)
                                    if not eq:
                                        continue
                                    for c in range(3):
                                        er = epsilon(r, c, k)
                                        if er:
                                            out[index((a, b, c))] += (
                                                coefficient * value * ep * eq * er
                                            )
    return out


def reduction(x, site):
    out = [[F(0) for _ in range(3)] for _ in range(3)]
    for partial in words_except(site):
        for a in range(3):
            for b in range(3):
                left, right = partial[:], partial[:]
                left[site], right[site] = a, b
                out[a][b] += x[index(left)] * x[index(right)]
    return out


def transition(x, y, site):
    out = [[F(0) for _ in range(3)] for _ in range(3)]
    for partial in words_except(site):
        for a in range(3):
            for b in range(3):
                left, right = partial[:], partial[:]
                left[site], right[site] = a, b
                out[a][b] += x[index(left)] * y[index(right)]
    return out


def matrix_inner(left, right):
    return sum(x * y for a, b in zip(left, right) for x, y in zip(a, b))


def matrix_norm_squared(matrix):
    return matrix_inner(matrix, matrix)


def invariant_fierz(x, y):
    value = norm_squared(x) * norm_squared(y) - dot(x, y) ** 2
    for site in range(3):
        value -= matrix_inner(reduction(x, site), reduction(y, site))
        value += matrix_norm_squared(transition(x, y, site))
    return value


def flatten(tensor, site):
    out = [[F(0) for _ in range(9)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                word = (a, b, c)
                row = word[site]
                rest = tuple(word[position] for position in range(3)
                             if position != site)
                column = 3 * rest[0] + rest[1]
                out[row][column] = tensor[index(word)]
    return out


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [[dot(row, column) for column in right_t] for row in left]


def exterior_deficits(x, y, site):
    X, Y = flatten(x, site), flatten(y, site)
    product = norm_squared(x) * norm_squared(y)
    column = product - matrix_norm_squared(matmul(transpose(X), Y))
    row = product - matrix_norm_squared(matmul(X, transpose(Y)))
    return column, row


def basis(position):
    out = [F(0)] * 27
    out[position] = F(1)
    return out


def main():
    # A deliberately nonsymmetric, full-local-support exact tensor pair.
    x = [F(0)] * 27
    y = [F(0)] * 27
    for word, value in {
        (0, 0, 0): 2,
        (0, 1, 2): -1,
        (1, 2, 0): 3,
        (2, 0, 1): 2,
        (2, 2, 2): -2,
    }.items():
        x[index(word)] = F(value)
    for word, value in {
        (0, 2, 1): 1,
        (1, 0, 2): 2,
        (1, 1, 1): -3,
        (2, 1, 0): 1,
        (2, 2, 2): 2,
    }.items():
        y[index(word)] = F(value)

    # Since D_x=Dhat_x/(2sqrt(2)), 8||D_xy||^2=||Dhat_xy||^2.
    direct = norm_squared(hodge_integer_action(x, y))
    invariant = invariant_fierz(x, y)
    assert direct == invariant

    for site in range(3):
        column, row = exterior_deficits(x, y, site)
        marginal_minus_transition = (
            matrix_inner(reduction(x, site), reduction(y, site))
            - matrix_norm_squared(transition(x, y, site))
        )
        assert marginal_minus_transition == row - column
        assert column >= 0 and row >= 0

    # Exact rank-four coordinate projection and its aggregated identity.
    frame = [basis(position) for position in (0, 5, 11, 21)]
    assert all(dot(left, right) == F(i == j)
               for i, left in enumerate(frame)
               for j, right in enumerate(frame))
    direct_sum = sum(
        norm_squared(hodge_integer_action(x, vector)) for vector in frame
    )
    overlap = sum(dot(x, vector) ** 2 for vector in frame)
    marginal_sum = sum(
        matrix_inner(reduction(x, site), reduction(vector, site))
        for site in range(3) for vector in frame
    )
    transition_sum = sum(
        matrix_norm_squared(transition(x, vector, site))
        for site in range(3) for vector in frame
    )
    aggregate = 4 * norm_squared(x) - overlap - marginal_sum + transition_sum
    assert direct_sum == aggregate

    exterior_signed = sum(
        exterior_deficits(x, vector, site)[0]
        - exterior_deficits(x, vector, site)[1]
        for site in range(3) for vector in frame
    )
    assert exterior_signed == transition_sum - marginal_sum

    print("exact three-slice DTH Fierz certificate passed")
    print("one-column matrix/invariant identity passed")
    print("rank-four aggregated projector identity passed")
    print("exterior-square signed remainder identity passed")


if __name__ == "__main__":
    main()
