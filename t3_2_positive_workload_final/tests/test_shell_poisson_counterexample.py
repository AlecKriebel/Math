import unittest
from decimal import Decimal, localcontext

import shell_poisson_counterexample as counterexample


class ShellPoissonCounterexampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = counterexample.certificate()
        cls.finite = cls.result["finite_counterexample"]

    def test_finite_shell_and_state(self):
        self.assertEqual(self.finite["n"], 4)
        self.assertEqual(self.finite["stationary_center"], [64, 4, 1024])
        self.assertEqual(self.finite["invariant"], [72, 2112])
        self.assertEqual(self.finite["evaluation_state"], [4, 34, 1054])
        self.assertEqual(self.finite["base_fiber_size"], 37)

    def test_mean_zero_corrector_reverses_the_averaged_sign(self):
        average = Decimal(self.finite["stationary_average_g"])
        corrector = Decimal(self.finite["lower_corrector_drift"])
        corrected = Decimal(self.finite["corrected_drift"])
        self.assertLess(average, Decimal("-455"))
        self.assertGreater(corrector, Decimal("472"))
        self.assertGreater(corrected, Decimal("16"))
        with localcontext() as context:
            context.prec = 80
            self.assertLess(
                abs(corrected - average - corrector),
                Decimal("1e-59"),
            )

    def test_top_propensity_dominates(self):
        self.assertEqual(self.finite["top_propensity"], 35848)
        self.assertEqual(self.finite["lower_propensity"], 1263)
        self.assertGreater(
            Decimal(self.finite["top_to_lower_propensity_ratio"]),
            Decimal(28),
        )

    def test_conductance_solution_residual(self):
        self.assertLess(
            Decimal(self.finite["maximum_poisson_residual"]),
            Decimal("1e-75"),
        )

    def test_dominant_lower_corrector_term(self):
        contributions = {
            row["edge"]: row for row in self.finite["reaction_contributions"]
        }
        self.assertEqual(contributions["2B->0"]["source_propensity"], 1122)
        self.assertGreater(
            Decimal(contributions["2B->0"]["drift_contribution"]),
            Decimal(446),
        )

    def test_asymptotic_fields_are_claim_neutral(self):
        asymptotic = self.result["asymptotic_family"]
        self.assertEqual(
            asymptotic["corrected_drift"],
            "(1/4+o(1)) N^4 log N",
        )
        self.assertIn("no recurrence or nonrecurrence", self.result["claim_scope"])
        self.assertEqual(
            self.result["certificate_sha256"],
            counterexample.EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
