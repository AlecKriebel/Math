#!/usr/bin/env python3
"""Exact local crossing bridge for the final-replica DTH partial transpose.

At one physical qutrit site, the holomorphic five-replica module is

    V^tensor5,

whereas partial transpose on the final ``z`` replica produces

    V^tensor4 tensor conjugate(V).

The invariant operator spaces on both sides have dimension 103.  This
verifier constructs rational highest-weight bases for the latter module and
the exact bridge

    h = A x,       z = B_5 x,

where ``x`` are coefficients in the same 103 selected permutation diagrams
used by ``agent_dth_local_crossing_exact.py``.  Hence the final-slot crossing
is exactly ``B_5 A^{-1}`` in highest-weight coordinates and exactly the
identity in matched diagram coordinates.  Its three-physical-site action is
the tensor cube of this local map.

No floating-point arithmetic or external package is used.
"""

from fractions import Fraction as F
from itertools import product
import sys

sys.path.insert(0, "verification")
import agent_dth_local_crossing_exact as bridge


# Dynkin labels, compatible GL(3) highest weights, carrier dimensions, and
# multiplicities in V^tensor4 tensor conjugate(V).
LAST_DYNKIN_WEIGHTS = ((4, 1), (3, 0), (2, 2), (1, 1), (0, 3), (0, 0))
LAST_GL_WEIGHTS = ((4, 0, -1), (3, 0, 0), (3, 1, -1),
                   (2, 1, 0), (2, 2, -1), (1, 1, 1))
LAST_NAMES = ("41", "30", "22", "11", "03", "00")
LAST_IRREP_DIMS = (35, 10, 27, 8, 10, 1)
LAST_MULTS = (1, 4, 3, 8, 2, 3)

assert sum(d * m for d, m in zip(LAST_IRREP_DIMS, LAST_MULTS)) == 3**5
assert sum(m * m for m in LAST_MULTS) == 103


def last_weight(word):
    """Weight of a word in V^tensor4 tensor conjugate(V)."""
    counts = [0, 0, 0]
    for position, value in enumerate(word):
        counts[value] += -1 if position == 4 else 1
    return tuple(counts)


def raised_words(word, simple_root):
    """Terms of E_01 or E_12 on V^tensor4 tensor conjugate(V)."""
    high = simple_root
    low = simple_root + 1
    for position, value in enumerate(word):
        if position == 4:
            # Contravariant infinitesimal action -E_(low,high).
            if value == high:
                out = list(word)
                out[position] = low
                yield tuple(out), -1
        elif value == low:
            out = list(word)
            out[position] = high
            yield tuple(out), 1


def last_highest_weight_bases():
    result = []
    for weight, expected in zip(LAST_GL_WEIGHTS, LAST_MULTS):
        source_words = [word for word in bridge.WORDS
                        if last_weight(word) == weight]
        source_index = {word: index for index, word in enumerate(source_words)}
        rows = {}
        for root in (0, 1):
            for word in source_words:
                column = source_index[word]
                for target_word, coefficient in raised_words(word, root):
                    label = (root, target_word)
                    row = rows.setdefault(label, {})
                    row[column] = row.get(column, F(0)) + F(coefficient)
        kernel = bridge.rational_nullspace(rows, len(source_words))
        assert len(kernel) == expected, (weight, len(kernel), expected)
        result.append([
            bridge.clean({
                bridge.WORD_INDEX[source_words[column]]: coefficient
                for column, coefficient in vector.items()
            })
            for vector in kernel
        ])
    return result


def partial_transpose_last(operator):
    """Transpose replica 5 (zero-based position 4) in a sparse operator."""
    out = {}
    for (row, column), value in operator.items():
        row_word = list(bridge.WORDS[row])
        column_word = list(bridge.WORDS[column])
        row_word[4], column_word[4] = column_word[4], row_word[4]
        key = (bridge.WORD_INDEX[tuple(row_word)],
               bridge.WORD_INDEX[tuple(column_word)])
        out[key] = out.get(key, F(0)) + value
    return bridge.clean(out)


def exact_last_restriction_bridge():
    """Return the exact 103 by 103 matrices A and B_5 and their bases."""
    holomorphic = bridge.holomorphic_highest_weight_bases()
    target = last_highest_weight_bases()
    hol_columns = []
    target_columns = []
    for permutation in bridge.SELECTED_PERMUTATIONS:
        covariant = bridge.permutation_operator(permutation)
        crossed = partial_transpose_last(covariant)
        hol_columns.append(bridge.flatten_blocks([
            bridge.restriction_block(covariant, basis)
            for basis in holomorphic
        ]))
        target_columns.append(bridge.flatten_blocks([
            bridge.restriction_block(crossed, basis)
            for basis in target
        ]))
    hol_matrix = [list(row) for row in zip(*hol_columns)]
    target_matrix = [list(row) for row in zip(*target_columns)]
    assert len(hol_matrix) == len(target_matrix) == 103
    assert all(len(row) == 103 for row in hol_matrix + target_matrix)
    return hol_matrix, target_matrix, holomorphic, target


def global_block_size_census():
    counts = {}
    for shapes in product(range(len(LAST_MULTS)), repeat=3):
        size = 1
        for shape in shapes:
            size *= LAST_MULTS[shape]
        counts[size] = counts.get(size, 0) + 1
    return counts


def main():
    hol_matrix, target_matrix, hol_bases, target_bases = (
        exact_last_restriction_bridge()
    )
    primes = (1_000_003, 1_000_033, 1_000_037)
    hol_determinants = [
        bridge.modular_determinant(hol_matrix, prime) for prime in primes
    ]
    target_determinants = [
        bridge.modular_determinant(target_matrix, prime) for prime in primes
    ]
    assert all(hol_determinants) and all(target_determinants)

    raw_gram = bridge.diagram_gram()
    hol_gram = bridge.block_gram_reconstruction(
        hol_matrix, hol_bases, bridge.HOL_IRREP_DIMS
    )
    target_gram = bridge.block_gram_reconstruction(
        target_matrix, target_bases, LAST_IRREP_DIMS
    )
    assert hol_gram == raw_gram
    assert target_gram == raw_gram

    # Forward and inverse crossing on a deterministic full-support vector.
    diagram_test = [F((19 * index + 7) % 29 - 14) for index in range(103)]
    hol_test = bridge.matvec(hol_matrix, diagram_test)
    target_test = bridge.matvec(target_matrix, diagram_test)
    assert bridge.cross_holomorphic_to_mixed(
        hol_test, hol_matrix, target_matrix
    ) == target_test
    assert bridge.cross_mixed_to_holomorphic(
        target_test, hol_matrix, target_matrix
    ) == hol_test

    source_counts = sum(1 for row in hol_matrix for value in row if value)
    target_counts = sum(1 for row in target_matrix for value in row if value)
    source_maximum = max(abs(value) for row in hol_matrix for value in row)
    target_maximum = max(abs(value) for row in target_matrix for value in row)
    basis_gram_determinants = []
    for basis in target_bases:
        gram = bridge.basis_gram(basis)
        # Bareiss-free exact determinant via modularly harmless elimination.
        determinant = F(1)
        work = [list(row) for row in gram]
        for column in range(len(work)):
            selected = next(row for row in range(column, len(work))
                            if work[row][column])
            if selected != column:
                work[column], work[selected] = work[selected], work[column]
                determinant = -determinant
            pivot = work[column][column]
            determinant *= pivot
            for row in range(column + 1, len(work)):
                coefficient = work[row][column] / pivot
                for j in range(column, len(work)):
                    work[row][j] -= coefficient * work[column][j]
        basis_gram_determinants.append(determinant)

    census = global_block_size_census()
    assert sum(census.values()) == 216
    assert sum(size * count for size, count in census.items()) == 9261
    assert sum(size * size * count for size, count in census.items()) == 103**3

    print("exact final-slot DTH crossing bridge passed")
    print("target Dynkin weights:", LAST_DYNKIN_WEIGHTS)
    print("target compatible GL weights:", LAST_GL_WEIGHTS)
    print("target carrier dimensions:", LAST_IRREP_DIMS)
    print("target multiplicities:", LAST_MULTS)
    print("target basis Gram determinants:", basis_gram_determinants)
    print("holomorphic restriction determinants:", hol_determinants)
    print("final-slot restriction determinants:", target_determinants)
    print("restriction nonzeros source/target:", source_counts, target_counts)
    print("restriction max absolute source/target:",
          source_maximum, target_maximum)
    print("global PSD block-size census:", sorted(census.items()))
    print("global blocks / summed sizes / parameters:",
          sum(census.values()),
          sum(size * count for size, count in census.items()),
          sum(size * size * count for size, count in census.items()))
    print("crossing/inverse in matched diagram coordinates: I_103")


if __name__ == "__main__":
    main()
