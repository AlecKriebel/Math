#!/usr/bin/env python3
"""Dependency-free exact check of the recoupled -1/9 product witness."""

from fractions import Fraction as Q
from itertools import product


COEFFICIENT = (Q(2), Q(-1), Q(2, 3), Q(-1, 3))


def swap(word, first, second):
    out = list(word)
    out[first], out[second] = out[second], out[first]
    return tuple(out)


def move(word, first_vertical, second_vertical, crossed):
    # The rightmost operator acts first.
    if crossed:
        word = swap(word, 2, 3)
    if second_vertical:
        word = swap(word, 1, 3)
    if first_vertical:
        word = swap(word, 0, 2)
    if crossed:
        word = swap(word, 0, 1)
    return word


LEFT = (
    {(0, 1): 1},
    {(0, 0): 1},
    {(j, j): 1 for j in range(3)},
)
RIGHT = (
    {(0, 1): 1},
    {(1, 1): 1},
    {(j, j): 1 for j in range(3)},
)


def local_table(left, right, crossed):
    state = {
        (a, b, c, d): x * y
        for (a, b), x in left.items()
        for (c, d), y in right.items()
    }
    norm_squared = sum(value * value for value in state.values())
    return {
        (first, second): Q(
            sum(
                value
                * state.get(
                    move(word, first, second, crossed),
                    0,
                )
                for word, value in state.items()
            ),
            norm_squared,
        )
        for first, second in product((0, 1), repeat=2)
    }


def contraction(tables):
    value = Q(0)
    for first_mask in range(8):
        for second_mask in range(8):
            term = (
                COEFFICIENT[first_mask.bit_count()]
                * COEFFICIENT[second_mask.bit_count()]
            )
            for site in range(3):
                term *= tables[site][
                    ((first_mask >> site) & 1,
                     (second_mask >> site) & 1)
                ]
            value += term
    return value


def rational_rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    work[row][j] - scale * work[pivot_row][j]
                    for j in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def main():
    direct = [
        local_table(left, right, False)
        for left, right in zip(LEFT, RIGHT)
    ]
    crossed = [
        local_table(left, right, True)
        for left, right in zip(LEFT, RIGHT)
    ]

    order = ((0, 0), (0, 1), (1, 0), (1, 1))
    assert tuple(direct[0][key] for key in order) == (1, 1, 1, 1)
    assert tuple(crossed[0][key] for key in order) == (0, 0, 0, 1)
    assert tuple(direct[1][key] for key in order) == (1, 0, 0, 0)
    assert tuple(crossed[1][key] for key in order) == (1, 0, 0, 0)
    bell_table = (Q(1), Q(1, 3), Q(1, 3), Q(1))
    assert tuple(direct[2][key] for key in order) == bell_table
    assert tuple(crossed[2][key] for key in order) == bell_table

    direct_value = contraction(direct)
    crossed_value = contraction(crossed)
    assert direct_value == Q(8, 9)
    assert crossed_value == Q(1)
    assert direct_value - crossed_value == Q(-1, 9)

    zero = Q(0)
    identity = [[Q(i == j) for j in range(3)] for i in range(3)]
    e01 = [[zero for _ in range(3)] for _ in range(3)]
    e00 = [[zero for _ in range(3)] for _ in range(3)]
    e11 = [[zero for _ in range(3)] for _ in range(3)]
    e01[0][1] = Q(1)
    e00[0][0] = Q(1)
    e11[1][1] = Q(1)
    assert tuple(map(rational_rank, (e01, e00, identity))) == (1, 1, 3)
    assert tuple(map(rational_rank, (e01, e11, identity))) == (1, 1, 3)

    print(
        "verified: direct=8/9, crossed=1, "
        "recoupled product expectation=-1/9"
    )


if __name__ == "__main__":
    main()
