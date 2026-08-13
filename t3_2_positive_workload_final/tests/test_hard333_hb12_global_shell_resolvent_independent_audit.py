from __future__ import annotations

import unittest

import hard333_hb12_global_shell_resolvent_independent_audit as audit


class Hard333HB12GlobalShellResolventIndependentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.certificate()

    def test_exact_upstream_snapshot_and_scope(self) -> None:
        self.assertEqual(
            self.result["strict_verdict"],
            "PASS_LOCAL_COMMON_W_STOPPED_BLOCK",
        )
        self.assertEqual(
            self.result["upstream"]["rows_sha256"],
            audit.EXPECTED_UPSTREAM_ROWS_SHA256,
        )
        self.assertEqual(
            self.result["upstream"]["payload_sha256"],
            audit.EXPECTED_UPSTREAM_PAYLOAD_SHA256,
        )
        self.assertTrue(self.result["upstream"]["all_claim_flags_false"])
        self.assertEqual(
            self.result["upstream"]["frozen_files"],
            {
                "note_sha256": audit.EXPECTED_UPSTREAM_NOTE_SHA256,
                "source_sha256": audit.EXPECTED_UPSTREAM_SOURCE_SHA256,
                "test_sha256": audit.EXPECTED_UPSTREAM_TEST_SHA256,
            },
        )

    def test_exact_old_guard_counterexample(self) -> None:
        witness = self.result["old_guard_counterexample"]
        self.assertEqual(witness["exact_top_balance"], "A^2=B*C")
        self.assertIn("contains B=0", witness["conclusion"])

    def test_false_stronger_margin_is_withdrawn(self) -> None:
        witness = self.result["false_stronger_margin_withdrawn"]
        self.assertTrue(witness["A_squared_equals_BC"])
        self.assertEqual(
            witness["tier_blocks"],
            [
                ["2C"],
                ["AC"],
                ["2A", "BC"],
                ["C"],
                ["AB"],
                ["A"],
                ["2B"],
                ["B"],
                ["0"],
            ],
        )
        self.assertIn("tends to zero", witness["same_g_stronger_margin"])
        edits = self.result["post_audit_edits"]
        self.assertEqual(edits["status"], "PASS")
        self.assertIn("shell-independent", edits["common_G_grammar"])
        self.assertIn("separately", edits["outside_core_split"])
        self.assertIn("not assumed", edits["false_margin_explicitly_withdrawn"])

    def test_all_eight_obligations_pass(self) -> None:
        obligations = self.result["obligations"]
        self.assertEqual(len(obligations), 8)
        self.assertEqual([row["id"] for row in obligations], list(range(1, 9)))
        self.assertEqual({row["status"] for row in obligations}, {"PASS"})

    def test_high_cut_and_lower_dimensional_counts(self) -> None:
        self.assertEqual(
            self.result["high_cut_counts"],
            {"unique_high_rows": 14, "tied_high_rows": 2, "total": 16},
        )
        menu = self.result["lower_dimensional_menu"]
        self.assertEqual(
            menu["two_active_48"],
            {"closed_rank_one_top_phase": 36, "promotion_dormant_top": 12},
        )
        self.assertEqual(
            menu["one_active_38"],
            {"direct_physical_C": 2, "generalized_family_ii": 36},
        )

    def test_no_recurrence_or_global_promotion(self) -> None:
        self.assertFalse(self.result["certification_edits_made"])
        self.assertEqual(set(self.result["dependency"].values()), {False})


if __name__ == "__main__":
    unittest.main()
