import sys
import unittest


sys.path.insert(0, "src")

import two_active_dormant_407_independent_audit as audit_module


class Dormant407IndependentAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit_module.audit()

    def test_finite_replay_and_graph_regression(self) -> None:
        self.assertEqual(
            self.result["finite_selector_and_951_to_317_map_replay"],
            "PASS",
        )
        graph = self.result["graph_resistance_bounded_attack"]
        self.assertEqual(graph["maximal_complete_digraph_templates"], 188)
        self.assertEqual(graph["hamilton_cycle_orientation_pairs"], 1470)
        self.assertEqual(graph["bounded_counterexamples"], 0)

    def test_uniform_green_counterexample(self) -> None:
        example = self.result["exact_analytic_counterexamples"]
        green = example["lemma_7_1_history"]
        self.assertEqual(green["endpoint"], [2, 1, 0])
        self.assertTrue(
            green["unbounded_historically_consistent_positive_debt_bases"]
        )
        self.assertFalse(green["uniform_green_bound_as_stated"])

    def test_pathwise_service_counterexample(self) -> None:
        service = self.result["exact_analytic_counterexamples"][
            "equation_8_6_history"
        ]
        self.assertTrue(service["first_strict_old_V_service"])
        self.assertEqual(service["change_in_3V_plus_U"], 1)
        self.assertFalse(service["pathwise_promoted_workload_decrease"])

    def test_claim_boundary(self) -> None:
        self.assertEqual(
            self.result["audit_verdict"], "FAIL_AS_WRITTEN_REPAIR_OPEN"
        )
        self.assertFalse(self.result["network_recurrence_counterexample_found"])
        self.assertFalse(self.result["analytic_theorem_independently_audited"])
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
