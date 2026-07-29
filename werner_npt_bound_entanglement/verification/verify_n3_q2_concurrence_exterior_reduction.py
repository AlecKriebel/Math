#!/usr/bin/env python3
"""Dependency-free exact checks for the coherent-Q2 exterior reduction."""

from fractions import Fraction as F


def norm2(a):
    return sum((x * x for row in a for x in row), F(0))


def partial_trace(c, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(3) if i not in traced)
    size = 3 ** len(remaining)
    out = [[F(0) for _ in range(size)] for _ in range(size)]

    def digits(index, length):
        answer = [0] * length
        for i in range(length - 1, -1, -1):
            answer[i] = index % 3
            index //= 3
        return answer

    def index(word):
        answer = 0
        for x in word:
            answer = 3 * answer + x
        return answer

    for row_out in range(size):
        rr = digits(row_out, len(remaining))
        for col_out in range(size):
            cc = digits(col_out, len(remaining))
            for trace_word_index in range(3 ** len(traced)):
                tt = digits(trace_word_index, len(traced))
                row = [0, 0, 0]
                col = [0, 0, 0]
                for position, site in enumerate(remaining):
                    row[site] = rr[position]
                    col[site] = cc[position]
                for position, site in enumerate(traced):
                    row[site] = col[site] = tt[position]
                out[row_out][col_out] += c[index(row)][index(col)]
    return out


def j_form(c):
    singles = sum((norm2(partial_trace(c, (i,))) for i in range(3)), F(0))
    pairs = sum(
        (norm2(partial_trace(c, pair)) for pair in ((0, 1), (0, 2), (1, 2))),
        F(0),
    )
    return F(3, 4) * norm2(c) - F(1, 2) * singles + F(1, 4) * pairs


# Canonical companion C=|000><110|+|001><111|.
C = [[F(0) for _ in range(27)] for _ in range(27)]
C[0][12] = F(1)
C[1][13] = F(1)
assert norm2(C) == 2
assert j_form(C) == F(-1, 2)

# Its two singular values are both one, so J+s1*s2/2 is exactly zero.
assert j_form(C) + F(1, 2) == 0

# Exact unscaled logical compression from the note.
R = [
    [F(1, 4), 0, 0, 0],
    [0, F(3, 4), F(-1, 2), 0],
    [0, F(-1, 2), F(3, 4), 0],
    [0, 0, 0, F(1, 4)],
]
singlet = [0, 1, -1, 0]
triplet = [0, 1, 1, 0]


def quadratic(matrix, vector):
    return sum(
        (
            vector[i] * matrix[i][j] * vector[j]
            for i in range(len(vector))
            for j in range(len(vector))
        ),
        F(0),
    ) / sum((x * x for x in vector), F(0))


assert quadratic(R, singlet) == F(5, 4)
assert quadratic(R, triplet) == F(1, 4)
assert [R[i][i] for i in (0, 3)] == [F(1, 4), F(1, 4)]
assert F(5, 4) - 3 * F(1, 4) == F(1, 2)
assert F(4, 9) * F(1, 2) == F(2, 9)

# The filtered-swap identity has Tr(F R)=J(C)=-1/2.
Fswap = [
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
]
trace_fr = sum(
    (Fswap[i][j] * R[j][i] for i in range(4) for j in range(4)),
    F(0),
)
assert trace_fr == j_form(C) == F(-1, 2)

print("all exact coherent-Q2 exterior-reduction checks passed")
