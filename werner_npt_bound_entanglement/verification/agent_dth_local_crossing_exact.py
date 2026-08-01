#!/usr/bin/env python3
"""Exact local covariant-to-mixed crossing data for the DTH lift.

This module constructs a deterministic 103-element permutation basis P_b of
the local covariant commutant and its matched mixed/walled basis

    D_b = PT_{12}(P_b).

It then computes two exact rational 103 by 103 restriction matrices:

    h = HOL_RESTRICTION * x,
    m = MIXED_RESTRICTION * x.

Thus the exact crossing is represented without a dense rational inverse by
the memory-bounded bridge (HOL_RESTRICTION, MIXED_RESTRICTION).  Both square
matrices are certified invertible modulo several primes.  In matched diagram
coordinates the crossing and inverse are literally the identity.

No external packages or floating-point arithmetic are used.
"""

from fractions import Fraction as F
from itertools import permutations, product
import sys

sys.path.insert(0, "verification")
import agent_dth_block_census as census


D = 3
NREP = 5
WORDS = list(product(range(D), repeat=NREP))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
LOCAL_DIMENSION = len(WORDS)

HOL_SHAPES = census.PARTITIONS
HOL_IRREP_DIMS = (21, 24, 15, 6, 3)
HOL_MULTS = (1, 4, 5, 6, 5)

MIXED_WEIGHTS = ((3, 2), (2, 1), (1, 0), (1, 3), (0, 2), (4, 0))
MIXED_IRREP_DIMS = (42, 15, 3, 24, 6, 15)
MIXED_MULTS = (1, 6, 6, 2, 5, 1)

EXCLUDED_LEXICOGRAPHIC_INDICES = frozenset(
    (23, 47, 71, 86, 87, 89, 95, 101, 107, 110, 111, 113, 115, 116, 117, 118, 119)
)


def selected_permutations():
    return tuple(
        permutation
        for index, permutation in enumerate(permutations(range(NREP)))
        if index not in EXCLUDED_LEXICOGRAPHIC_INDICES
    )


SELECTED_PERMUTATIONS = selected_permutations()
assert len(SELECTED_PERMUTATIONS) == 103


def clean(vector):
    return {key: value for key, value in vector.items() if value}


def add(left, right, scale=F(1)):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, F(0)) + scale * value
        if not out[key]:
            del out[key]
    return out


def dot(left, right):
    if len(left) > len(right):
        left, right = right, left
    return sum((value * right.get(key, F(0)) for key, value in left.items()), F(0))


def permutation_operator(permutation):
    """Sparse P_pi with row_word[i] = column_word[pi[i]]."""
    out = {}
    for column, word in enumerate(WORDS):
        row_word = tuple(word[permutation[position]] for position in range(NREP))
        out[(WORD_INDEX[row_word], column)] = F(1)
    return out


def partial_transpose_first_pair(operator):
    out = {}
    for (row, column), value in operator.items():
        row_word = WORDS[row]
        column_word = WORDS[column]
        new_row_word = column_word[:2] + row_word[2:]
        new_column_word = row_word[:2] + column_word[2:]
        key = (WORD_INDEX[new_row_word], WORD_INDEX[new_column_word])
        out[key] = out.get(key, F(0)) + value
    return clean(out)


def apply_operator(operator, vector):
    out = {}
    for (row, column), value in operator.items():
        coefficient = vector.get(column, F(0))
        if coefficient:
            out[row] = out.get(row, F(0)) + value * coefficient
    return clean(out)


def dictionary_word_vector(vector):
    return {WORD_INDEX[word]: F(value) for word, value in vector.items() if value}


def holomorphic_highest_weight_bases():
    result = []
    for shape, expected in zip(HOL_SHAPES, HOL_MULTS):
        basis = [
            dictionary_word_vector(vector)
            for vector in census.specht_basis(shape)
        ]
        assert len(basis) == expected
        result.append(basis)
    return result


def mixed_weight(word):
    counts = [0, 0, 0]
    for position in (2, 3, 4):
        counts[word[position]] += 1
    for position in (0, 1):
        counts[word[position]] -= 1
    return tuple(counts)


def highest_gl_weight(weight):
    p, q = weight
    third = (1 - p - 2 * q) // 3
    assert 3 * third == 1 - p - 2 * q
    return (third + q + p, third + q, third)


def raised_words(word, simple_root):
    low = simple_root + 1
    high = simple_root
    for position, value in enumerate(word):
        if position < 2:
            # Contravariant infinitesimal action -E_(low,high).
            if value == high:
                new = list(word)
                new[position] = low
                yield tuple(new), -1
        elif value == low:
            new = list(word)
            new[position] = high
            yield tuple(new), 1


def rational_nullspace(rows, columns):
    """Nullspace basis of a sparse rational row matrix.

    rows maps row labels to dictionaries column -> coefficient.
    Returned vectors are dictionaries column -> Fraction.
    """
    matrix = [dict(row) for _, row in sorted(rows.items(), key=lambda item: item[0])]
    pivot_columns = []
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row].get(column)),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = {
            key: value / pivot for key, value in matrix[pivot_row].items() if value
        }
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            coefficient = matrix[row].get(column, F(0))
            if coefficient:
                matrix[row] = add(matrix[row], matrix[pivot_row], -coefficient)
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break

    free_columns = [column for column in range(columns) if column not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = {free: F(1)}
        for row, pivot in enumerate(pivot_columns):
            coefficient = matrix[row].get(free, F(0))
            if coefficient:
                vector[pivot] = -coefficient
        basis.append(clean(vector))
    return basis


def mixed_highest_weight_bases():
    result = []
    for weight, expected in zip(MIXED_WEIGHTS, MIXED_MULTS):
        source_words = [
            word for word in WORDS if mixed_weight(word) == highest_gl_weight(weight)
        ]
        source_index = {word: index for index, word in enumerate(source_words)}
        rows = {}
        for root in (0, 1):
            for word in source_words:
                column = source_index[word]
                for target_word, coefficient in raised_words(word, root):
                    label = (root, target_word)
                    row = rows.setdefault(label, {})
                    row[column] = row.get(column, F(0)) + F(coefficient)
        kernel = rational_nullspace(rows, len(source_words))
        assert len(kernel) == expected, (weight, len(kernel), expected)
        full_basis = []
        for vector in kernel:
            full_basis.append(
                clean(
                    {
                        WORD_INDEX[source_words[column]]: coefficient
                        for column, coefficient in vector.items()
                    }
                )
            )
        result.append(full_basis)
    return result


def basis_gram(basis):
    return [[dot(left, right) for right in basis] for left in basis]


def invert_fraction_matrix(matrix):
    size = len(matrix)
    work = [
        list(map(F, row)) + [F(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        selected = next(row for row in range(column, size) if work[row][column])
        work[column], work[selected] = work[selected], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    value - coefficient * pivot_value
                    for value, pivot_value in zip(work[row], work[column])
                ]
    return [row[size:] for row in work]


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matvec(matrix, vector):
    return [
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(matrix))
    ]


def solve_fraction_system(matrix, right_hand_side):
    """Exact one-right-hand-side solve, intended for certificate recovery."""
    size = len(matrix)
    work = [
        list(map(F, matrix[row])) + [F(right_hand_side[row])]
        for row in range(size)
    ]
    for column in range(size):
        selected = next(row for row in range(column, size) if work[row][column])
        work[column], work[selected] = work[selected], work[column]
        pivot = work[column][column]
        # Eliminate below without normalizing the entire pivot row first.
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            coefficient = work[row][column] / pivot
            for j in range(column, size + 1):
                work[row][j] -= coefficient * work[column][j]
    solution = [F(0)] * size
    for row in range(size - 1, -1, -1):
        value = work[row][size] - sum(
            work[row][column] * solution[column]
            for column in range(row + 1, size)
        )
        solution[row] = value / work[row][row]
    return solution


def cross_holomorphic_to_mixed(
    holomorphic_coordinates, hol_matrix, mixed_matrix
):
    diagram_coordinates = solve_fraction_system(
        hol_matrix, holomorphic_coordinates
    )
    return matvec(mixed_matrix, diagram_coordinates)


def cross_mixed_to_holomorphic(
    mixed_coordinates, hol_matrix, mixed_matrix
):
    diagram_coordinates = solve_fraction_system(
        mixed_matrix, mixed_coordinates
    )
    return matvec(hol_matrix, diagram_coordinates)


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def trace_matrix(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def restriction_block(operator, basis):
    applied = [apply_operator(operator, vector) for vector in basis]
    return [[dot(left, right) for right in applied] for left in basis]


def flatten_blocks(blocks):
    out = []
    for block in blocks:
        for row in block:
            out.extend(row)
    return out


def exact_restriction_bridge():
    holomorphic = holomorphic_highest_weight_bases()
    mixed = mixed_highest_weight_bases()
    hol_columns = []
    mixed_columns = []
    for permutation in SELECTED_PERMUTATIONS:
        covariant = permutation_operator(permutation)
        crossed = partial_transpose_first_pair(covariant)
        hol_columns.append(
            flatten_blocks(
                [restriction_block(covariant, basis) for basis in holomorphic]
            )
        )
        mixed_columns.append(
            flatten_blocks([restriction_block(crossed, basis) for basis in mixed])
        )
    # Return row-major 103 by 103 matrices.
    hol_matrix = [list(row) for row in zip(*hol_columns)]
    mixed_matrix = [list(row) for row in zip(*mixed_columns)]
    assert len(hol_matrix) == len(mixed_matrix) == 103
    assert all(len(row) == 103 for row in hol_matrix + mixed_matrix)
    return hol_matrix, mixed_matrix, holomorphic, mixed


def fraction_mod(value, prime):
    return value.numerator % prime * pow(value.denominator % prime, -1, prime) % prime


def modular_determinant(matrix, prime):
    work = [
        [fraction_mod(value, prime) for value in row]
        for row in matrix
    ]
    determinant = 1
    for column in range(len(work)):
        selected = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if selected is None:
            return 0
        if selected != column:
            work[column], work[selected] = work[selected], work[column]
            determinant = -determinant
        pivot = work[column][column]
        determinant = determinant * pivot % prime
        inverse = pow(pivot, prime - 2, prime)
        for row in range(column + 1, len(work)):
            coefficient = work[row][column] * inverse % prime
            if coefficient:
                for j in range(column, len(work)):
                    work[row][j] = (
                        work[row][j] - coefficient * work[column][j]
                    ) % prime
    return determinant % prime


def inverse_permutation(permutation):
    out = [0] * len(permutation)
    for source, target in enumerate(permutation):
        out[target] = source
    return tuple(out)


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def cycle_count(permutation):
    seen = set()
    cycles = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycles += 1
        current = start
        while current not in seen:
            seen.add(current)
            current = permutation[current]
    return cycles


def diagram_gram():
    return [
        [
            D ** cycle_count(compose(inverse_permutation(left), right))
            for right in SELECTED_PERMUTATIONS
        ]
        for left in SELECTED_PERMUTATIONS
    ]


def block_gram_reconstruction(restriction_columns, bases, irrep_dimensions):
    """Reconstruct raw operator HS Gram from highest-weight restrictions."""
    inverse_grams = [
        invert_fraction_matrix(basis_gram(basis))
        for basis in bases
    ]
    # Split each 103-vector column into square blocks.
    offsets = []
    offset = 0
    for basis in bases:
        size = len(basis)
        offsets.append((offset, size))
        offset += size * size
    assert offset == 103

    blocks_by_column = []
    for column in range(103):
        blocks = []
        for offset, size in offsets:
            values = [
                restriction_columns[offset + i * size + j][column]
                for i in range(size)
                for j in range(size)
            ]
            blocks.append(
                [values[i * size : (i + 1) * size] for i in range(size)]
            )
        blocks_by_column.append(blocks)

    gram = [[F(0) for _ in range(103)] for _ in range(103)]
    for first in range(103):
        for second in range(first, 103):
            value = F(0)
            for block_first, block_second, inverse_gram, carrier_dimension in zip(
                blocks_by_column[first],
                blocks_by_column[second],
                inverse_grams,
                irrep_dimensions,
            ):
                product_matrix = matmul(
                    matmul(
                        matmul(inverse_gram, transpose(block_first)),
                        inverse_gram,
                    ),
                    block_second,
                )
                value += carrier_dimension * trace_matrix(product_matrix)
            gram[first][second] = gram[second][first] = value
    return gram


def exact_dependent_relations():
    """Express the seventeen omitted permutations in the selected basis."""
    pivots = {}
    selected_position = {}
    relations = {}
    basis_counter = 0
    for lex_index, permutation in enumerate(permutations(range(NREP))):
        operator = {
            row * LOCAL_DIMENSION + column: value
            for (row, column), value in permutation_operator(permutation).items()
        }
        vector = dict(operator)
        relation = {lex_index: F(1)}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                coefficient = vector[pivot]
                vector = {
                    key: value / coefficient for key, value in vector.items()
                }
                relation = {
                    key: value / coefficient for key, value in relation.items()
                }
                pivots[pivot] = (vector, relation)
                selected_position[lex_index] = basis_counter
                basis_counter += 1
                break
            old_vector, old_relation = pivots[pivot]
            coefficient = vector[pivot]
            vector = add(vector, old_vector, -coefficient)
            relation = add(relation, old_relation, -coefficient)
        else:
            dependent_coefficient = relation[lex_index]
            coordinates = [F(0)] * 103
            for old_index, coefficient in relation.items():
                if old_index == lex_index:
                    continue
                coordinates[selected_position[old_index]] = (
                    -coefficient / dependent_coefficient
                )
            relations[lex_index] = coordinates
    assert basis_counter == 103
    assert set(relations) == EXCLUDED_LEXICOGRAPHIC_INDICES
    return relations


def main():
    hol_matrix, mixed_matrix, hol_bases, mixed_bases = exact_restriction_bridge()
    primes = (1_000_003, 1_000_033, 1_000_037)
    hol_determinants = [modular_determinant(hol_matrix, prime) for prime in primes]
    mixed_determinants = [
        modular_determinant(mixed_matrix, prime) for prime in primes
    ]
    assert all(hol_determinants) and all(mixed_determinants)

    raw_gram = diagram_gram()
    assert modular_determinant(raw_gram, primes[0]) == 471279
    hol_gram = block_gram_reconstruction(hol_matrix, hol_bases, HOL_IRREP_DIMS)
    mixed_gram = block_gram_reconstruction(
        mixed_matrix, mixed_bases, MIXED_IRREP_DIMS
    )
    assert hol_gram == raw_gram
    assert mixed_gram == raw_gram

    relations = exact_dependent_relations()
    assert len(relations) == 17
    assert all(
        all(value.denominator == 1 for value in coordinates)
        for coordinates in relations.values()
    )

    # Exact forward/inverse audit on a full-support deterministic coefficient
    # vector.  Determinant nonvanishing above proves the same algorithms work
    # for every right-hand side.
    diagram_test = [F((17 * index + 5) % 23 - 11) for index in range(103)]
    hol_test = matvec(hol_matrix, diagram_test)
    mixed_test = matvec(mixed_matrix, diagram_test)
    assert cross_holomorphic_to_mixed(
        hol_test, hol_matrix, mixed_matrix
    ) == mixed_test
    assert cross_mixed_to_holomorphic(
        mixed_test, hol_matrix, mixed_matrix
    ) == hol_test

    print("exact local DTH crossing bridge passed")
    print("matched diagram basis size:", len(SELECTED_PERMUTATIONS))
    print("holomorphic restriction determinants:", hol_determinants)
    print("mixed restriction determinants:", mixed_determinants)
    print("diagram Gram determinant mod 1000003: 471279")
    print("omitted permutation relations:", len(relations), "(all integral)")
    print("crossing/inverse in matched diagram coordinates: I_103")


if __name__ == "__main__":
    main()
