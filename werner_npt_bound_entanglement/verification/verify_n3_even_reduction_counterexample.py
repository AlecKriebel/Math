#!/usr/bin/env python3
"""Exact integer verification of the n=3 even-reduction counterexample."""

from __future__ import annotations


D = 3
N = D**3


def digits(index: int) -> tuple[int, int, int]:
    return index // 9, (index // 3) % 3, index % 3


WORDS = [digits(index) for index in range(N)]


def partial_trace(
    matrix: list[list[int]], traced: tuple[int, ...]
) -> list[list[int]]:
    keep = tuple(site for site in range(3) if site not in traced)
    size = D ** len(keep)
    out = [[0 for _ in range(size)] for _ in range(size)]

    def retained_index(word: tuple[int, int, int]) -> int:
        value = 0
        for site in keep:
            value = D * value + word[site]
        return value

    for row, left in enumerate(WORDS):
        for column, right in enumerate(WORDS):
            if any(left[site] != right[site] for site in traced):
                continue
            out[retained_index(left)][retained_index(right)] += (
                matrix[row][column]
            )
    return out


def hs_norm_squared(matrix: list[list[int]]) -> int:
    return sum(entry * entry for row in matrix for entry in row)


def pair_value(
    matrix: list[list[int]], left: int, right: int
) -> int:
    return (
        hs_norm_squared(partial_trace(matrix, (left, right)))
        - hs_norm_squared(partial_trace(matrix, (left,)))
        - hs_norm_squared(partial_trace(matrix, (right,)))
        + hs_norm_squared(matrix)
    )


def main() -> None:
    matrix = [[0 for _ in range(N)] for _ in range(N)]
    matrix[0][12] = 1   # |000><110|
    matrix[1][13] = 1   # |001><111|

    nonzero_rows = {
        row for row in range(N) if any(matrix[row][column] for column in range(N))
    }
    nonzero_columns = {
        column
        for column in range(N)
        if any(matrix[row][column] for row in range(N))
    }
    assert nonzero_rows == {0, 1}
    assert nonzero_columns == {12, 13}
    assert hs_norm_squared(matrix) == 2
    assert sum(matrix[index][index] for index in range(N)) == 0

    values = [
        pair_value(matrix, 0, 1),
        pair_value(matrix, 0, 2),
        pair_value(matrix, 1, 2),
    ]
    assert values == [2, -2, -2]
    assert sum(values) == -2

    # The two nonzero rows and columns are orthogonal unit coordinate
    # vectors, so the two nonzero singular values are exactly 1.
    s1 = s2 = 1
    trace = 0
    corrected = sum(values) + (
        (s1 + s2) ** 2 - trace**2
    ) // 2
    assert corrected == 0

    # 8 Q_3 = 2 ||C||_2^2 - |Tr C|^2 + 2 E.
    eight_q3 = (
        2 * hs_norm_squared(matrix)
        - trace**2
        + 2 * sum(values)
    )
    assert eight_q3 == 0
    print("verified: rank=2, pair terms=(2,-2,-2), E=-2, Q3=0")


if __name__ == "__main__":
    main()
