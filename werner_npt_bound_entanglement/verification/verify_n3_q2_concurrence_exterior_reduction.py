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

# A dense but small exact Gaussian-integer counterexample to the
# exterior inequality.  Every entry is stored as (real, imaginary).
X = [
    [(50, 38), (0, 0)], [(-18, -41), (1, -2)], [(43, 1), (0, -1)],
    [(-43, -12), (-1, 0)], [(21, 20), (0, 0)], [(-31, 10), (0, 1)],
    [(7, 1), (1, -1)], [(-1, 1), (-1, 2)], [(8, -2), (1, 0)],
    [(115, -6), (0, 0)], [(-183, -12), (-1, -1)], [(27, 31), (-1, 0)],
    [(-7, 23), (0, 0)], [(73, -20), (0, -1)], [(28, -25), (0, -1)],
    [(-92, 3), (-1, 0)], [(63, -17), (1, 2)], [(-78, 14), (1, 1)],
    [(111, 3), (0, 0)], [(-119, 41), (1, -2)], [(93, 26), (-1, -1)],
    [(-42, -21), (-1, 0)], [(49, -18), (0, -1)], [(-48, -35), (-1, 0)],
    [(-43, 63), (1, -1)], [(24, -48), (0, 3)], [(-25, 58), (2, 0)],
]
Y = [
    [(4, 2), (6, 5)], [(-3, -2), (6, -6)], [(3, 1), (8, -6)],
    [(-3, -1), (-11, -1)], [(2, 1), (1, 5)], [(-2, 0), (-8, 8)],
    [(0, 1), (9, -1)], [(0, 0), (-5, 0)], [(0, 1), (7, -4)],
    [(-6, -24), (4, -6)], [(2, 17), (-13, -3)], [(-10, -16), (-7, -2)],
    [(6, 14), (7, 7)], [(-3, -10), (10, -6)], [(8, 9), (13, -6)],
    [(4, -2), (-12, -5)], [(-3, 1), (-3, 7)], [(3, -2), (-13, 7)],
    [(-14, -5), (5, 4)], [(9, 5), (3, 2)], [(-12, 0), (9, 0)],
    [(10, 2), (-6, -7)], [(-6, -2), (0, -2)], [(7, -1), (-12, -5)],
    [(1, -3), (3, 8)], [(0, 2), (-4, 3)], [(0, -2), (9, 11)],
]


def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def gconj(a):
    return (a[0], -a[1])


def gnorm(a):
    return a[0] * a[0] + a[1] * a[1]


CG = [[(0, 0) for _ in range(27)] for _ in range(27)]
for i in range(27):
    for j in range(27):
        for a in range(2):
            CG[i][j] = gadd(CG[i][j], gmul(X[i][a], gconj(Y[j][a])))


def gpartial_trace(c, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(3) if i not in traced)
    size = 3 ** len(remaining)
    out = [[(0, 0) for _ in range(size)] for _ in range(size)]

    def words(length):
        if length == 0:
            return [()]
        return [
            tuple((index // (3 ** (length - 1 - k))) % 3
                  for k in range(length))
            for index in range(3 ** length)
        ]

    def index(word):
        return 9 * word[0] + 3 * word[1] + word[2]

    rem_words = words(len(remaining))
    trace_words = words(len(traced))
    for ir, rr in enumerate(rem_words):
        for ic, cc in enumerate(rem_words):
            for tt in trace_words:
                row = [0, 0, 0]
                col = [0, 0, 0]
                for position, site in enumerate(remaining):
                    row[site] = rr[position]
                    col[site] = cc[position]
                for position, site in enumerate(traced):
                    row[site] = col[site] = tt[position]
                out[ir][ic] = gadd(out[ir][ic], c[index(row)][index(col)])
    return out


def gmatrix_norm(a):
    return sum(gnorm(x) for row in a for x in row)


N = gmatrix_norm(CG)
single_mass = sum(gmatrix_norm(gpartial_trace(CG, (i,))) for i in range(3))
pair_mass = sum(
    gmatrix_norm(gpartial_trace(CG, pair))
    for pair in ((0, 1), (0, 2), (1, 2))
)
full_trace = gpartial_trace(CG, (0, 1, 2))[0][0]
full_trace_norm = gnorm(full_trace)
four_J = 3 * N - 2 * single_mass + pair_mass
eight_Q3 = 8 * N - 4 * single_mass + 2 * pair_mass - full_trace_norm


def gram_determinant(z):
    g00 = sum(gnorm(z[i][0]) for i in range(27))
    g11 = sum(gnorm(z[i][1]) for i in range(27))
    g01 = (0, 0)
    for i in range(27):
        g01 = gadd(g01, gmul(gconj(z[i][0]), z[i][1]))
    return g00 * g11 - gnorm(g01)


det_x = gram_determinant(X)
det_y = gram_determinant(Y)
exterior_square = det_x * det_y

assert (N, single_mass, pair_mass) == (369939292, 842955888, 560431501)
assert four_J == -15662399
assert (det_x, det_y) == (7849591, 6444692)
assert exterior_square == 50588196320972
assert full_trace == (-6525, 6981)
assert full_trace_norm == 91309986
assert eight_Q3 == 617243800
assert eight_Q3 // 8 == 77155475 > 0

# J=four_J/4 is negative, and |J| exceeds sqrt(exterior_square)/2.
# This is checked without radicals.
assert four_J < 0
assert four_J * four_J - 4 * exterior_square == 42957957151313 > 0

print("all exact coherent-Q2 exterior-reduction checks passed")
