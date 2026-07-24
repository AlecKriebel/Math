"""Regression tests for the adjacent-42 Eliahou repair theorem."""

from __future__ import annotations

import unittest

from verify_eliahou_adjacent42_repair import (
    EXPECTED_BASE_RESIDUALS,
    EXPECTED_TRANSFER_COEFFICIENT_80,
    base_correlations,
    eliahou_base,
    equal_separation_pairs,
    expected_seed_fold,
    fold42,
    fold_correlations_from_aperiodic,
    fold_quadruple,
    joined_root_profiles,
    local_component_polynomial,
    q_pair_signature_catalogs,
    reciprocal_q_masks_of_weight_at_most_two,
    special_change_case_split,
    summed_periodic_correlations,
    transfer_polynomial,
    verify_center_q_flip_obstruction,
)


class EliahouAdjacent42Tests(unittest.TestCase):
    def test_seed_residuals_collapse_to_a_flat_energy14_fold(self) -> None:
        base = eliahou_base()
        correlations = base_correlations(base)
        self.assertEqual(
            {
                lag: value
                for lag, value in enumerate(correlations)
                if lag and value
            },
            EXPECTED_BASE_RESIDUALS,
        )
        self.assertEqual(fold_quadruple(base), expected_seed_fold())
        self.assertEqual(
            summed_periodic_correlations(fold_quadruple(base)),
            (14,) + (0,) * 41,
        )
        self.assertEqual(
            fold_correlations_from_aperiodic(correlations),
            summed_periodic_correlations(fold_quadruple(base)),
        )

    def test_exact_target_needs_eighty_new_equal_pairs(self) -> None:
        base = eliahou_base()
        self.assertEqual(equal_separation_pairs(base), 3)
        self.assertEqual((334 - 2) // 4, 83)
        self.assertEqual(83 - equal_separation_pairs(base), 80)
        self.assertEqual(
            [
                sum(value * value for value in fold42(sequence))
                for sequence in base
            ],
            [4, 0, 5, 5],
        )

    def test_reciprocal_skeleton_transfer_polynomial(self) -> None:
        self.assertEqual(
            local_component_polynomial((True, True, True, True)),
            {0: 1, 2: 12, 4: 8},
        )
        self.assertEqual(
            local_component_polynomial((True, False, True, True)),
            {0: 1, 2: 6},
        )
        self.assertEqual(
            local_component_polynomial((False, True, True, False)),
            {0: 1, 2: 2},
        )
        self.assertEqual(
            transfer_polynomial()[80], EXPECTED_TRANSFER_COEFFICIENT_80
        )

    def test_complete_distance41_case_split(self) -> None:
        self.assertEqual(special_change_case_split(40), ((40, 0, 0),))
        self.assertEqual(
            special_change_case_split(41),
            ((39, 2, 0), (40, 1, 0), (41, 0, 0)),
        )
        masks = reciprocal_q_masks_of_weight_at_most_two()
        self.assertEqual(
            {weight: len(values) for weight, values in masks.items()},
            {0: 1, 1: 1, 2: 83},
        )
        self.assertEqual(masks[1], ((125,),))
        verify_center_q_flip_obstruction()

    def test_root_plus_minus_one_reduce_weight2_q_pairs_to_39(self) -> None:
        long_catalog, short_catalog = q_pair_signature_catalogs()
        surviving_long = {
            signature: indices
            for signature, indices in long_catalog.items()
            if joined_root_profiles(*signature, True)
        }
        surviving_short = {
            signature: indices
            for signature, indices in short_catalog.items()
            if joined_root_profiles(*signature, False)
        }
        self.assertEqual(sum(map(len, long_catalog.values())), 42)
        self.assertEqual(sum(map(len, short_catalog.values())), 38)
        self.assertEqual(sum(map(len, surviving_long.values())), 21)
        self.assertEqual(sum(map(len, surviving_short.values())), 18)
        self.assertEqual(
            {
                signature: len(joined_root_profiles(*signature, True))
                for signature in surviving_long
            },
            {(-2, 0): 2, (0, 2): 2},
        )
        self.assertEqual(
            {
                signature: len(joined_root_profiles(*signature, False))
                for signature in surviving_short
            },
            {(0, 0): 2},
        )


if __name__ == "__main__":
    unittest.main()
