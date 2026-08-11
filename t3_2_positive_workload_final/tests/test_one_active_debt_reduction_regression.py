import unittest

import one_active_debt_reduction_regression as regression
import one_active_phase_shape as phase_shape


class OneActiveDebtReductionRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = regression.certificate()

    def test_scope_is_claim_neutral(self):
        self.assertFalse(
            self.payload["arbitrary_strong_orientation_certified"]
        )
        self.assertFalse(self.payload["analytic_recurrence_certified"])
        self.assertFalse(self.payload["global_t3_2_certified"])

    def test_relative_old_debt_semantics(self):
        self.assertIn(
            "first r<0",
            self.payload["service_semantics"],
        )
        self.assertIn(
            "from the same base",
            self.payload["arrival_semantics"],
        )

    def test_absolute_creation_boundary_is_killed_not_clamped(self):
        self.assertIsNone(
            regression.bounded_reflected_debt(8, 1, debt_bound=8)
        )
        self.assertEqual(
            regression.bounded_reflected_debt(8, -1, debt_bound=8), 7
        )
        self.assertEqual(
            regression.bounded_reflected_debt(0, -1, debt_bound=8), 0
        )

    def test_future_arrivals_are_strictly_deeper(self):
        for family in self.payload["orientation_families"].values():
            self.assertEqual(
                family["future_arrival_not_strictly_deeper"], []
            )
            self.assertEqual(family["missing_strict_reduction"], [])
            self.assertEqual(
                len(family["reduction_depth_two_payload"]), 16
            )
            self.assertTrue(
                all(
                    int(key.rsplit(",", 1)[1]) <= 2
                    for key in family[
                        "future_upward_reduction_histogram"
                    ]
                )
            )
            self.assertEqual(
                {
                    tuple(tuple(support) for support in row["normalized_supports"])
                    for row in family["reduction_depth_two_payload"]
                },
                {
                    (("0", "AC"), ("2A", "2B", "AB", "BC")),
                    (("0", "AC"), ("B", "2A", "AB", "BC")),
                    (("0", "AC"), ("B", "2A", "2B", "BC")),
                    (("0", "AC"), ("B", "2A", "2B", "AB", "BC")),
                },
            )

    def test_relative_boundary_sensitivity(self):
        for family in self.payload[
            "relative_boundary_sensitivity"
        ].values():
            self.assertGreater(family["rows_checked"], 0)
            self.assertEqual(family["bound_6_vs_10_mismatches"], [])

    def test_maximal_orientations_are_allowed_and_strong(self):
        self.assertTrue(
            all(
                regression.orientation_is_allowed_and_strong(
                    pair,
                    descriptor,
                    regression.maximal_orientation(pair, descriptor),
                )
                for pair, descriptor in phase_shape.candidate_incidences()
            )
        )


if __name__ == "__main__":
    unittest.main()
