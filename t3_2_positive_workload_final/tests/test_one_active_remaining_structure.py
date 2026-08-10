from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import one_active_remaining_structure as structure


class OneActiveRemainingStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = structure.certificate()

    def test_exact_scope_and_claim_boundary(self) -> None:
        self.assertEqual(self.result["candidate_pairs"], 1227)
        self.assertEqual(self.result["candidate_incidences"], 3297)
        self.assertFalse(self.result["analytic_one_active_theorem_certified"])
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])

    def test_affine_feasibility_excludes_active_invariant(self) -> None:
        self.assertEqual(
            self.result["full_active_coefficient_invariant_incidences"], 0
        )

    def test_exact_phase_and_access_partition(self) -> None:
        self.assertEqual(
            self.result["phase_histogram"],
            {
                "lower_only+mixed_killed": 1784,
                "mixed_killed+lower_only": 246,
                "mixed_killed+mixed_killed": 1045,
                "whole_top+mixed_killed": 222,
            },
        )
        self.assertEqual(
            self.result["initial_access_histogram"],
            {
                "frozen_face": 123,
                "mixed_direct_enabled": 2471,
                "nonzero_lower_seed": 20,
                "whole_open_countable": 222,
                "zero_source_seed": 461,
            },
        )

    def test_canonical_depth_partition_and_critical_family(self) -> None:
        self.assertEqual(
            self.result["canonical_depth_histogram"],
            {
                "mixed_zero_and_nested_service": 32,
                "nested_slow_before_fast_service": 131,
                "no_positive_debt_base": 2228,
                "zero_contest_from_every_debt_base": 906,
            },
        )
        self.assertEqual(
            self.result["canonical_depth_order_histogram"],
            {
                "creation_strictly_deeper": 994,
                "no_positive_debt_base": 2228,
                "some_equal_none_shallower": 75,
            },
        )
        self.assertEqual(self.result["canonical_analytic_templates"], 23)
        self.assertEqual(self.result["critical_equal_depth_incidences"], 75)
        self.assertEqual(self.result["critical_equal_depth"]["pairs"], 15)
        self.assertEqual(
            len(self.result["critical_equal_depth_pair_payload"]), 15
        )
        self.assertEqual(
            len(self.result["critical_normalized_support_templates"]), 9
        )
        self.assertEqual(
            self.result["critical_pair_failure_count_histogram"],
            {5: 8, 6: 6, 7: 1},
        )
        self.assertEqual(
            self.result["critical_pair_noncritical_incidences"], 8
        )
        self.assertEqual(
            len(self.result["critical_pair_noncritical_payload"]), 8
        )
        self.assertEqual(
            self.result["critical_pair_noncritical_class_histogram"],
            {
                (
                    "mixed_direct_enabled|no_positive_debt_base|"
                    "no_positive_debt_base"
                ): 6,
                (
                    "zero_source_seed|zero_contest_from_every_debt_base|"
                    "creation_strictly_deeper"
                ): 2,
            },
        )
        self.assertEqual(
            self.result["critical_shell_structure"],
            {
                "mixed_linkage": ["0", "AC", "BC"],
                "mixed_linkage_invariant": "Q=C-A-B",
                "lower_source_total_degrees": [1, 2],
                "normalized_support_templates": 9,
                "averaged_q_drift_formula": (
                    "-a_minus*Z[N+1]/Z[N]"
                    "+a_plus*Z[N+2]/Z[N], with a_minus>0"
                ),
            },
        )
        self.assertEqual(
            self.result["critical_pair_active_coordinate_count_histogram"],
            {1: 15},
        )
        self.assertEqual(
            self.result["critical_pair_mixed_shell_count_histogram"],
            {1: 15},
        )
        self.assertTrue(
            all(
                row["active_species"] == ["C"]
                and row["critical_incidences"] == 5
                and row["mixed_shell_linkages"] == [["0", "AC", "BC"]]
                for row in self.result["critical_pair_axis_payload"]
            )
        )
        self.assertEqual(
            self.result["critical_equal_depth"]["pair_sha256"],
            "6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3",
        )
        self.assertEqual(
            self.result["critical_equal_depth_word_histogram"],
            {"debt=1,creation=2,service=2": 75},
        )

    def test_payload_hash_is_frozen(self) -> None:
        self.assertEqual(
            self.result["payload_sha256"], structure.EXPECTED_PAYLOAD_SHA256
        )


if __name__ == "__main__":
    unittest.main()
