#!/usr/bin/env python3
"""Small exact checker for the n=3 unshifted-minor structural audit."""

from fractions import Fraction
from itertools import combinations


def strong_defect(k: int, r: int) -> int:
    """Sector eigenvalue of 8 Q3(H)-[2 Tr(H^2)-(Tr H)^2]."""

    return (-1) ** k * (3**r - 2) + 1


def target(k: int, r: int) -> int:
    """Twice the coefficients used below, avoiding fractions."""

    rows = ((0, 1, 4, 13), (1, 0, -3, -12))
    return 2 * rows[k][r]


# The corrected unrestricted defect is exactly half of the already proved
# strong PSD n=3 defect kernel, evaluated crosswise rather than diagonally.
for k in range(2):
    for r in range(4):
        assert target(k, r) == strong_defect(k, r)


def projector_defect(weight: int) -> int:
    return 1 if weight == 2 else -3 if weight == 3 else 0


def grouped_rows(kind: str):
    rows = []
    for k in range(2):
        row = []
        for r in range(4):
            bits = [1] * r + [0] * (3 - r)
            values = []
            if kind == "Ki":
                for i in range(3):
                    values.append(
                        projector_defect((k ^ bits[i]) + r - bits[i])
                    )
            elif kind == "ij":
                for i, j in combinations(range(3), 2):
                    remaining = 3 - i - j
                    values.append(
                        projector_defect(
                            k + (bits[i] ^ bits[j]) + bits[remaining]
                        )
                    )
            elif kind == "omit":
                for omitted in range(3):
                    values.append(
                        projector_defect(
                            k
                            + sum(
                                bits[i] for i in range(3) if i != omitted
                            )
                        )
                    )
            else:
                raise ValueError(kind)
            row.append(sum(values))
        rows.append(tuple(row))
    return tuple(rows)


A = grouped_rows("Ki")
B = grouped_rows("ij")
C = grouped_rows("omit")
assert A == ((0, 0, 3, -9), (0, 2, -3, 3))
assert B == ((0, 0, 2, 0), (0, 3, -6, 3))
assert C == ((0, 0, 1, 3), (0, 2, -1, -9))

# A nonnegative combination a A+b B+c C plus coordinatewise nonnegative
# sector masses cannot equal D.  At (k,r)=(1,1), D is zero while these
# three coefficients are 2,3,2.  Hence a=b=c=0, which cannot generate
# either negative coefficient of D.
assert (A[1][1], B[1][1], C[1][1]) == (2, 3, 2)
assert target(1, 1) == 0
assert target(1, 2) < 0 and target(1, 3) < 0


def n_diagonal(x, y):
    answer = 1
    for a, b in zip(x, y):
        answer *= 2 - int(a == b)
    return answer


def n_element(x, y, z, w):
    answer = 1
    for a, b, c, d in zip(x, y, z, w):
        answer *= 2 * int(a == c) * int(b == d) - int(a == d) * int(b == c)
    return answer


# Exact obstruction to "ordinary Cauchy--Schwarz plus crossed-energy
# Monge".  The true unshifted determinant is equality, while the attempted
# comparison of its two Cauchy--Schwarz diagonal norms loses a factor 64.
u1 = v1 = (0, 0, 0)
u2 = v2 = (1, 1, 1)
a11 = n_diagonal(u1, v1)
a22 = n_diagonal(u2, v2)
a12 = n_diagonal(u1, v2)
a21 = n_diagonal(u2, v1)
h = n_element(u1, v2, u2, v1)
assert (a11, a22, a12, a21, h) == (1, 1, 8, 8, -1)
assert h * h == a11 * a22
assert a12 * a21 == 64 * a11 * a22

print("verified exact n=3 unshifted-minor sector identities")
print("target D is one half of the crossed strong-PSD defect kernel")
print("natural grouped sector cone is obstructed at (k,r)=(1,1)")
print("crossed-energy Monge loses the exact factor 64 at determinant equality")


# Separate Hermitian-quadrature positivity cannot settle the rank-two
# nonnormal problem.  Here is an exact inertia-(2,2) Hermitian matrix with
# negative Q3.  Use A=diag(1,1,-2), B=-A, and
#
#     D = I tensor A + B tensor I = I tensor A - A tensor I.
#
# Its only nonzero diagonal entries are two +3's and two -3's.  Because A
# is traceless and L(I_3)=-I_3/2, one has
#
#     (L tensor L)(D) = -D/2.
#
# Tensoring D/6 with a rank-one qutrit projection R contributes the
# additional exact factor Q1(R)=1/2.
a_diagonal = (1, 1, -2)
d_diagonal = tuple(
    a_diagonal[column] - a_diagonal[row]
    for row in range(3)
    for column in range(3)
)
assert sorted(x for x in d_diagonal if x) == [-3, -3, 3, 3]
d_norm_squared = sum(x * x for x in d_diagonal)
assert d_norm_squared == 36
q2_d = -d_norm_squared // 2
assert q2_d == -18
q3_h = Fraction(q2_d, 36) * Fraction(1, 2)
assert q3_h == Fraction(-1, 4)

print("verified exact inertia-(2,2) obstruction Q3((D/6) tensor R)=-1/4")
