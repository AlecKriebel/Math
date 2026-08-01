#!/usr/bin/env python3
"""Exact local mixed-module census for degree-three DTH support.

After partial transpose of one bivector, one physical site carries

    conjugate(C^3)^tensor2 tensor (C^3)^tensor5.

The multiplicity of a dominant weight is the dimension of the simultaneous
kernel of the two integral raising matrices on that weight space.  Modular
row reduction gives an upper bound on every rational kernel dimension.  The
listed upper bounds already account, by the Weyl dimension formula, for all
3^7 dimensions of the module.  Complete reducibility therefore forces every
bound to be attained and proves the census exactly.

Only integer arithmetic modulo a prime and the Python standard library are
used.
"""

from collections import defaultdict
from itertools import product


D = 3
NREP = 7
PRIME = 1_000_003

EXPECTED = {
    (5, 0, -2): (1, 81),
    (5, -1, -1): (1, 28),
    (4, 1, -2): (4, 64),
    (4, 0, -1): (10, 35),
    (3, 2, -2): (5, 35),
    (3, 1, -1): (24, 27),
    (3, 0, 0): (20, 10),
    (2, 2, -1): (15, 10),
    (2, 1, 0): (36, 8),
    (1, 1, 1): (11, 1),
}

HOL_SHAPES = (
    (7,), (6, 1), (5, 2), (5, 1, 1),
    (4, 3), (4, 2, 1), (3, 3, 1), (3, 2, 2),
)


def mixed_weight(word):
    counts = [0, 0, 0]
    for position in range(2, NREP):
        counts[word[position]] += 1
    for position in range(2):
        counts[word[position]] -= 1
    return tuple(counts)


def raised_terms(word, simple_root):
    low = simple_root + 1
    high = simple_root
    for position, value in enumerate(word):
        if position < 2:
            if value == high:
                new = list(word)
                new[position] = low
                yield tuple(new), -1
        elif value == low:
            new = list(word)
            new[position] = high
            yield tuple(new), 1


def raising_matrix(words):
    rows = {}
    terms = []
    for column, word in enumerate(words):
        for root in (0, 1):
            for target, coefficient in raised_terms(word, root):
                key = (root, target)
                if key not in rows:
                    rows[key] = len(rows)
                terms.append((rows[key], column, coefficient))
    matrix = [[0] * len(words) for _ in rows]
    for row, column, coefficient in terms:
        matrix[row][column] += coefficient
    return matrix


def modular_rank(matrix, prime=PRIME):
    if not matrix:
        return 0
    matrix = [[value % prime for value in row] for row in matrix]
    rows = len(matrix)
    columns = len(matrix[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], prime - 2, prime)
        matrix[rank] = [(value * inverse) % prime
                        for value in matrix[rank]]
        pivot_row = matrix[rank]
        for row in range(rows):
            if row == rank or not matrix[row][column]:
                continue
            coefficient = matrix[row][column]
            matrix[row] = [
                (left - coefficient * right) % prime
                for left, right in zip(matrix[row], pivot_row)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def weyl_dimension(weight):
    numerator = 1
    denominator = 1
    for first in range(3):
        for second in range(first + 1, 3):
            numerator *= (
                weight[first] - weight[second] + second - first
            )
            denominator *= second - first
    assert numerator % denominator == 0
    return numerator // denominator


def hook_multiplicity(shape):
    hooks = 1
    for row, length in enumerate(shape):
        for column in range(length):
            below = sum(
                column < other_length
                for other_length in shape[row + 1:]
            )
            hooks *= length - column + below
    factorial = 1
    for value in range(2, sum(shape) + 1):
        factorial *= value
    assert factorial % hooks == 0
    return factorial // hooks


def main():
    grouped = defaultdict(list)
    for word in product(range(D), repeat=NREP):
        grouped[mixed_weight(word)].append(word)
    dominant = {
        weight: words for weight, words in grouped.items()
        if weight[0] >= weight[1] >= weight[2]
    }
    assert set(dominant) == set(EXPECTED)

    proved_upper = {}
    for weight in sorted(dominant, reverse=True):
        words = dominant[weight]
        rank = modular_rank(raising_matrix(words))
        upper = len(words) - rank
        expected, carrier = EXPECTED[weight]
        assert upper == expected
        assert weyl_dimension(weight) == carrier
        proved_upper[weight] = upper
        print("mixed weight/space/rank/multiplicity/carrier:",
              weight, len(words), rank, upper, carrier)

    # If the actual characteristic-zero multiplicities are m_weight, modular
    # rank gives m_weight <= proved_upper[weight].  Complete reducibility and
    # the equality below force equality term by term.
    capacity = sum(
        proved_upper[weight] * weyl_dimension(weight)
        for weight in dominant
    )
    assert capacity == D ** NREP

    hol_multiplicities = tuple(hook_multiplicity(shape)
                               for shape in HOL_SHAPES)
    hol_carriers = tuple(weyl_dimension(
        tuple(shape) + (0,) * (3 - len(shape))
    ) for shape in HOL_SHAPES)
    assert hol_multiplicities == (1, 6, 14, 15, 14, 35, 21, 21)
    assert hol_carriers == (36, 48, 42, 15, 24, 15, 6, 3)
    assert sum(a * b for a, b in zip(
        hol_multiplicities, hol_carriers
    )) == D ** NREP
    assert sum(value ** 2 for value in hol_multiplicities) == 2761
    assert sum(value[0] ** 2 for value in EXPECTED.values()) == 2761

    print("exact degree-three mixed S7 census passed")
    print("module/commutant dimensions:", D ** NREP, 2761)


if __name__ == "__main__":
    main()
