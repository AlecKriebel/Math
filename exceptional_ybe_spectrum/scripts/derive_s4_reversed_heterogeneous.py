#!/usr/bin/env python3
"""Discovery helper for the reversed S4-equivariant heterogeneous branch.

This script constructs exact multiplicity-space Pauli matrices for

    V_3 tensor V_2 tensor V_3

from rational models of the standard and two-dimensional irreducible
representations of S4.  It is a derivation/search helper, not the final
certificate.
"""

from __future__ import annotations

import itertools

import sympy as sp


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def build_exact_commutant():
    permutations = list(itertools.permutations(range(4)))
    matchings = [
        frozenset((frozenset((0, 1)), frozenset((2, 3)))),
        frozenset((frozenset((0, 2)), frozenset((1, 3)))),
        frozenset((frozenset((0, 3)), frozenset((1, 2)))),
    ]
    basis_three = sp.Matrix(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, -1, -1]]
    )
    basis_two = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    metric_three = basis_three.T * basis_three
    metric_two = basis_two.T * basis_two
    metric = sp.kronecker_product(
        metric_three, metric_two, metric_three
    )
    metric_inverse = metric.inv()

    representations = []
    outer_representations = []
    characters = []
    for permutation in permutations:
        permutation_four = sp.zeros(4)
        for index in range(4):
            permutation_four[permutation[index], index] = 1
        representation_three = (
            permutation_four * basis_three
        )[:3, :]

        permutation_three = sp.zeros(3)
        for index, matching in enumerate(matchings):
            image = frozenset(
                frozenset(permutation[element] for element in pair)
                for pair in matching
            )
            permutation_three[matchings.index(image), index] = 1
        representation_two = (
            permutation_three * basis_two
        )[:2, :]

        representations.append(
            sp.kronecker_product(
                representation_three,
                representation_two,
                representation_three,
            )
        )
        outer_representations.append(
            sp.kronecker_product(
                representation_three, representation_three
            )
        )
        character_three = sum(
            permutation[index] == index for index in range(4)
        ) - 1
        character_two = sp.trace(permutation_three) - 1
        characters.append(
            (
                1,
                parity(permutation),
                character_two,
                character_three,
                parity(permutation) * character_three,
            )
        )

    dimensions = (1, 1, 2, 3, 3)
    central = []
    outer = []
    for character_index, dimension in enumerate(dimensions):
        central.append(
            sum(
                (
                    sp.Rational(
                        dimension * characters[index][character_index],
                        24,
                    )
                    * representations[index]
                    for index in range(24)
                ),
                sp.zeros(18),
            )
        )
        outer.append(
            sum(
                (
                    sp.Rational(
                        dimension * characters[index][character_index],
                        24,
                    )
                    * outer_representations[index]
                    for index in range(24)
                ),
                sp.zeros(9),
            )
        )

    def embed_outer(matrix):
        embedded = sp.zeros(18)
        for left, middle, right in itertools.product(
            range(3), range(2), range(3)
        ):
            source = (left * 2 + middle) * 3 + right
            for new_left, new_right in itertools.product(
                range(3), repeat=2
            ):
                target = (new_left * 2 + middle) * 3 + new_right
                embedded[target, source] = matrix[
                    3 * new_left + new_right,
                    3 * left + right,
                ]
        return embedded

    # The multiplicity-two copies are split by the outer V_3 tensor V_3
    # coupling channel.  The three choices below are respectively:
    # V_2 from outer 1 versus outer V_2; V_3 from outer V_3 versus V_3';
    # and V_3' from outer V_3 versus V_3'.
    low = (
        central[2] * embed_outer(outer[0]),
        central[3] * embed_outer(outer[3]),
        central[4] * embed_outer(outer[3]),
    )

    def adjoint(matrix):
        return metric_inverse * matrix.conjugate().T * metric

    inverse_representations = [
        representation.inv() for representation in representations
    ]

    def averaged_elementary(row, column):
        elementary = sp.zeros(18)
        elementary[row, column] = 1
        return sum(
            (
                representation
                * elementary
                * representation_inverse
                for representation, representation_inverse in zip(
                    representations, inverse_representations
                )
            ),
            sp.zeros(18),
        ) / 24

    # These fixed elementary matrices have nonzero averaged intertwiners.
    # The normalizations are verified below rather than assumed.
    sources = ((0, 3), (1, 0), (1, 0))
    normalizations = (sp.Integer(8), 24 * sp.sqrt(3), 8 * sp.sqrt(3))
    paulis = []
    for index, (
        central_projector,
        low_projector,
        source,
        normalization,
    ) in enumerate(zip(central[2:], low, sources, normalizations)):
        high_projector = central_projector - low_projector
        step = (
            normalization
            * high_projector
            * averaged_elementary(*source)
            * low_projector
        )
        assert sp.simplify(adjoint(step) * step - low_projector) == sp.zeros(18)
        assert sp.simplify(step * adjoint(step) - high_projector) == sp.zeros(18)
        paulis.append(
            (
                sp.simplify(step + adjoint(step)),
                sp.simplify(-sp.I * (step - adjoint(step))),
                sp.simplify(high_projector - low_projector),
            )
        )

    return {
        "metric": metric,
        "representations": representations,
        "central": tuple(central),
        "outer": tuple(outer),
        "low": low,
        "paulis": tuple(paulis),
    }


def main():
    data = build_exact_commutant()
    metric = data["metric"]
    metric_inverse = metric.inv()
    central = data["central"]
    paulis = data["paulis"]

    def adjoint(matrix):
        return metric_inverse * matrix.conjugate().T * metric

    assert sum(central, sp.zeros(18)) == sp.eye(18)
    assert [sp.trace(projector) for projector in central] == [1, 1, 4, 6, 6]
    for first in range(5):
        assert central[first] * central[first] == central[first]
        for second in range(first):
            assert central[first] * central[second] == sp.zeros(18)
    for projector, triple in zip(central[2:], paulis):
        for matrix in triple:
            assert adjoint(matrix) == matrix
            assert sp.simplify(matrix * matrix - projector) == sp.zeros(18)
            assert sp.trace(matrix) == 0
        assert sp.simplify(triple[0] * triple[1] - sp.I * triple[2]) == sp.zeros(18)
        assert sp.simplify(triple[1] * triple[2] - sp.I * triple[0]) == sp.zeros(18)
        assert sp.simplify(triple[2] * triple[0] - sp.I * triple[1]) == sp.zeros(18)

    print("central ranks:", *(sp.trace(projector) for projector in central))
    print("commutant dimension:", sum(1 if rank == 1 else 4 for rank in (1, 1, 2, 2, 2)))
    print("three exact multiplicity-space Pauli triples: verified")


if __name__ == "__main__":
    main()
