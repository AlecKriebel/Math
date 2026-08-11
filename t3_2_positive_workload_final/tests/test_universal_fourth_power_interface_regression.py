from fractions import Fraction
import unittest

import universal_fourth_power_interface_regression as regression


class UniversalFourthPowerInterfaceRegressionTest(unittest.TestCase):
    def test_exact_fourth_power_expansion(self) -> None:
        for base in (1, 3, 100):
            for jump in (-3, -1, 0, 2, 5):
                self.assertEqual(
                    regression.fourth_power_increment(base, jump),
                    regression.fourth_power_expansion(base, jump),
                )

    def test_mean_zero_neutral_endpoint_has_positive_curvature(self) -> None:
        for base in (1, 10, 10_000):
            self.assertEqual(
                regression.symmetric_neutral_curvature(base),
                6 * base**2 + 1,
            )

    def test_resistance_at_most_two_is_below_fourth_power_drift(self) -> None:
        for resistance in range(3):
            scaling = regression.repeated_kernel_scaling(resistance)
            self.assertEqual(scaling["negative_endpoint_power"], 3)
            self.assertEqual(scaling["upward_expected_power"], 2)
            self.assertEqual(scaling["duration_is_lower_order"], 1)

    def test_individual_word_resistance_does_not_control_aggregate(self) -> None:
        level = 100
        for resistance in (1, 2):
            aggregate = regression.loop_amplified_up_probability(
                level, resistance
            )
            per_visit = Fraction(1, level ** (resistance + 1))
            self.assertGreater(aggregate, per_visit)
            self.assertEqual(
                aggregate,
                Fraction(1, level**resistance + 1),
            )

    def test_every_strong_one_species_phase_has_negative_leading_edge(self) -> None:
        counts = regression.one_species_strong_phase_counts()
        self.assertEqual(counts["strong_graphs"], 21)
        self.assertEqual(
            counts["negative_leading_graphs"],
            counts["strong_graphs"],
        )

    def test_all_23_moving_cutoff_lift_is_local_only(self) -> None:
        payload = regression.certificate()
        self.assertEqual(payload["analytic_templates"], 23)
        self.assertEqual(
            sum(payload["phase_architecture_incidences"].values()), 3297
        )
        self.assertEqual(
            payload["phase_architecture_incidences"]["whole_top_open_poisson"],
            222,
        )
        self.assertEqual(payload["moving_cutoff_delta"], "1/8")
        self.assertEqual(
            payload["moving_cutoff_expected_cost_power"], "23/8"
        )
        self.assertEqual(
            payload["family_ii_cap_semantics"],
            "normalized cap 2 means arbitrary fixed class invariant >=2",
        )
        self.assertTrue(payload["boundary_ties_use_endpoint_weighted_charge"])
        self.assertEqual(payload["m2_unweighted_third_interruption_power"], -3)
        self.assertTrue(payload["direct_phase_nested_exponential_green"])
        self.assertFalse(payload["deterministic_up_overshoot_bound_required"])
        self.assertEqual(
            payload["nonboundary_endpoint_moment_order_strictly_above"], 8
        )
        self.assertTrue(payload["one_dimensional_no_fast_phase_certified"])
        self.assertTrue(
            payload[
                "graph_resistance_to_aggregate_kernel_analytic_lift_certified"
            ]
        )
        self.assertTrue(
            payload["all_23_moving_cutoff_promotion_access_certified"]
        )

    def test_pair_composition_is_certified_but_global_flag_remains_false(self) -> None:
        payload = regression.certificate()
        self.assertTrue(payload["arbitrary_orientation_graph_lemma_certified"])
        self.assertTrue(payload["candidate_1227_recurrence_certified"])
        self.assertFalse(payload["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
