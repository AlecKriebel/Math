#!/usr/bin/env python3
"""Exact local census for the prolonged degree-three DTH support map.

At one physical qutrit site the partial transpose on the anchored bivector
changes the seven-replica module into

    MIXED_SOURCE = conjugate(V)^2 tensor V^5.

The support contraction evaluates the first contravariant leg against the
last (z) leg and leaves

    MIXED_TARGET = conjugate(V) tensor V^4.

This verifier constructs every highest-weight space over QQ, applies the
support contraction there, and checks its exact rank.  It also checks the
raw operator identity E E^* = 3 I.  No floating-point arithmetic or external
data files are used.
"""

from fractions import Fraction as F
from itertools import product


D = 3


def clean(vector):
    return {key: value for key, value in vector.items() if value}


def add(left, right, scale=F(1)):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, F(0)) + scale * value
        if not out[key]:
            del out[key]
    return out


def rational_nullspace(rows, columns):
    """Return an exact sparse basis for the nullspace of ``rows``."""
    matrix = [dict(row) for _, row in sorted(rows.items(), key=lambda item: item[0])]
    pivots = []
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, len(matrix))
             if matrix[row].get(column)),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = {
            key: value / pivot for key, value in matrix[pivot_row].items()
            if value
        }
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            coefficient = matrix[row].get(column, F(0))
            if coefficient:
                matrix[row] = add(matrix[row], matrix[pivot_row], -coefficient)
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = {free_column: F(1)}
        for row, pivot in enumerate(pivots):
            coefficient = matrix[row].get(free_column, F(0))
            if coefficient:
                vector[pivot] = -coefficient
        basis.append(clean(vector))
    return tuple(basis)


def sparse_rank(vectors):
    """Exact column rank of sparse rational vectors."""
    pivots = {}
    rank = 0
    for original in vectors:
        vector = dict(original)
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                coefficient = vector[pivot]
                pivots[pivot] = {
                    key: value / coefficient for key, value in vector.items()
                }
                rank += 1
                break
            coefficient = vector[pivot]
            vector = add(vector, pivots[pivot], -coefficient)
    return rank


def mixed_weight(word, contravariant_legs):
    counts = [0, 0, 0]
    for position, value in enumerate(word):
        counts[value] += -1 if position < contravariant_legs else 1
    return tuple(counts)


def raised_words(word, contravariant_legs, simple_root):
    low = simple_root + 1
    high = simple_root
    for position, value in enumerate(word):
        if position < contravariant_legs:
            # On the dual representation E_(high,low) acts as
            # -E_(low,high).
            if value == high:
                changed = list(word)
                changed[position] = low
                yield tuple(changed), -1
        elif value == low:
            changed = list(word)
            changed[position] = high
            yield tuple(changed), 1


def highest_weight_bases(contravariant_legs, covariant_legs):
    total_legs = contravariant_legs + covariant_legs
    words = tuple(product(range(D), repeat=total_legs))
    weights = sorted({mixed_weight(word, contravariant_legs) for word in words},
                     reverse=True)
    result = {}
    for weight in weights:
        if not (weight[0] >= weight[1] >= weight[2]):
            continue
        weight_words = tuple(
            word for word in words
            if mixed_weight(word, contravariant_legs) == weight
        )
        word_index = {word: index for index, word in enumerate(weight_words)}
        rows = {}
        for root in (0, 1):
            for word in weight_words:
                column = word_index[word]
                for target, coefficient in raised_words(
                    word, contravariant_legs, root
                ):
                    row = rows.setdefault((root, target), {})
                    row[column] = row.get(column, F(0)) + F(coefficient)
        kernel = rational_nullspace(rows, len(weight_words))
        if not kernel:
            continue
        dynkin = (weight[0] - weight[1], weight[1] - weight[2])
        result[dynkin] = tuple(
            clean({weight_words[column]: coefficient
                   for column, coefficient in vector.items()})
            for vector in kernel
        )
    return result


def carrier_dimension(dynkin):
    p, q = dynkin
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def support_contraction(vector):
    """E: bar(V)^2 tensor V^5 -> bar(V) tensor V^4.

    Input order is (first contravariant, retained contravariant,
    four passive covariant legs, z).  Thus E contracts positions 0 and 6.
    """
    output = {}
    for word, coefficient in vector.items():
        if word[0] != word[6]:
            continue
        target = word[1:6]
        output[target] = output.get(target, F(0)) + coefficient
    return clean(output)


def raw_support_adjoint(vector):
    """Adjoint of ``support_contraction`` on a sparse raw vector."""
    output = {}
    for word, coefficient in vector.items():
        # word=(retained contravariant, four covariant legs)
        for contracted in range(D):
            source = (contracted,) + word + (contracted,)
            output[source] = output.get(source, F(0)) + coefficient
    return clean(output)


def main():
    source = highest_weight_bases(2, 5)
    target = highest_weight_bases(1, 4)

    expected_source = {
        (5, 2): 1,
        (6, 0): 1,
        (3, 3): 4,
        (4, 1): 10,
        (1, 4): 5,
        (2, 2): 24,
        (3, 0): 20,
        (0, 3): 15,
        (1, 1): 36,
        (0, 0): 11,
    }
    expected_target = {
        (4, 1): 1,
        (2, 2): 3,
        (3, 0): 4,
        (0, 3): 2,
        (1, 1): 8,
        (0, 0): 3,
    }
    assert {weight: len(basis) for weight, basis in source.items()} == expected_source
    assert {weight: len(basis) for weight, basis in target.items()} == expected_target

    assert sum(carrier_dimension(weight) * multiplicity
               for weight, multiplicity in expected_source.items()) == 3 ** 7
    assert sum(multiplicity ** 2 for multiplicity in expected_source.values()) == 2761
    assert sum(carrier_dimension(weight) * multiplicity
               for weight, multiplicity in expected_target.items()) == 3 ** 5
    assert sum(multiplicity ** 2 for multiplicity in expected_target.values()) == 103

    ranks = {}
    for weight, basis in source.items():
        images = tuple(support_contraction(vector) for vector in basis)
        rank = sparse_rank(images)
        ranks[weight] = rank
        assert rank == expected_target.get(weight, 0)

    # Direct exact audit of E E^* = 3 I on the complete raw target basis.
    for word in product(range(D), repeat=5):
        basis_vector = {word: F(1)}
        assert support_contraction(raw_support_adjoint(basis_vector)) == {
            word: F(3)
        }

    total_rank = sum(carrier_dimension(weight) * rank
                     for weight, rank in ranks.items())
    assert total_rank == 3 ** 5
    assert 3 ** 7 - total_rank == 1944

    print("exact degree-three mixed-support census passed")
    print("source weights/multiplicities:", expected_source)
    print("target weights/multiplicities:", expected_target)
    print("highest-weight support ranks:", ranks)
    print("commutant dimensions source/target: 2761 103")
    print("raw rank/kernel: 243 1944")
    print("E E^* = 3 I_243")


if __name__ == "__main__":
    main()
