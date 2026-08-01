#!/usr/bin/env python3
"""Dependency-free exact census for the final-slot DTH PPT crossing.

The local holomorphic module has five covariant qutrit slots.  Transposing
the final ``z`` slot changes it to four covariant slots and one
contravariant slot.  This verifier constructs every dominant weight space,
computes the common kernel of the two raising operators over the rationals,
and checks the resulting multiplicities and dimensions exactly.

It also audits, on matrix-unit indices, the two elementary partial-transpose
identities used to show that pair exchange leaves only Gamma_1 and Gamma_5
as independent PPT cuts of the tripartition (w):(w):(z).
"""

from fractions import Fraction
import itertools


D = 3
WORDS = tuple(itertools.product(range(D), repeat=5))


def local_weight(word):
    """Weight of 3^4 tensor conjugate(3), with slot four contravariant."""
    result = [0, 0, 0]
    for position, value in enumerate(word):
        result[value] += -1 if position == 4 else 1
    return tuple(result)


def raised_terms(word, simple_root):
    """Terms of E_01 or E_12 in the mixed tensor representation."""
    high = simple_root
    low = simple_root + 1
    for position, value in enumerate(word):
        if position == 4:
            # The contravariant action is minus the transpose action.
            if value == high:
                target = list(word)
                target[position] = low
                yield tuple(target), -1
        elif value == low:
            target = list(word)
            target[position] = high
            yield tuple(target), 1


def rational_rank(rows, number_of_columns):
    """Exact row rank of a sparse integer matrix."""
    matrix = [
        [Fraction(row.get(column, 0)) for column in range(number_of_columns)]
        for row in rows
        if row
    ]
    rank = 0
    for column in range(number_of_columns):
        pivot = next(
            (row for row in range(rank, len(matrix))
             if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                left - scale * right
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def highest_weight_multiplicity(weight):
    source = [word for word in WORDS if local_weight(word) == weight]
    source_index = {word: index for index, word in enumerate(source)}
    row_index = {}
    rows = []
    for simple_root in (0, 1):
        for word in source:
            column = source_index[word]
            for target, coefficient in raised_terms(word, simple_root):
                key = (simple_root, target)
                if key not in row_index:
                    row_index[key] = len(rows)
                    rows.append({})
                row = rows[row_index[key]]
                row[column] = row.get(column, 0) + coefficient
    rank = rational_rank(rows, len(source))
    return len(source) - rank, len(source), rank


def su3_label(weight):
    return weight[0] - weight[1], weight[1] - weight[2]


def carrier_dimension(label):
    p, q = label
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def transpose_subset(unit, subset):
    """Image indices of a matrix unit under a subsystem transpose."""
    row, column = unit
    row = list(row)
    column = list(column)
    for position in subset:
        row[position], column[position] = column[position], row[position]
    return tuple(row), tuple(column)


def swap_first_two_factors(unit):
    row, column = unit
    return ((row[1], row[0], row[2]),
            (column[1], column[0], column[2]))


def audit_ppt_cut_identities():
    # Small dimensions suffice because these are identities on matrix units.
    indices = tuple(itertools.product(range(2), range(2), range(3)))
    for row in indices:
        for column in indices:
            unit = (row, column)
            # S Gamma_A(.) S = Gamma_B(S . S).
            left = swap_first_two_factors(transpose_subset(unit, (0,)))
            right = transpose_subset(swap_first_two_factors(unit), (1,))
            assert left == right
            # Gamma_AB(.) = transpose(Gamma_C(.)).
            left = transpose_subset(unit, (0, 1))
            right = transpose_subset(transpose_subset(unit, (2,)), (0, 1, 2))
            assert left == right


def main():
    dominant = sorted({
        local_weight(word)
        for word in WORDS
        if local_weight(word)[0] >= local_weight(word)[1]
        >= local_weight(word)[2]
    }, reverse=True)
    expected = {
        (0, 0): 3,
        (0, 3): 2,
        (1, 1): 8,
        (2, 2): 3,
        (3, 0): 4,
        (4, 1): 1,
    }
    observed = {}
    print("dominant-weight census for 3^4 tensor conjugate(3)")
    for weight in dominant:
        multiplicity, source_dimension, raising_rank = (
            highest_weight_multiplicity(weight)
        )
        label = su3_label(weight)
        observed[label] = multiplicity
        print(
            " ", label,
            "weight", weight,
            "weight-space", source_dimension,
            "raising-rank", raising_rank,
            "multiplicity", multiplicity,
            "carrier", carrier_dimension(label),
        )
    assert observed == expected
    total_dimension = sum(
        multiplicity * carrier_dimension(label)
        for label, multiplicity in observed.items()
    )
    commutant_dimension = sum(value * value for value in observed.values())
    assert total_dimension == D ** 5 == 243
    assert commutant_dimension == 103
    assert sum(observed.values()) == 21
    audit_ppt_cut_identities()
    print("total carrier dimension:", total_dimension)
    print("commutant dimension:", commutant_dimension)
    print("global block count / reduced dimension / maximum block:",
          6 ** 3, 21 ** 3, 8 ** 3)
    print("PPT cut identities: exact matrix-unit audit passed")


if __name__ == "__main__":
    main()
