"""Dependency-free exact verifier for notes/agent_compression.md.

The calculation uses unnormalized integer vectors.  Their squared norms are
1, 2, 2, 4, so every normalized matrix entry remains rational.
"""

from fractions import Fraction


Bits = tuple[int, int, int, int]
Vector = dict[Bits, Fraction]


def product(left: dict[tuple[int, int], int],
            right: dict[tuple[int, int], int]) -> Vector:
    return {
        a + b: Fraction(ca * cb)
        for a, ca in left.items()
        for b, cb in right.items()
    }


def inner(left: Vector, right: Vector) -> Fraction:
    return sum((coefficient * right.get(bits, 0)
                for bits, coefficient in left.items()), Fraction(0))


def permute(vector: Vector, rule) -> Vector:
    out: Vector = {}
    for bits, coefficient in vector.items():
        image = rule(bits)
        out[image] = out.get(image, Fraction(0)) + coefficient
    return out


def r2(vector: Vector) -> Vector:
    f1 = permute(vector, lambda x: (x[2], x[1], x[0], x[3]))
    f2 = permute(vector, lambda x: (x[0], x[3], x[2], x[1]))
    f12 = permute(f1, lambda x: (x[0], x[3], x[2], x[1]))
    keys = set(vector) | set(f1) | set(f2) | set(f12)
    return {
        key: (
            vector.get(key, 0)
            - (f1.get(key, 0) + f2.get(key, 0)) / 2
            + f12.get(key, 0) / 4
        )
        for key in keys
    }


zerozero = {(0, 0): 1}
oneone = {(1, 1): 1}
s_raw = {(0, 1): 1, (1, 0): 1}

# Ordered raw basis: 00⊗11, 00⊗s, s⊗11, s⊗s.
basis = [
    product(zerozero, oneone),
    product(zerozero, s_raw),
    product(s_raw, oneone),
    product(s_raw, s_raw),
]
norm_squared = [inner(vector, vector) for vector in basis]
assert norm_squared == [1, 2, 2, 4]

raw = [[inner(left, r2(right)) for right in basis] for left in basis]

# Entries whose normalization would involve sqrt(2) are all zero.  The only
# nontrivial off-diagonal entry has normalization sqrt(1*4)=2.
assert raw[0][1] == raw[0][2] == raw[1][3] == raw[2][3] == 0
assert raw[1][0] == raw[2][0] == raw[3][1] == raw[3][2] == 0
k = [
    [raw[0][0], 0, 0, raw[0][3] / 2],
    [0, raw[1][1] / 2, raw[1][2] / 2, 0],
    [0, raw[2][1] / 2, raw[2][2] / 2, 0],
    [raw[3][0] / 2, 0, 0, raw[3][3] / 4],
]
expected = [
    [Fraction(1), 0, 0, Fraction(-1, 2)],
    [0, Fraction(1, 2), 0, 0],
    [0, 0, Fraction(1, 2), 0],
    [Fraction(-1, 2), 0, 0, Fraction(3, 4)],
]
assert k == expected

trace = sum(k[i][i] for i in range(4))
assert trace == Fraction(11, 4)

# The corner block has trace 7/4 and determinant 1/2, hence eigenvalues
# (7 ± sqrt(17))/8.  Its top eigenvalue exceeds trace(K)/2 precisely because
# sqrt(17) > 4, certified by the integer inequality 17 > 4^2.
corner_trace = k[0][0] + k[3][3]
corner_det = k[0][0] * k[3][3] - k[0][3] * k[3][0]
assert corner_trace == Fraction(7, 4)
assert corner_det == Fraction(1, 2)
assert 17 > 4**2

print("verified exact compression matrix, spectrum, and strict violation")
