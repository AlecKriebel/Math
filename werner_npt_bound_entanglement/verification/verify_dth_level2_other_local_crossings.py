#!/usr/bin/env python3
"""Exact diagram audits for the Gamma_z and Gamma_AA local crossings.

For a subset ``S`` of the seven local replicas, this verifier restricts
``Gamma_S(P_pi)`` to exact rational highest-weight multiplicity bases of

    conjugate(C^3)^tensor(|S|) tensor (C^3)^tensor(7-|S|).

It audits a generating family of S7 diagrams using exact trace and
Hilbert--Schmidt identities.  The same blocks are the matrix-free crossing
oracle used in the finite-group Fourier formula.  No floating-point
arithmetic or external cache is used.
"""

from fractions import Fraction as F
from itertools import product
import sys


sys.path.insert(0, "verification")
import verify_dth_level2_mixed_support_census as MIXED


D = 3
NREP = 7
CUTS = {
    "gamma_z": frozenset((6,)),
    "gamma_aa": frozenset((0, 1, 2, 3)),
    "gamma_az": frozenset((0, 1, 6)),
}

EXPECTED = {
    "gamma_z": {
        (6, 1): (1, 63),
        (4, 2): (5, 60),
        (5, 0): (6, 21),
        (2, 3): (9, 42),
        (3, 1): (24, 24),
        (0, 4): (5, 15),
        (1, 2): (30, 15),
        (2, 0): (26, 6),
        (0, 1): (21, 3),
    },
    "gamma_aa": {
        (3, 4): (1, 90),
        (4, 2): (3, 60),
        (5, 0): (2, 21),
        (1, 5): (2, 48),
        (2, 3): (12, 42),
        (3, 1): (18, 24),
        (0, 4): (9, 15),
        (1, 2): (33, 15),
        (2, 0): (24, 6),
        (0, 1): (23, 3),
    },
    "gamma_az": {
        (4, 3): (1, 90),
        (5, 1): (2, 48),
        (2, 4): (3, 60),
        (3, 2): (12, 42),
        (4, 0): (9, 15),
        (0, 5): (2, 21),
        (1, 3): (18, 24),
        (2, 1): (33, 15),
        (0, 2): (24, 6),
        (1, 0): (23, 3),
    },
}


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


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def inverse_matrix(matrix):
    size = len(matrix)
    work = [
        list(map(F, row)) + [F(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        selected = next(row for row in range(column, size)
                        if work[row][column])
        work[column], work[selected] = work[selected], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    left - coefficient * right
                    for left, right in zip(work[row], work[column])
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
        value = start
        while value not in seen:
            seen.add(value)
            value = permutation[value]
    return count


def adjacent(first):
    output = list(range(NREP))
    output[first], output[first + 1] = output[first + 1], output[first]
    return tuple(output)


def relocate_basis(vector, transposed):
    """Move the standard leading contravariant legs to ``transposed``."""
    order = tuple(sorted(transposed)) + tuple(
        position for position in range(NREP) if position not in transposed
    )
    output = {}
    for word, coefficient in vector.items():
        changed = [None] * NREP
        for source, target in enumerate(order):
            changed[target] = word[source]
        changed = tuple(changed)
        output[changed] = output.get(changed, F(0)) + coefficient
    return MIXED.clean(output)


def exact_bases(cut):
    transposed = CUTS[cut]
    standard = MIXED.highest_weight_bases(
        len(transposed), NREP - len(transposed)
    )
    output = {
        dynkin: tuple(relocate_basis(vector, transposed) for vector in basis)
        for dynkin, basis in standard.items()
    }
    expected = EXPECTED[cut]
    assert {
        dynkin: (len(basis), MIXED.carrier_dimension(dynkin))
        for dynkin, basis in output.items()
    } == expected
    return output


def partial_transpose_outputs(permutation, input_word, transposed):
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
        output.append(tuple(
            assigned[find(position)] for position in range(NREP)
        ))
    return tuple(output)


def apply_crossed_diagram(permutation, vector, transposed):
    output = {}
    for input_word, coefficient in vector.items():
        for output_word in partial_transpose_outputs(
            permutation, input_word, transposed
        ):
            output[output_word] = output.get(output_word, F(0)) + coefficient
    return MIXED.clean(output)


def coordinate_blocks(permutation, bases, transposed):
    output = {}
    for dynkin, basis in bases.items():
        solver = MIXED.coordinate_solver(basis)
        columns = []
        for vector in basis:
            image = apply_crossed_diagram(permutation, vector, transposed)
            column = MIXED.coordinates(solver, image)
            reconstruction = {}
            for coefficient, basis_vector in zip(column, basis):
                reconstruction = MIXED.add(
                    reconstruction, basis_vector, coefficient
                )
            assert reconstruction == image
            columns.append(column)
        output[dynkin] = transpose(tuple(columns))
    return output


def gram_matrix(basis):
    return tuple(
        tuple(sum(
            left.get(word, F(0)) * right.get(word, F(0))
            for word in set(left) | set(right)
        ) for right in basis)
        for left in basis
    )


def metric_adjoint(matrix, gram, gram_inverse):
    return matmul(matmul(gram_inverse, transpose(matrix)), gram)


def block_trace(blocks, bases):
    return sum(
        F(MIXED.carrier_dimension(dynkin)) * trace(blocks[dynkin])
        for dynkin in bases
    )


def block_hs(left, right, bases, grams, inverse_grams):
    answer = F(0)
    for dynkin in bases:
        answer += F(MIXED.carrier_dimension(dynkin)) * trace(matmul(
            metric_adjoint(
                left[dynkin], grams[dynkin], inverse_grams[dynkin]
            ),
            right[dynkin],
        ))
    return answer


def audit_cut(cut):
    transposed = CUTS[cut]
    bases = exact_bases(cut)
    assert sum(
        len(basis) * MIXED.carrier_dimension(dynkin)
        for dynkin, basis in bases.items()
    ) == D ** NREP
    assert sum(len(basis) ** 2 for basis in bases.values()) == 2761

    grams = {dynkin: gram_matrix(basis)
             for dynkin, basis in bases.items()}
    inverses = {dynkin: inverse_matrix(gram)
                for dynkin, gram in grams.items()}
    identity = tuple(range(NREP))
    cycle = (1, 2, 3, 4, 5, 6, 0)
    diagrams = (identity,) + tuple(adjacent(i) for i in range(6)) + (cycle,)
    blocks = {
        permutation: coordinate_blocks(permutation, bases, transposed)
        for permutation in diagrams
    }
    for permutation in diagrams:
        assert block_trace(blocks[permutation], bases) == F(
            D ** cycle_count(permutation)
        )
    for left in diagrams:
        for right in diagrams:
            relative = compose(inverse_permutation(left), right)
            assert block_hs(
                blocks[left], blocks[right], bases, grams, inverses
            ) == F(D ** cycle_count(relative))
    print(cut, "exact diagram crossing audit passed; types:", len(bases))


def main():
    audit_cut("gamma_z")
    audit_cut("gamma_aa")
    audit_cut("gamma_az")
    print("exact Gamma_z/Gamma_AA local crossing audits passed")


if __name__ == "__main__":
    main()
