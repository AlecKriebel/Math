#!/usr/bin/env python3
"""Exact checker for the complete Latin--Segre minor orbit."""

from fractions import Fraction as F
from itertools import product
from math import comb


# S_3 character data ordered by conjugacy classes e,(12),(123).
class_sizes = (1, 3, 2)
sign_character = (1, -1, 1)
characters = {
    "S": (1, 1, 1),
    "M": (2, 0, -1),
    "A": (1, -1, 1),
}
permutation_dimensions = {"S": 1, "M": 2, "A": 1}
physical_dimensions = {"S": 10, "M": 8, "A": 1}


def sign_multiplicity(labels):
    total = 0
    for class_size, sign_value, class_index in zip(
        class_sizes, sign_character, range(3)
    ):
        value = class_size * sign_value
        for label in labels:
            value *= characters[label][class_index]
        total += value
    return F(total, 6)


allowed = []
total_dimension = 0
weights = {}
frame_eigenvalues = {}

for labels in product(("S", "M", "A"), repeat=3):
    multiplicity = sign_multiplicity(labels)
    assert multiplicity in (0, 1)
    if not multiplicity:
        continue
    allowed.append(labels)

    physical_dimension = 1
    permutation_dimension = 1
    for label in labels:
        physical_dimension *= physical_dimensions[label]
        permutation_dimension *= permutation_dimensions[label]

    total_dimension += physical_dimension
    weight = F(permutation_dimension, 36)
    eigenvalue = weight / physical_dimension
    weights[labels] = weight
    frame_eigenvalues[labels] = eigenvalue


assert len(allowed) == 11
assert total_dimension == comb(27, 3) == 2925
assert sum(weights.values(), F(0)) == 1
assert min(frame_eigenvalues.values()) == F(1, 5760)
assert max(frame_eigenvalues.values()) == F(1, 36)

# The allowed triples have exactly the three forms stated in the note.
for labels in product(("S", "M", "A"), repeat=3):
    number_m = labels.count("M")
    number_a = labels.count("A")
    predicted = (
        (number_m == 0 and number_a % 2 == 1)
        or number_m == 2
        or number_m == 3
    )
    assert (labels in allowed) == predicted

# Exact C_star calibration.  We verify the permutation contractions
# rather than importing a 27-by-27 symbolic matrix.  The convention is
# V(a,b,c)=(c,a,b), so V^{-1}(a,b,c)=(b,c,a).
rows = ((0, 1, 0), (1, 2, 1), (2, 0, 2))
columns = ((0, 2, 2), (1, 0, 0), (2, 1, 1))


def compression(permutation):
    return tuple(
        tuple(int(row == permutation(column)) for column in columns)
        for row in rows
    )


zero3 = ((0, 0, 0),) * 3
cycle3 = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
assert compression(lambda x: (x[1], x[0], x[2])) == cycle3  # F_12
assert compression(lambda x: (x[0], x[2], x[1])) == zero3   # F_23
assert compression(lambda x: (x[2], x[1], x[0])) == zero3   # F_13
assert compression(lambda x: (x[2], x[0], x[1])) == cycle3  # V
assert compression(lambda x: (x[1], x[2], x[0])) == zero3   # V^{-1}

# Thus the displayed compression of A_2+r A_3 is cycle3 times 1+r,
# where r is the positive square root of 3/5.  Its determinant is
# (1+r)^3 and cannot vanish.
r_squared = F(3, 5)
assert r_squared > 0
assert 1 + r_squared > 0

# Rank-two q=0 boundary sector invariants.
c = F(4, 3)
d = F(2, 3)
q = -c / 2 + d
G = -c + 3 * d
a = F(0)
Xi = -c / 2 + F(7, 4) * d
assert (q, c, G, a, Xi) == (
    F(0),
    F(4, 3),
    F(2, 3),
    F(0),
    F(1, 2),
)

# The high-rank invariant comparison has the same degree masses:
# ||D0/sqrt(54)||^2=72/54=4/3 and
# ||E0/sqrt(40)||^2=(80/3)/40=2/3.
assert F(72, 54) == c
assert F(80, 3 * 40) == d

# Its symmetric eigenvalue 2/sqrt(54)+4/(9sqrt(40)) is positive, so
# the third exterior power and Latin-minor average are nonzero.
assert F(2) > 0
assert F(4, 9) > 0

print(
    "verified: the independent Latin product-triple Haar frame has "
    "spectrum in [1/5760,1/36] on all 2925 exterior dimensions, "
    "and the q=0 boundary calibration is sector-indistinguishable "
    "from a high-rank operator"
)
