#!/usr/bin/env python3
"""Exact checks for the small coherent-Q2 counterpencil."""


def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gmul(a, b):
    return (
        a[0] * b[0] - a[1] * b[1],
        a[0] * b[1] + a[1] * b[0],
    )


def gconj(a):
    return (a[0], -a[1])


def gnorm(a):
    return a[0] * a[0] + a[1] * a[1]


# Binary-word order: 000,001,010,011,100,101,110,111.
x = [(4, 3), (0, 0), (0, 0), (5, 0), (0, 0), (-3, -3), (4, 2), (-9, -3)]
y = [(1, 7), (-2, -7), (4, 6), (-5, -5), (1, -7), (0, 7), (-2, -7), (3, 6)]
z = [(1, -1), (0, 0), (0, 0), (0, -2), (0, 0), (-1, 1), (1, -1), (0, -2)]
e = [(1, 0)] + [(0, 0)] * 7


def pencil(t):
    """C_t=x*y^dagger+t*z*e^dagger, with integral t."""
    return [
        [
            gadd(
                gmul(x[i], gconj(y[j])),
                gmul((t, 0), gmul(z[i], gconj(e[j]))),
            )
            for j in range(8)
        ]
        for i in range(8)
    ]


def words(length):
    return [
        tuple((number >> (length - 1 - k)) & 1 for k in range(length))
        for number in range(2 ** length)
    ]


def index(word):
    return 4 * word[0] + 2 * word[1] + word[2]


def partial_trace(matrix, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(3) if i not in traced)
    rem_words = words(len(remaining))
    trace_words = words(len(traced))
    out = [[(0, 0) for _ in rem_words] for _ in rem_words]
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
                out[ir][ic] = gadd(
                    out[ir][ic], matrix[index(row)][index(col)]
                )
    return out


def matrix_norm(matrix):
    return sum(gnorm(value) for row in matrix for value in row)


def invariants(t):
    c = pencil(t)
    n = matrix_norm(c)
    s = sum(matrix_norm(partial_trace(c, (i,))) for i in range(3))
    p = sum(
        matrix_norm(partial_trace(c, pair))
        for pair in ((0, 1), (0, 2), (1, 2))
    )
    tr = matrix_norm(partial_trace(c, (0, 1, 2)))
    return n, s, p, tr


def quadratic_coefficients(values):
    """Recover a*t^2+b*t+c from its values at t=-1,0,1."""
    minus, zero, plus = values
    assert (plus - minus) % 2 == 0
    assert (plus + minus) % 2 == 0
    return ((plus + minus) // 2 - zero, (plus - minus) // 2, zero)


samples = [invariants(t) for t in (-1, 0, 1)]
coefficients = [
    quadratic_coefficients([sample[k] for sample in samples])
    for k in range(4)
]
assert coefficients == [
    (14, 172, 71556),
    (14, 1260, 158820),
    (6, 24, 103113),
    (2, -356, 15844),
]


def gram_determinant(a, b):
    aa = sum(gnorm(value) for value in a)
    bb = sum(gnorm(value) for value in b)
    ab = (0, 0)
    for left, right in zip(a, b):
        ab = gadd(ab, gmul(gconj(left), right))
    return aa * bb - gnorm(ab)


det_xz = gram_determinant(x, z)
det_ye = gram_determinant(y, e)
exterior_square = det_xz * det_ye
assert (det_xz, det_ye, exterior_square) == (2290, 352, 806080)

# At t=1: 4*J2=3*N-2*S+P=-1819.
n, s, p, tr = invariants(1)
four_j2 = 3 * n - 2 * s + p
eight_j3 = n - s + p - tr
eight_q3 = 8 * n - 4 * s + 2 * p - tr
assert (n, s, p, tr) == (71742, 160094, 103143, 15490)
assert (four_j2, eight_j3, eight_q3) == (-1819, -699, 124356)

# Standalone violation: J2+sqrt(exterior_square)/2<0.
assert four_j2 < 0
assert four_j2 * four_j2 - 4 * exterior_square == 84441 > 0

# Coupled compensation at t=1:
# 4*(J2+2*J3+s1*s2)=-2518+4*sqrt(exterior_square)>0.
fixed_part = four_j2 + eight_j3
assert fixed_part == -2518
assert 16 * exterior_square - fixed_part * fixed_part == 6556956 > 0

# Polynomial identities from the note.  A quadratic is determined by
# its exact values at -1,0,1.
four_j2_coeffs = quadratic_coefficients(
    [3 * n0 - 2 * s0 + p0 for n0, s0, p0, _ in samples]
)
eight_j3_coeffs = quadratic_coefficients(
    [n0 - s0 + p0 - t0 for n0, s0, p0, t0 in samples]
)
eight_q3_coeffs = quadratic_coefficients(
    [8 * n0 - 4 * s0 + 2 * p0 - t0 for n0, s0, p0, t0 in samples]
)
assert four_j2_coeffs == (20, -1980, 141)
assert eight_j3_coeffs == (4, -708, 5)
assert eight_q3_coeffs == (66, -3260, 127550)

# Radical-free positivity facts used in the proof.
assert exterior_square > 672 * 672
assert 3260 * 3260 - 4 * 66 * 127550 == -23045600 < 0
assert 23045600 * 33 == 2880700 * 264

print("all exact small coherent-Q2 counterpencil checks passed")
