from __future__ import annotations

import unittest

import hard_exact_pair_macroscopic_entropy_independent_audit as audit


class HardExactPairMacroscopicEntropyIndependentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.certificate()

    def test_frozen_target_and_verdict(self) -> None:
        self.assertEqual(
            self.result["strict_verdict"], "PASS_LOCAL_ANALYTIC_THEOREM"
        )
        self.assertEqual(
            self.result["frozen_files"],
            {
                "theorem_sha256": audit.EXPECTED_THEOREM_SHA256,
                "certificate_source_sha256": (
                    audit.EXPECTED_CERTIFICATE_SOURCE_SHA256
                ),
                "certificate_test_sha256": audit.EXPECTED_CERTIFICATE_TEST_SHA256,
                "prior_hostile_audit_sha256": (
                    audit.EXPECTED_PRIOR_HOSTILE_AUDIT_SHA256
                ),
            },
        )

    def test_old_pathwise_counterexample_is_retained(self) -> None:
        witness = self.result["prior_pathwise_counterexample"]
        self.assertTrue(witness["total_increment_positive"])
        self.assertGreater(witness["exact_total_entropy_increment"], 0)
        self.assertIn("no pathwise negative sign", witness["lesson"])

    def test_killed_overshoot_repair(self) -> None:
        repair = self.result["repair"]
        self.assertFalse(repair["pathwise_shell_sign_used"])
        self.assertTrue(repair["killed_positive_overshoot_used"])
        self.assertEqual(
            repair["strong_connectivity_rate_conditions"],
            ["B+R0>0", "D+R1>0", "R0+R1>0"],
        )

    def test_exact_finite_scope(self) -> None:
        replay = self.result["finite_replay"]
        self.assertEqual(replay["physical_normalized_templates"], 188)
        self.assertEqual(replay["exact_templates"], 19)
        self.assertEqual(replay["rows_sha256"], audit.EXPECTED_ROWS_SHA256)
        self.assertGreaterEqual(replay["minimum_carrier_gap_q_minus_pa"], 1)
        self.assertGreaterEqual(
            replay["minimum_interruption_gap_q_minus_pcmax"], 1
        )
        self.assertEqual(
            replay["unique_nonsingleton_maximizer"]["maximizers"],
            ["0", "UI"],
        )

    def test_all_analytic_obligations_pass(self) -> None:
        obligations = self.result["obligations"]
        self.assertEqual(len(obligations), 7)
        self.assertEqual([row["id"] for row in obligations], list(range(1, 8)))
        self.assertEqual({row["status"] for row in obligations}, {"PASS"})

    def test_claim_boundary_and_frozen_payload(self) -> None:
        self.assertFalse(self.result["certification_edits_made"])
        self.assertEqual(set(self.result["upstream_claim_flags"].values()), {False})
        self.assertEqual(set(self.result["dependency"].values()), {False})
        self.assertEqual(
            self.result["audit_payload_sha256"],
            audit.EXPECTED_AUDIT_PAYLOAD_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
