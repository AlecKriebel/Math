"""Regression tests for the coupled order-three LP(333) row-sum theorem."""

from __future__ import annotations

from collections import Counter
import unittest

from verify_lp333_twisted_order3 import (
    FIXED_MARGIN_CATALOG_SHA256,
    GENERIC_CATALOG_SHA256,
    abc_completions,
    abc_target,
    binary_axis_options,
    binary_orbit_row_signatures,
    binary_rows,
    catalog_digest,
    check_crt_actions_and_orientation_reversal,
    count_row_symmetry_orbits,
    fixed_margin_row_sum_catalog,
    generic_row_sum_catalog,
    qpsk_row_sums,
    reachable_binary_row_sums,
    realizable_twisted_pairs,
    six_axis_states_by_row,
    six_weight_three_axis_states,
    survives_pure_row_axis,
    unrestricted_twisted_pairs,
    zero_column_compatible,
    zero_column_fixed_triples,
)


class TwistedOrderThreeTests(unittest.TestCase):
    def test_crt_actions_and_partial_orientation_bijection(self) -> None:
        check_crt_actions_and_orientation_reversal()

    def test_positive_definite_pair_and_completion_census(self) -> None:
        self.assertEqual(len(qpsk_row_sums()), 1444)
        self.assertEqual(len(unrestricted_twisted_pairs()), 36)
        self.assertEqual(len(realizable_twisted_pairs()), 12)
        self.assertEqual(
            Counter(
                len(abc_completions(*abc_target(d_value, e_value)))
                for d_value, e_value in realizable_twisted_pairs()
            ),
            Counter({504: 12}),
        )

    def test_catalog_and_fixed_margin_lift(self) -> None:
        generic = generic_row_sum_catalog()
        filtered = fixed_margin_row_sum_catalog()
        self.assertEqual(len(generic), 6048)
        self.assertEqual(catalog_digest(generic), GENERIC_CATALOG_SHA256)
        self.assertEqual(len(zero_column_fixed_triples()), 9)
        self.assertEqual(len(filtered), 1296)
        self.assertEqual(catalog_digest(filtered), FIXED_MARGIN_CATALOG_SHA256)

        self.assertEqual(len(binary_orbit_row_signatures(3)), 20)
        self.assertEqual(len(binary_orbit_row_signatures(6)), 20)
        reachable = reachable_binary_row_sums()
        self.assertEqual(len(reachable), 186576)
        for word in generic:
            exact_margin_lift = (
                binary_rows(word, 0) in reachable
                and binary_rows(word, 1) in reachable
            )
            self.assertEqual(exact_margin_lift, zero_column_compatible(word))

    def test_exact_row_sum_symmetry_orbits(self) -> None:
        self.assertEqual(
            count_row_symmetry_orbits(False), (216, Counter({6: 216}))
        )
        self.assertEqual(
            count_row_symmetry_orbits(True), (108, Counter({12: 108}))
        )

    def test_pure_row_axis_is_feasible_for_every_catalog_word(self) -> None:
        catalog = fixed_margin_row_sum_catalog()
        self.assertEqual(len(six_weight_three_axis_states()), 21953)
        self.assertEqual(len(six_axis_states_by_row()), 3430)
        targets = {
            binary_rows(word, sequence_index)
            for word in catalog
            for sequence_index in (0, 1)
        }
        self.assertEqual(len(targets), 147)
        self.assertTrue(all(binary_axis_options(target) for target in targets))
        self.assertTrue(all(survives_pure_row_axis(word) for word in catalog))


if __name__ == "__main__":
    unittest.main()
