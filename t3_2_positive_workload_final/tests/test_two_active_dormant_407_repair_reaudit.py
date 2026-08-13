import sys
import unittest


sys.path.insert(0, "src")

import two_active_dormant_407_repair_reaudit as reaudit_module


class Dormant407RepairReauditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = reaudit_module.reaudit()

    def test_exact_template_and_strong_orientation(self) -> None:
        example = self.result["actual_service_endpoint_counterexample"]
        support = example["normalized_support"]
        self.assertEqual(support["proper"], ["2U", "VI"])
        self.assertEqual(support["lower"], ["0", "I", "2I", "UI"])
        self.assertEqual(support["exact_generalized_rows"], 6)
        self.assertEqual(
            support["spectator_cap_histogram"], {"0": 2, "1": 2, "2": 2}
        )

    def test_historical_debt_and_actual_service_endpoint(self) -> None:
        example = self.result["actual_service_endpoint_counterexample"]
        self.assertEqual(
            example["historical_positive_debt_word"]["endpoint"], [10, 0, 1]
        )
        service = example["zero_order_actual_service_endpoint"]
        self.assertEqual(service["endpoint"], [12, 0, -1])
        self.assertEqual(service["spectator_change"], 2)
        self.assertEqual(service["old_V_change"], -1)

    def test_bounded_corrector_claim_fails(self) -> None:
        drift = self.result["actual_service_endpoint_counterexample"][
            "B_ell_drift"
        ]
        self.assertTrue(drift["positive_for_every_fixed_ell_U_eventually"])
        self.assertFalse(drift["d_plus_has_finite_support"])
        self.assertFalse(drift["chi_is_uniformly_bounded"])
        self.assertEqual(self.result["bounded_B_ell_plus_chi"], "FAIL")

    def test_claim_boundary(self) -> None:
        self.assertEqual(
            self.result["descriptor_local_reaudit_verdict"],
            "FAIL_AS_WRITTEN_REPAIR_OPEN",
        )
        self.assertFalse(self.result["network_recurrence_counterexample_found"])
        self.assertFalse(self.result["analytic_theorem_independently_audited"])
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
