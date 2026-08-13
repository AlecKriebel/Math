import sys
import unittest


sys.path.insert(0, "src")

import two_active_dormant_407_asymmetric_return_audit as audit


class Dormant407AsymmetricReturnAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.audit()

    def test_frozen_snapshot_and_flags(self) -> None:
        self.assertEqual(
            self.result["audited_snapshot_sha256"], audit.FROZEN_HASHES
        )
        self.assertEqual(
            self.result["certification_flags"],
            {
                "analytic_theorem_independently_audited": False,
                "pair_level_recurrence_certified": False,
                "global_t3_2_certified": False,
            },
        )

    def test_exact_template_and_orientations(self) -> None:
        self.assertEqual(
            self.result["exact_template"],
            {
                "proper": ["2U", "VI"],
                "lower": ["0", "I", "2I", "UI"],
            },
        )
        self.assertEqual(self.result["physical_rows"], 6)
        self.assertEqual(
            self.result["spectator_cap_histogram"],
            {"0": 2, "1": 2, "2": 2},
        )

    def test_historically_reachable_growth_word(self) -> None:
        states = self.result["growth_word_states_U_I_R_J"]
        self.assertEqual(states[0], [2, 0, 0, 0])
        self.assertEqual(states[-1], [3, 0, 0, 3])
        self.assertLessEqual(max(state[1] for state in states), 2)
        self.assertLessEqual(max(state[2] for state in states), 1)

    def test_paid_exact_return_only_increments_j(self) -> None:
        states = self.result["paid_exact_return_states_U_I_R_J"]
        self.assertEqual(states[0], [10, 0, 0, 7])
        self.assertEqual(states[-1], [10, 0, 0, 8])
        self.assertEqual(
            self.result["mark_ratio_on_exact_return"],
            "Psi(endpoint)/Psi(start)=z1>1",
        )

    def test_contracted_cycle_probability_tends_to_one(self) -> None:
        values = [
            row["probability"]
            for row in self.result["contracted_cycle_probability"]
        ]
        self.assertEqual(values, sorted(values))
        self.assertGreater(values[-1], 0.999)

    def test_strict_claim_negative_verdict(self) -> None:
        self.assertEqual(self.result["verdict"], "FAIL-as-written")
        self.assertEqual(
            self.result["scope"],
            "proof failure, not a recurrence or T3-2 counterexample",
        )
        self.assertIn(
            "second killed base resolvent",
            self.result["repair_case_split"]["required_missing_argument"],
        )


if __name__ == "__main__":
    unittest.main()
