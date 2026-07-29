#!/usr/bin/env python3
"""Dependency-free exact checks for the local S4 recoupling no-go."""

from fractions import Fraction as Q
from itertools import combinations, permutations, product


def compose(p, q):
    """Permutation p after q."""
    return tuple(p[q[i]] for i in range(4))


IDENTITY = tuple(range(4))


def transposition(i, j):
    p = list(IDENTITY)
    p[i], p[j] = p[j], p[i]
    return tuple(p)


F1 = transposition(0, 2)
F2 = transposition(1, 3)
LEFT = transposition(0, 1)
RIGHT = transposition(2, 3)


def cycle_type(p):
    seen = set()
    lengths = []
    for i in range(4):
        if i in seen:
            continue
        j = i
        length = 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = p[j]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


CHARACTERS = {
    "4": {(1, 1, 1, 1): 1, (2, 1, 1): 1, (2, 2): 1,
          (3, 1): 1, (4,): 1},
    "31": {(1, 1, 1, 1): 3, (2, 1, 1): 1, (2, 2): -1,
           (3, 1): 0, (4,): -1},
    "22": {(1, 1, 1, 1): 2, (2, 1, 1): 0, (2, 2): 2,
           (3, 1): -1, (4,): 0},
    "211": {(1, 1, 1, 1): 3, (2, 1, 1): -1, (2, 2): -1,
            (3, 1): 0, (4,): 1},
    "1111": {(1, 1, 1, 1): 1, (2, 1, 1): -1, (2, 2): 1,
             (3, 1): 1, (4,): -1},
}


ORDERS = {
    "4": ((1, 1),),
    "31": ((1, 1), (1, -1), (-1, 1)),
    "22": ((1, 1), (-1, -1)),
    "211": ((1, -1), (-1, 1), (-1, -1)),
    "1111": ((-1, -1),),
}


EXPECTED_SQUARES = {
    "4": ((Q(1),),),
    "31": (
        (Q(0), Q(1, 2), Q(1, 2)),
        (Q(1, 2), Q(1, 4), Q(1, 4)),
        (Q(1, 2), Q(1, 4), Q(1, 4)),
    ),
    "22": ((Q(1, 4), Q(3, 4)), (Q(3, 4), Q(1, 4))),
    "211": (
        (Q(1, 4), Q(1, 4), Q(1, 2)),
        (Q(1, 4), Q(1, 4), Q(1, 2)),
        (Q(1, 2), Q(1, 2), Q(0)),
    ),
    "1111": ((Q(1),),),
}


def character_rank(character, a, b):
    elements = (
        (1, IDENTITY),
        (a, F1),
        (b, F2),
        (a * b, compose(F1, F2)),
    )
    return sum(c * character[cycle_type(g)] for c, g in elements) // 4


def overlap(character, a, b, sigma, tau):
    vertical = (
        (1, IDENTITY),
        (a, F1),
        (b, F2),
        (a * b, compose(F1, F2)),
    )
    horizontal = (
        (1, IDENTITY),
        (sigma, LEFT),
        (tau, RIGHT),
        (sigma * tau, compose(LEFT, RIGHT)),
    )
    return Q(sum(
        cv * ch * character[cycle_type(compose(g, h))]
        for cv, g in vertical
        for ch, h in horizontal
    ), 16)


def check_recoupling_squares():
    for name, order in ORDERS.items():
        character = CHARACTERS[name]
        nonzero = tuple(
            signs for signs in product((1, -1), repeat=2)
            if character_rank(character, *signs)
        )
        assert nonzero == order
        table = tuple(
            tuple(overlap(character, *v, *h) for h in order)
            for v in order
        )
        assert table == EXPECTED_SQUARES[name]


class QRoot:
    """a+b*sqrt(n), with exact rational a,b."""

    def __init__(self, a=0, b=0, n=2):
        self.a = Q(a)
        self.b = Q(b)
        self.n = n

    def __add__(self, other):
        other = as_root(other, self.n)
        return QRoot(self.a + other.a, self.b + other.b, self.n)

    __radd__ = __add__

    def __neg__(self):
        return QRoot(-self.a, -self.b, self.n)

    def __sub__(self, other):
        return self + (-as_root(other, self.n))

    def __rsub__(self, other):
        return as_root(other, self.n) - self

    def __mul__(self, other):
        other = as_root(other, self.n)
        return QRoot(
            self.a * other.a + self.n * self.b * other.b,
            self.a * other.b + self.b * other.a,
            self.n,
        )

    __rmul__ = __mul__

    def __eq__(self, other):
        other = as_root(other, self.n)
        return self.a == other.a and self.b == other.b


def as_root(value, n):
    if isinstance(value, QRoot):
        assert value.n == n
        return value
    return QRoot(value, 0, n)


def check_orthogonal(matrix):
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            value = sum(matrix[i][k] * matrix[j][k] for k in range(size))
            assert value == (1 if i == j else 0)


def check_signed_recoupling_matrices():
    r2 = QRoot(0, Q(1, 2), 2)  # 1/sqrt(2)
    r3 = QRoot(0, Q(1, 2), 3)  # sqrt(3)/2
    u31 = (
        (QRoot(0, 0, 2), r2, r2),
        (r2, QRoot(Q(1, 2), 0, 2), QRoot(Q(-1, 2), 0, 2)),
        (r2, QRoot(Q(-1, 2), 0, 2), QRoot(Q(1, 2), 0, 2)),
    )
    u22 = (
        (QRoot(Q(1, 2), 0, 3), r3),
        (r3, QRoot(Q(-1, 2), 0, 3)),
    )
    u211 = (
        (QRoot(Q(1, 2), 0, 2), QRoot(Q(-1, 2), 0, 2), r2),
        (QRoot(Q(-1, 2), 0, 2), QRoot(Q(1, 2), 0, 2), r2),
        (r2, r2, QRoot(0, 0, 2)),
    )
    check_orthogonal(u31)
    check_orthogonal(u22)
    check_orthogonal(u211)


def check_negative_block_arithmetic():
    y = (Q(2, 3), Q(2, 3), Q(2), Q(22, 3))
    h = tuple(value * value for value in y)
    probabilities = (
        Q(1, 64),
        Q(9, 64),
        Q(27, 64),
        Q(27, 64),
    )
    transformed = sum(probabilities[q] * h[q] for q in range(4))
    assert transformed == Q(220, 9)
    assert h[0] - transformed == Q(-24)


LOCAL_XI = {
    (1, 1, 0, 0): -1,
    (1, 0, 1, 0): 2,
    (1, 0, 0, 1): -1,
    (0, 1, 1, 0): -1,
    (0, 1, 0, 1): 2,
    (0, 0, 1, 1): -1,
}


def permute_local_word(word, permutation):
    out = [0] * 4
    for i, value in enumerate(word):
        out[permutation[i]] = value
    return tuple(out)


def check_physical_xi():
    assert sum(value * value for value in LOCAL_XI.values()) == 12
    for generator in (F1, F2):
        moved = {
            permute_local_word(word, generator): value
            for word, value in LOCAL_XI.items()
        }
        assert moved == LOCAL_XI

    # Verify that the central [2,2] idempotent fixes xi.
    projected = {}
    character = CHARACTERS["22"]
    for permutation in permutations(range(4)):
        coefficient = Q(2 * character[cycle_type(permutation)], 24)
        if not coefficient:
            continue
        for word, value in LOCAL_XI.items():
            moved = permute_local_word(word, permutation)
            projected[moved] = projected.get(moved, Q(0)) + coefficient * value
    assert projected == {word: Q(value) for word, value in LOCAL_XI.items()}

    # The displayed 4 x 4 coefficient matrix has determinant -3.
    matrix = (
        (0, 0, 0, -1),
        (0, 2, -1, 0),
        (0, -1, 2, 0),
        (-1, 0, 0, 0),
    )
    determinant = 0
    for permutation in permutations(range(4)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(4) for j in range(i + 1, 4)
        )
        term = (-1) ** inversions
        for i in range(4):
            term *= matrix[i][permutation[i]]
        determinant += term
    assert determinant == -3


def swap_global(word, site, first, second):
    out = list(word)
    i = 4 * site + first
    j = 4 * site + second
    out[i], out[j] = out[j], out[i]
    return tuple(out)


def apply_group_word(word, mask1=0, mask2=0, left=False, right=False):
    # The rightmost operator acts first.
    if right:
        for site in range(3):
            word = swap_global(word, site, 2, 3)
    for site in range(3):
        if (mask2 >> site) & 1:
            word = swap_global(word, site, 1, 3)
        if (mask1 >> site) & 1:
            word = swap_global(word, site, 0, 2)
    if left:
        for site in range(3):
            word = swap_global(word, site, 0, 1)
    return word


def check_direct_three_site_contraction():
    xi3 = {}
    for first, second, third in product(LOCAL_XI, repeat=3):
        xi3[first + second + third] = (
            LOCAL_XI[first] * LOCAL_XI[second] * LOCAL_XI[third]
        )
    norm_squared = sum(value * value for value in xi3.values())
    assert len(xi3) == 216
    assert norm_squared == 12 ** 3

    def expectation(mask1=0, mask2=0, left=False, right=False):
        numerator = sum(
            value * xi3.get(
                apply_group_word(word, mask1, mask2, left, right), 0
            )
            for word, value in xi3.items()
        )
        return Q(numerator, norm_squared)

    coefficients = {
        mask: (Q(2), Q(-1), Q(2, 3), Q(-1, 3))[
            bin(mask).count("1")
        ]
        for mask in range(8)
    }
    h_value = sum(
        coefficients[a] * coefficients[b] * expectation(a, b)
        for a in range(8) for b in range(8)
    )
    crossed_value = sum(
        coefficients[a] * coefficients[b]
        * expectation(a, b, left=True, right=True)
        for a in range(8) for b in range(8)
    )
    assert h_value == Q(4, 9)
    assert crossed_value == Q(220, 9)
    assert h_value - crossed_value == Q(-24)


def check_false_marginal_feature_bound():
    u = ((0, 0, 0), (2, 2, 2))
    v = ((0, 0, 0), (1, 0, 0))

    def local_parity_element(x, y, xp, yp, antisymmetric):
        direct = int(x == xp and y == yp)
        swapped = int(x == yp and y == xp)
        return Q(direct - swapped if antisymmetric else direct + swapped, 2)

    def sector_element(x, y, xp, yp, antisymmetric_sites):
        return product_fraction(
            local_parity_element(
                x[site], y[site], xp[site], yp[site],
                site in antisymmetric_sites,
            )
            for site in range(3)
        )

    logical = []
    for r, s in product(range(2), repeat=2):
        logical.append((u[r], v[s]))

    k_feature = [[Q(0) for _ in range(4)] for _ in range(4)]
    for row, (x, y) in enumerate(logical):
        for column, (xp, yp) in enumerate(logical):
            exact_two = sum(
                sector_element(x, y, xp, yp, set(pair))
                for pair in combinations(range(3), 2)
            )
            exact_three = sector_element(x, y, xp, yp, {0, 1, 2})
            k_feature[row][column] = Q(4, 9) * exact_two + Q(20, 9) * exact_three

    expected = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(4, 9), Q(0)),
        (Q(0), Q(0), Q(0), Q(4, 9)),
    )
    assert tuple(tuple(row) for row in k_feature) == expected
    trace_b = (
        (k_feature[0][0] + k_feature[1][1],
         k_feature[0][2] + k_feature[1][3]),
        (k_feature[2][0] + k_feature[3][1],
         k_feature[2][2] + k_feature[3][3]),
    )
    assert trace_b == ((Q(0), Q(0)), (Q(0), Q(8, 9)))
    assert Q(4, 9) - (Q(2, 9) + Q(0)) == Q(2, 9)


def product_fraction(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def main():
    check_recoupling_squares()
    check_signed_recoupling_matrices()
    check_negative_block_arithmetic()
    check_physical_xi()
    check_direct_three_site_contraction()
    check_false_marginal_feature_bound()
    print("local S4 recoupling and exact -24 relaxation: PASS")


if __name__ == "__main__":
    main()
