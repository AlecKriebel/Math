#!/usr/bin/env python3
"""Exact local censuses for the remaining degree-three DTH PPT cuts.

The degree-three Grassmann lift has seven local qutrit replicas.  Partial
transpose on ``t`` replicas changes the local covariant module to

    conjugate(C^3)^tensor(t) tensor (C^3)^tensor(7-t).

The remaining grouped cuts are represented by ``t=1`` (Gamma_z) and
``t=4`` (Gamma_AA).  We also compute ``t=3`` to audit complement/full-
transpose duality with ``t=4``.  Multiplicities are proved exactly by
modular row reduction of the two integral highest-weight raising maps.  The
resulting upper bounds exhaust all ``3^7`` dimensions, so complete
reducibility forces equality in characteristic zero.

Only the Python standard library and integer arithmetic are used.
"""

from collections import defaultdict
from itertools import product


D = 3
NREP = 7
PRIME = 1_000_003


def mixed_weight(word, transposed):
    counts = [0, 0, 0]
    for position, value in enumerate(word):
        counts[value] += -1 if position < transposed else 1
    return tuple(counts)


def raised_terms(word, simple_root, transposed):
    high = simple_root
    low = simple_root + 1
    for position, value in enumerate(word):
        if position < transposed:
            # The contragredient Lie-algebra action is -E^T.
            if value == high:
                target = list(word)
                target[position] = low
                yield tuple(target), -1
        elif value == low:
            target = list(word)
            target[position] = high
            yield tuple(target), 1


def raising_matrix(words, transposed):
    rows = {}
    terms = []
    for column, word in enumerate(words):
        for root in (0, 1):
            for target, coefficient in raised_terms(word, root, transposed):
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
        matrix[rank] = [value * inverse % prime for value in matrix[rank]]
        pivot_row = matrix[rank]
        for row in range(rows):
            if row == rank or matrix[row][column] == 0:
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
    for first in range(D):
        for second in range(first + 1, D):
            numerator *= (
                weight[first] - weight[second] + second - first
            )
            denominator *= second - first
    assert numerator % denominator == 0
    return numerator // denominator


def census(transposed):
    grouped = defaultdict(list)
    for word in product(range(D), repeat=NREP):
        grouped[mixed_weight(word, transposed)].append(word)
    dominant = {
        weight: words for weight, words in grouped.items()
        if weight[0] >= weight[1] >= weight[2]
    }
    result = {}
    for weight in sorted(dominant, reverse=True):
        words = dominant[weight]
        rank = modular_rank(raising_matrix(words, transposed))
        multiplicity = len(words) - rank
        if multiplicity:
            result[weight] = (multiplicity, weyl_dimension(weight))
    assert sum(m * d for m, d in result.values()) == D ** NREP
    return result


def dual_weight(weight):
    return tuple(-value for value in reversed(weight))


def main():
    results = {value: census(value) for value in (1, 3, 4)}
    for transposed in (1, 3, 4):
        result = results[transposed]
        assert sum(m * d for m, d in result.values()) == D ** NREP
        assert sum(m * m for m, _ in result.values()) == 2761
        print(f"t={transposed} mixed weights/multiplicities/carriers:")
        for weight, data in result.items():
            print(" ", weight, data)
        print(" irreducibles/total multiplicity/commutant:",
              len(result), sum(m for m, _ in result.values()),
              sum(m * m for m, _ in result.values()))

    # Complementary cuts differ by full transpose.  Locally this exchanges a
    # representation with its contragredient, preserving multiplicities and
    # carrier dimensions.
    expected_dual = {
        dual_weight(weight): data for weight, data in results[3].items()
    }
    assert results[4] == expected_dual

    print("exact Gamma_z/Gamma_AA local censuses passed")
    print("t=4 is the exact contragredient census of t=3")


if __name__ == "__main__":
    main()
