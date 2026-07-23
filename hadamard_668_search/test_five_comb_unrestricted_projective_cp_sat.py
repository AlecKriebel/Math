#!/usr/bin/env python3
"""Independent checks for the unrestricted projective packing model."""

from __future__ import annotations

from itertools import product
import unittest

from check_five_comb_mub_reductions import (
    HOLE_POSITIONS,
    PROJECTIVE_RREF,
    PROJECTIVE_SLOT_STATES,
    QUARTETS,
    SHIFTS,
    TARGET,
    VECTORS,
)
from search_five_comb_unrestricted_projective_cp_sat import (
    LAGS,
    normalized_projective_labels,
    projective_inner_product,
    projective_row_orbit_is_canonical,
    reconstruct,
    scalar_carrier,
    scalar_cross_vector,
    scalar_hole_vector,
)


def full_carrier(
    quartet_index: int,
    labels: tuple[int, ...],
    slot: int,
    carrier_type: int,
) -> tuple[dict[int, int], ...]:
    scalar = scalar_carrier(QUARTETS[quartet_index], slot, carrier_type)
    return tuple(
        {
            position: VECTORS[labels[slot]][row] * sign
            for position, sign in scalar.items()
        }
        for row in range(4)
    )


def direct_cross_vector(
    left: tuple[dict[int, int], ...],
    right: tuple[dict[int, int], ...],
) -> tuple[int, ...]:
    result = [0] * (LAGS + 1)
    for left_row, right_row in zip(left, right, strict=True):
        for left_position, left_sign in left_row.items():
            for right_position, right_sign in right_row.items():
                lag = abs(right_position - left_position)
                if lag:
                    result[lag] += left_sign * right_sign
    return tuple(result)


def direct_correlations(
    sequences: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    return tuple(
        sum(
            sequence[position] * sequence[position + lag]
            for sequence in sequences
            for position in range(len(sequence) - lag)
        )
        for lag in range(1, LAGS + 1)
    )


class UnrestrictedProjectivePackingTests(unittest.TestCase):
    def test_sparse_parametrization_is_exact(self) -> None:
        labelings = {
            normalized_projective_labels(parameters)
            for parameters in product((0, 1), repeat=12)
        }
        self.assertEqual(len(labelings), 4096)
        self.assertEqual(len(PROJECTIVE_RREF), 9)
        self.assertEqual(
            sum(
                projective_row_orbit_is_canonical(labeling)
                for labeling in labelings
            ),
            1440,
        )
        for labeling in labelings:
            self.assertEqual(labeling[0], 0)
            syndrome = TARGET
            for slot, label in enumerate(labeling):
                syndrome ^= PROJECTIVE_SLOT_STATES[slot][label]
            self.assertEqual(syndrome, 0)

    def test_projective_scalar_factorization(self) -> None:
        labelings = (
            normalized_projective_labels((0,) * 12),
            normalized_projective_labels(
                (1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0)
            ),
            (0, 4, 5, 1, 2, 6, 7, 3),
        )
        fixtures = (
            (0, 0, 1, 0, 3),
            (17, 2, 7, 4, 5),
            (39, 1, 6, 2, 4),
            (47, 3, 5, 6, 7),
        )
        for labels in labelings:
            for quartet_index, left, right, left_type, right_type in fixtures:
                scalar = scalar_cross_vector(
                    scalar_carrier(QUARTETS[quartet_index], left, left_type),
                    scalar_carrier(QUARTETS[quartet_index], right, right_type),
                )
                factored = tuple(
                    projective_inner_product(labels[left], labels[right])
                    * value
                    for value in scalar
                )
                direct = direct_cross_vector(
                    full_carrier(
                        quartet_index, labels, left, left_type
                    ),
                    full_carrier(
                        quartet_index, labels, right, right_type
                    ),
                )
                self.assertEqual(factored, direct)

                hole = HOLE_POSITIONS[(left + right) % len(HOLE_POSITIONS)]
                hole_row, hole_position = hole
                scalar_hole = scalar_hole_vector(
                    scalar_carrier(
                        QUARTETS[quartet_index], left, left_type
                    ),
                    hole_position,
                )
                direct_hole = [0] * (LAGS + 1)
                for position, sign in full_carrier(
                    quartet_index, labels, left, left_type
                )[hole_row].items():
                    lag = abs(hole_position - position)
                    if lag:
                        direct_hole[lag] += sign
                self.assertEqual(
                    tuple(direct_hole),
                    tuple(
                        VECTORS[labels[left]][hole_row] * value
                        for value in scalar_hole
                    ),
                )

    def test_row_pair_actions_are_true_construction_symmetries(self) -> None:
        quartet_index = 39
        labels = normalized_projective_labels(
            (1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0)
        )
        types = (7, 2, 5, 0, 3, 6, 1, 4)
        orientations = (0, 1, 1, 0, 1, 0, 0, 1)
        holes = tuple((index // 2) % 2 for index in range(len(HOLE_POSITIONS)))
        original = reconstruct(
            quartet_index, labels, types, orientations, holes
        )
        hole_lookup = {
            position: holes[index]
            for index, position in enumerate(HOLE_POSITIONS)
        }

        def permuted_holes(permutation: tuple[int, ...]) -> tuple[int, ...]:
            return tuple(
                hole_lookup[(permutation[row], position)]
                for row, position in HOLE_POSITIONS
            )

        long_labels = tuple(
            (label & 1)
            + 2 * (((label >> 1) & 1) ^ (label & 1))
            + 4 * ((label >> 2) & 1)
            for label in labels
        )
        long_orientations = tuple(
            orientation ^ (label & 1)
            for orientation, label in zip(
                orientations, labels, strict=True
            )
        )
        swapped_long = reconstruct(
            quartet_index,
            long_labels,
            types,
            long_orientations,
            permuted_holes((1, 0, 2, 3)),
        )
        self.assertEqual(
            swapped_long,
            (original[1], original[0], original[2], original[3]),
        )

        short_labels = tuple(
            (label & 1)
            + 2
            * (
                ((label >> 1) & 1)
                ^ (label & 1)
                ^ ((label >> 2) & 1)
            )
            + 4 * ((label >> 2) & 1)
            for label in labels
        )
        swapped_short = reconstruct(
            quartet_index,
            short_labels,
            types,
            orientations,
            permuted_holes((0, 1, 3, 2)),
        )
        self.assertEqual(
            swapped_short,
            (original[0], original[1], original[3], original[2]),
        )

        alternated_orientations = tuple(
            orientation ^ (SHIFTS[slot] & 1)
            for slot, orientation in enumerate(orientations)
        )
        alternated_holes = tuple(
            hole ^ (position & 1)
            for hole, (_row, position) in zip(
                holes, HOLE_POSITIONS, strict=True
            )
        )
        alternated = reconstruct(
            quartet_index,
            labels,
            types,
            alternated_orientations,
            alternated_holes,
        )
        self.assertEqual(
            alternated,
            tuple(
                tuple(
                    value * (-1 if position & 1 else 1)
                    for position, value in enumerate(sequence)
                )
                for sequence in original
            ),
        )

    def test_complete_decomposition_matches_raw_correlations(self) -> None:
        fixtures = (
            (
                0,
                normalized_projective_labels((0,) * 12),
                tuple(range(8)),
                (0, 1, 0, 1, 1, 0, 1, 0),
                tuple(index % 2 for index in range(len(HOLE_POSITIONS))),
            ),
            (
                39,
                (0, 4, 5, 1, 2, 6, 7, 3),
                (5, 0, 4, 1, 7, 2, 6, 3),
                (0, 0, 1, 1, 0, 1, 0, 1),
                tuple((3 * index + 1) % 2 for index in range(len(HOLE_POSITIONS))),
            ),
            (
                47,
                normalized_projective_labels(
                    (1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0)
                ),
                (7, 2, 5, 0, 3, 6, 1, 4),
                (0, 1, 1, 0, 1, 0, 0, 1),
                tuple((index // 2) % 2 for index in range(len(HOLE_POSITIONS))),
            ),
        )
        for quartet_index, labels, types, orientations, holes in fixtures:
            sequences = reconstruct(
                quartet_index, labels, types, orientations, holes
            )
            modeled = [0] * (LAGS + 1)
            carriers = tuple(
                scalar_carrier(QUARTETS[quartet_index], slot, types[slot])
                for slot in range(8)
            )

            for left in range(8):
                for right in range(left + 1, 8):
                    multiplier = (
                        (-1 if orientations[left] else 1)
                        * (-1 if orientations[right] else 1)
                        * projective_inner_product(
                            labels[left], labels[right]
                        )
                    )
                    vector = scalar_cross_vector(
                        carriers[left], carriers[right]
                    )
                    for lag in range(1, LAGS + 1):
                        modeled[lag] += multiplier * vector[lag]

            for slot in range(8):
                for hole_index, (hole_row, hole_position) in enumerate(
                    HOLE_POSITIONS
                ):
                    multiplier = (
                        (-1 if orientations[slot] else 1)
                        * (-1 if holes[hole_index] else 1)
                        * VECTORS[labels[slot]][hole_row]
                    )
                    vector = scalar_hole_vector(
                        carriers[slot], hole_position
                    )
                    for lag in range(1, LAGS + 1):
                        modeled[lag] += multiplier * vector[lag]

            for left, (left_row, left_position) in enumerate(HOLE_POSITIONS):
                for right in range(left + 1, len(HOLE_POSITIONS)):
                    right_row, right_position = HOLE_POSITIONS[right]
                    if left_row != right_row:
                        continue
                    lag = abs(right_position - left_position)
                    modeled[lag] += (
                        (-1 if holes[left] else 1)
                        * (-1 if holes[right] else 1)
                    )

            self.assertEqual(tuple(modeled[1:]), direct_correlations(sequences))


if __name__ == "__main__":
    unittest.main()
