#!/usr/bin/env python3
"""Exact rational pullback seeds for the cap-100 Gamma_A blocks.

The four integer vectors below live in the exact rational mixed
highest-weight bases.  They were obtained by rounding robust numerical
negative eigenvectors, but this verifier makes no numerical sign claim.  It
checks their exact Gram norms and evaluates their rank-one functionals on a
fixed collection of crossed S7 diagram triples in Fraction arithmetic.

Together with ``verify_dth_level2_local_crossing_oracle.py``, this is exact
pullback data suitable for reconstructing a rational dual functional.  It is
not an infeasibility certificate for the two-cone extension.
"""

from fractions import Fraction as F
import sys

sys.path.insert(0, "verification")
import verify_dth_level2_local_crossing_oracle as CROSSING


SEEDS = {
    (1, 2, 9): (
        0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, -1, 0, -1, 1,
        0, 0, 0, 0, 0, 0, 0, 1,
    ),
    (1, 4, 9): (
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0,
    ),
    (0, 2, 5): (
        0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
    ),
    (1, 4, 6): (
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 1, 0, -1, 1, 0, 0,
        -1, 1, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, -1, 0,
        0, 1, 0, 1, -1, -1, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -2,
        2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, -1, 1, 0, 1, -1, 0, 0,
    ),
}

EXPECTED_GRAM_NORMS = {
    (1, 2, 9): F(528),
    (1, 4, 9): F(912),
    (0, 2, 5): F(32),
    (1, 4, 6): F(696),
}

EXPECTED_SIGNATURES = {
    (1, 2, 9): (F(528), F(-528), F(240), F(240), F(0)),
    (1, 4, 9): (F(912), F(-912), F(-48), F(240), F(-432)),
    (0, 2, 5): (F(32), F(32), F(0), F(16), F(0)),
    (1, 4, 6): (F(696), F(-696), F(24), F(264), F(-8)),
}


def kron3_matvec(matrices, vector):
    dimensions = tuple(len(matrix) for matrix in matrices)
    assert len(vector) == dimensions[0] * dimensions[1] * dimensions[2]

    def index(i, j, k):
        return (i * dimensions[1] + j) * dimensions[2] + k

    output = [F(0)] * len(vector)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            for k in range(dimensions[2]):
                value = F(0)
                for a in range(dimensions[0]):
                    left = matrices[0][i][a]
                    if not left:
                        continue
                    for b in range(dimensions[1]):
                        middle = matrices[1][j][b]
                        if not middle:
                            continue
                        for c in range(dimensions[2]):
                            right = matrices[2][k][c]
                            coefficient = vector[index(a, b, c)]
                            if coefficient and right:
                                value += left * middle * right * coefficient
                output[index(i, j, k)] = value
    return tuple(output)


def dot(left, right):
    return sum(F(a) * F(b) for a, b in zip(left, right))


def exact_functional(target, vector, permutations):
    mixed = [
        CROSSING.mixed_coordinate_blocks(permutation)[index]
        for index, permutation in zip(target, permutations)
    ]
    grams = [CROSSING.MIXED_GRAMS[index] for index in target]
    image = kron3_matvec(mixed, vector)
    gram_image = kron3_matvec(grams, image)
    return dot(vector, gram_image)


def main():
    identity = tuple(range(7))
    diagrams = (
        (identity, identity, identity),
        (CROSSING.adjacent(0), identity, identity),
        (identity, CROSSING.adjacent(2), identity),
        (identity, identity, CROSSING.adjacent(4)),
        (CROSSING.adjacent(0), CROSSING.adjacent(2),
         (1, 2, 3, 4, 5, 6, 0)),
    )

    all_values = {}
    for target, vector in SEEDS.items():
        dimensions = tuple(len(CROSSING.MIXED_BASES[index]) for index in target)
        assert len(vector) == dimensions[0] * dimensions[1] * dimensions[2]
        assert any(vector)
        norm = exact_functional(target, vector, diagrams[0])
        assert norm == EXPECTED_GRAM_NORMS[target]
        values = tuple(
            exact_functional(target, vector, diagram) for diagram in diagrams
        )
        assert values == EXPECTED_SIGNATURES[target]
        all_values[target] = values

    print("exact rational Gamma_A pullback seeds passed")
    print("targets / exact Gram norms:", EXPECTED_GRAM_NORMS)
    print("exact crossed-diagram signatures:")
    for target, values in all_values.items():
        print(" ", target, values)


if __name__ == "__main__":
    main()
