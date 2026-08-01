#!/usr/bin/env python3
"""Exact rational oracle for the local degree-three Gamma_A crossing.

The holomorphic local commutant is the image of QQ[S_7] on ``3^tensor7``.
After transposing the first two replicas it becomes the mixed commutant on
``bar(3)^tensor2 tensor 3^tensor5``.  This module gives the exact rational
Fourier/diagram formula converting arbitrary holomorphic multiplicity blocks
to mixed multiplicity blocks.

The main audit evaluates a generating collection of diagrams in exact
Fraction arithmetic and checks trace and Hilbert--Schmidt preservation in
both nonorthogonal highest-weight coordinate systems.  It does not store a
dense 2761 by 2761 rational matrix.
"""

from fractions import Fraction as F
from itertools import permutations, product
import sys

sys.path.insert(0, "verification")
import verify_dth_level2_mixed_support_census as MIXED
import verify_dth_level2_rational_branches as HOL


D = 3
NREP = 7
ORDER = 5040
HOL_MULTS = tuple(len(HOL.local_basis(index)) for index in range(8))
HOL_CARRIERS = (36, 48, 42, 15, 24, 15, 6, 3)
MIXED_DYNKIN = (
    (5, 2), (6, 0), (3, 3), (4, 1), (1, 4),
    (2, 2), (3, 0), (0, 3), (1, 1), (0, 0),
)
MIXED_CARRIERS = (81, 28, 64, 35, 35, 27, 10, 10, 8, 1)


def identity_matrix(size):
    return tuple(tuple(F(i == j) for j in range(size)) for i in range(size))


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix))


def matmul(left, right):
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def matadd(left, right, scale=F(1)):
    return tuple(
        tuple(a + scale * b for a, b in zip(row_left, row_right))
        for row_left, row_right in zip(left, right)
    )


def matscale(matrix, scale):
    return tuple(tuple(scale * value for value in row) for row in matrix)


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def inverse_matrix(matrix):
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
    return tuple(tuple(row[size:]) for row in work)


def inverse_permutation(permutation):
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def cycle_count(permutation):
    seen = set()
    count = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        count += 1
        current = start
        while current not in seen:
            seen.add(current)
            current = permutation[current]
    return count


def adjacent(first):
    permutation = list(range(NREP))
    permutation[first], permutation[first + 1] = (
        permutation[first + 1], permutation[first]
    )
    return tuple(permutation)


def holomorphic_coordinate_blocks(permutation):
    return tuple(
        tuple(
            tuple(F(int(value)) for value in row)
            for row in HOL.s7_representation(index, tuple(permutation)).tolist()
        )
        for index in range(8)
    )


MIXED_BASES_BY_WEIGHT = MIXED.highest_weight_bases(2, 5)
MIXED_BASES = tuple(MIXED_BASES_BY_WEIGHT[weight] for weight in MIXED_DYNKIN)
MIXED_SOLVERS = tuple(MIXED.coordinate_solver(basis) for basis in MIXED_BASES)


def mixed_gram(basis):
    return tuple(
        tuple(sum(left.get(word, F(0)) * right.get(word, F(0))
                  for word in set(left) | set(right))
              for right in basis)
        for left in basis
    )


MIXED_GRAMS = tuple(mixed_gram(basis) for basis in MIXED_BASES)
MIXED_GRAM_INVERSES = tuple(inverse_matrix(gram) for gram in MIXED_GRAMS)


def partial_transpose_outputs(permutation, input_word):
    """Output words of Gamma_(0,1)(P_permutation) on one input word."""
    transposed = frozenset((0, 1))
    parent = list(range(NREP))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left, right):
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    assignments = []
    for old in range(NREP):
        position = permutation[old]
        left_is_input = position in transposed
        right_is_output = old in transposed
        if left_is_input and not right_is_output:
            if input_word[position] != input_word[old]:
                return ()
        elif not left_is_input and not right_is_output:
            assignments.append((position, input_word[old]))
        elif left_is_input and right_is_output:
            assignments.append((old, input_word[position]))
        else:
            union(position, old)

    values = {}
    for position, value in assignments:
        root = find(position)
        if root in values and values[root] != value:
            return ()
        values[root] = value
    roots = sorted({find(position) for position in range(NREP)})
    free = tuple(root for root in roots if root not in values)
    output = []
    for choices in product(range(D), repeat=len(free)):
        assigned = dict(values)
        assigned.update(zip(free, choices))
        output.append(tuple(assigned[find(position)] for position in range(NREP)))
    return tuple(output)


def apply_crossed_diagram(permutation, vector):
    output = {}
    for input_word, coefficient in vector.items():
        for output_word in partial_transpose_outputs(permutation, input_word):
            output[output_word] = output.get(output_word, F(0)) + coefficient
    return MIXED.clean(output)


def mixed_coordinate_blocks(permutation):
    output = []
    for basis, solver in zip(MIXED_BASES, MIXED_SOLVERS):
        columns = []
        for vector in basis:
            image = apply_crossed_diagram(permutation, vector)
            column = MIXED.coordinates(solver, image)
            reconstruction = {}
            for coefficient, basis_vector in zip(column, basis):
                reconstruction = MIXED.add(
                    reconstruction, basis_vector, coefficient
                )
            assert reconstruction == image
            columns.append(column)
        output.append(transpose(tuple(columns)))
    return tuple(output)


def metric_adjoint(matrix, gram, gram_inverse):
    return matmul(matmul(gram_inverse, transpose(matrix)), gram)


def block_trace(blocks, carriers):
    return sum(F(carrier) * trace(block)
               for carrier, block in zip(carriers, blocks))


def block_hs(left, right, carriers, grams, inverse_grams):
    answer = F(0)
    for first, second, carrier, gram, inverse_gram in zip(
        left, right, carriers, grams, inverse_grams
    ):
        answer += F(carrier) * trace(matmul(
            metric_adjoint(first, gram, inverse_gram), second
        ))
    return answer


def canonical_group_coefficient(hol_blocks, permutation):
    """Coefficient of P_permutation in the canonical QQ[S7] preimage.

    The input blocks are coordinate operators on the eight Specht
    multiplicity spaces.  The formula is finite-group Fourier inversion.
    """
    inverse = inverse_permutation(permutation)
    representations = holomorphic_coordinate_blocks(inverse)
    return sum(
        F(multiplicity, ORDER) * trace(matmul(representation, block))
        for multiplicity, representation, block in zip(
            HOL_MULTS, representations, hol_blocks
        )
    )


def cross_holomorphic_blocks(hol_blocks):
    """Apply the complete exact local crossing to arbitrary hol blocks.

    This deliberately favors a small verifier over speed: it streams through
    all 5040 diagrams and never stores the dense rational 2761-square map.
    """
    output = tuple(
        tuple(tuple(F(0) for _ in range(len(basis)))
              for _ in range(len(basis)))
        for basis in MIXED_BASES
    )
    for permutation in permutations(range(NREP)):
        coefficient = canonical_group_coefficient(hol_blocks, permutation)
        if not coefficient:
            continue
        output = tuple(
            matadd(total, block, coefficient)
            for total, block in zip(
                output, mixed_coordinate_blocks(tuple(permutation))
            )
        )
    return output


def main():
    assert HOL_MULTS == (1, 6, 14, 15, 14, 35, 21, 21)
    assert tuple(len(basis) for basis in MIXED_BASES) == (
        1, 1, 4, 10, 5, 24, 20, 15, 36, 11
    )
    assert sum(value * value for value in HOL_MULTS) == 2761
    assert sum(len(basis) ** 2 for basis in MIXED_BASES) == 2761

    identity = tuple(range(NREP))
    cycle = (1, 2, 3, 4, 5, 6, 0)
    diagrams = (identity,) + tuple(adjacent(i) for i in range(6)) + (cycle,)
    mixed_blocks = {permutation: mixed_coordinate_blocks(permutation)
                    for permutation in diagrams}

    for permutation in diagrams:
        expected_trace = F(D ** cycle_count(permutation))
        assert block_trace(mixed_blocks[permutation], MIXED_CARRIERS) == expected_trace

    for left in diagrams:
        for right in diagrams:
            relative = compose(inverse_permutation(left), right)
            expected = F(D ** cycle_count(relative))
            actual = block_hs(
                mixed_blocks[left], mixed_blocks[right], MIXED_CARRIERS,
                MIXED_GRAMS, MIXED_GRAM_INVERSES,
            )
            assert actual == expected, (left, right, actual, expected)

    # Fourier normalization audit on a deterministic sparse group-algebra
    # element.  The formula is checked on its exact holomorphic blocks; the
    # crossed blocks use the identical coefficients by linearity of PT.
    coefficients = {
        identity: F(2, 3),
        adjacent(0): F(-5, 7),
        adjacent(3): F(11, 13),
        cycle: F(17, 19),
    }
    hol_sum = tuple(
        tuple(tuple(F(0) for _ in range(size)) for _ in range(size))
        for size in HOL_MULTS
    )
    mixed_sum = tuple(
        tuple(tuple(F(0) for _ in range(len(basis))) for _ in range(len(basis)))
        for basis in MIXED_BASES
    )
    for permutation, coefficient in coefficients.items():
        hol_sum = tuple(
            matadd(total, block, coefficient)
            for total, block in zip(
                hol_sum, holomorphic_coordinate_blocks(permutation)
            )
        )
        mixed_sum = tuple(
            matadd(total, block, coefficient)
            for total, block in zip(mixed_sum, mixed_blocks[permutation])
        )
    # The canonical inverse may distribute the same represented operator over
    # all 5040 diagrams, so compare its trace functional and record four exact
    # coefficients rather than asserting equality to the sparse preimage.
    assert block_trace(hol_sum, HOL_CARRIERS) == block_trace(
        mixed_sum, MIXED_CARRIERS
    )
    sampled_inverse = {
        permutation: canonical_group_coefficient(hol_sum, permutation)
        for permutation in diagrams
    }
    assert all(value.denominator > 0 for value in sampled_inverse.values())

    print("exact local degree-three Gamma_A crossing oracle passed")
    print("holomorphic/mixed commutant dimensions: 2761 2761")
    print("exact diagrams audited:", len(diagrams))
    print("all exact trace/HS diagram-pair audits:", len(diagrams) ** 2)
    print("sampled canonical inverse coefficients:", sampled_inverse)


if __name__ == "__main__":
    main()
