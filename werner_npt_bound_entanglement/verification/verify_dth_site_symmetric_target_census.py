#!/usr/bin/env python3
"""Exact site-symmetric five-replica DTH target census.

The complete constrained five-replica moment has 4,139 real-symmetric
highest-weight coordinates.  Averaging over permutations of the three
physical qutrit sites preserves every defining cone constraint and the DTH
witness.  This verifier computes, over QQ, the invariant coordinate count in
each unordered local S_5 shape triple and proves that only 761 equations
remain.

SymPy is used for exact rational matrix arithmetic.  No floating-point rank
or character decision occurs.
"""

from itertools import combinations_with_replacement, product
from pathlib import Path
import importlib.util

import sympy as sp


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "dth_site_symmetric_exact_k", HERE / "agent_dth_exact_k_coordinates.py"
)
EXACT_K = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(EXACT_K)


EXPECTED = {
    (0, 0, 0): (0, "aaa", (0, 0, 0), 0),
    (0, 0, 1): (0, "aab", (0, 0), 0),
    (0, 0, 2): (1, "aab", (1, 0), 1),
    (0, 0, 3): (0, "aab", (0, 0), 0),
    (0, 0, 4): (1, "aab", (1, 0), 1),
    (0, 1, 1): (1, "aab", (1, 0), 1),
    (0, 1, 2): (2, "abc", (), 3),
    (0, 1, 3): (2, "abc", (), 3),
    (0, 1, 4): (2, "abc", (), 3),
    (0, 2, 2): (2, "aab", (2, 0), 3),
    (0, 2, 3): (2, "abc", (), 3),
    (0, 2, 4): (2, "abc", (), 3),
    (0, 3, 3): (4, "aab", (3, 1), 7),
    (0, 3, 4): (2, "abc", (), 3),
    (0, 4, 4): (2, "aab", (2, 0), 3),
    (1, 1, 1): (5, "aaa", (1, 0, 2), 4),
    (1, 1, 2): (7, "aab", (5, 2), 18),
    (1, 1, 3): (8, "aab", (4, 4), 20),
    (1, 1, 4): (7, "aab", (5, 2), 18),
    (1, 2, 2): (8, "aab", (5, 3), 21),
    (1, 2, 3): (10, "abc", (), 55),
    (1, 2, 4): (8, "abc", (), 36),
    (1, 3, 3): (12, "aab", (7, 5), 43),
    (1, 3, 4): (10, "abc", (), 55),
    (1, 4, 4): (8, "aab", (5, 3), 21),
    (2, 2, 2): (11, "aaa", (3, 0, 4), 16),
    (2, 2, 3): (12, "aab", (6, 6), 42),
    (2, 2, 4): (11, "aab", (7, 4), 38),
    (2, 3, 3): (16, "aab", (10, 6), 76),
    (2, 3, 4): (12, "abc", (), 78),
    (2, 4, 4): (11, "aab", (7, 4), 38),
    (3, 3, 3): (16, "aaa", (2, 2, 6), 27),
    (3, 3, 4): (15, "aab", (9, 6), 66),
    (3, 4, 4): (12, "aab", (6, 6), 42),
    (4, 4, 4): (10, "aaa", (2, 0, 4), 13),
}


def flat_index(indices, dimensions):
    value = 0
    for index, dimension in zip(indices, dimensions):
        value = dimension * value + index
    return value


def permute_axes(matrix, dimensions, permutation):
    """Exact tensor-axis permutation of a raw multiplicity matrix."""
    permuted_dimensions = tuple(dimensions[index] for index in permutation)
    output = sp.zeros(matrix.rows, matrix.cols)
    for indices in product(*(range(dimension) for dimension in dimensions)):
        source = flat_index(indices, dimensions)
        permuted = tuple(indices[index] for index in permutation)
        target = flat_index(permuted, permuted_dimensions)
        output[target, :] = matrix[source, :]
    return output


def restricted_character(shape_triple, permutation):
    physical, _, _ = EXACT_K.hol_k_coordinates(shape_triple)
    dimensions = tuple(
        EXACT_K.HOL_MULTS[index] for index in shape_triple
    )
    moved = permute_axes(physical, dimensions, permutation)
    # Pivot rows give an exact left inverse of the full-column-rank K chart.
    _, pivot_rows = physical.T.rref()
    pivot_rows = list(pivot_rows)
    action = physical[pivot_rows, :].inv() * moved[pivot_rows, :]
    assert physical * action == moved
    character = sp.sympify(sp.trace(action))
    assert character.is_Integer
    return int(character)


def invariant_data(shape_triple):
    physical, _, _ = EXACT_K.hol_k_coordinates(shape_triple)
    dimension = physical.cols
    distinct = len(set(shape_triple))
    if distinct == 3:
        reduced = dimension * (dimension + 1) // 2
        return dimension, "abc", (), reduced
    if distinct == 2:
        positions = next(
            [position for position, value in enumerate(shape_triple)
             if value == repeated]
            for repeated in set(shape_triple)
            if shape_triple.count(repeated) == 2
        )
        permutation = list(range(3))
        permutation[positions[0]], permutation[positions[1]] = (
            permutation[positions[1]], permutation[positions[0]]
        )
        character = restricted_character(shape_triple, tuple(permutation))
        plus = (dimension + character) // 2
        minus = (dimension - character) // 2
        assert plus + minus == dimension
        reduced = plus * (plus + 1) // 2 + minus * (minus + 1) // 2
        return dimension, "aab", (plus, minus), reduced

    transposition_character = restricted_character(shape_triple, (1, 0, 2))
    cycle_character = restricted_character(shape_triple, (1, 2, 0))
    trivial = (
        dimension + 3 * transposition_character + 2 * cycle_character
    ) // 6
    sign = (
        dimension - 3 * transposition_character + 2 * cycle_character
    ) // 6
    standard = (dimension - cycle_character) // 3
    assert trivial + sign + 2 * standard == dimension
    reduced = (
        trivial * (trivial + 1) // 2
        + sign * (sign + 1) // 2
        + standard * (standard + 1) // 2
    )
    return dimension, "aaa", (trivial, sign, standard), reduced


def main():
    triples = tuple(combinations_with_replacement(range(5), 3))
    assert len(triples) == 35
    observed = {triple: invariant_data(triple) for triple in triples}
    assert observed == EXPECTED
    assert sum(value[3] for value in observed.values()) == 761

    # Independent ordered-block count from the same exact K dimensions.
    full_count = 0
    for triple in product(range(5), repeat=3):
        dimension = EXACT_K.hol_k_coordinates(triple)[0].cols
        full_count += dimension * (dimension + 1) // 2
    assert full_count == 4139

    print("ordered target symmetric coordinates:", full_count)
    print("site-symmetric target coordinates:", 761)
    print("key S3 modules: 333=(2 trivial,2 sign,6 standard), "
          "444=(2 trivial,0 sign,4 standard)")
    print("PASS: exact site-symmetric DTH target census")


if __name__ == "__main__":
    main()
