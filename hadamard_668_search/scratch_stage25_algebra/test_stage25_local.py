#!/usr/bin/env python3
"""Pinned regression checks for the stage-2.5 local algebra audit."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import analyze_stage25_local as local  # noqa: E402


class Stage25LocalAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate0 = local.analyze(0, 10, False)
        cls.candidate2 = local.analyze(2, 10, False)

    def test_candidate0_certificate(self) -> None:
        result = self.candidate0
        self.assertEqual(
            result["semantic_sha256"],
            "967833873b1acf76cc05c89b1cd133cbd8f74c4a24595082c6df6cb03b2b5a92",
        )
        self.assertEqual(
            result["witness"]["delayed_e1_exact_A_Q"], (-9, 0)
        )
        geometry = result["digit2_local_geometry"]
        self.assertEqual(geometry["jacobian_rank"], 18)
        self.assertEqual(geometry["tangent_dimension"], 17)
        self.assertEqual(geometry["common_radical_dimension"], 0)
        digit3 = result["digit3_linearization"]
        self.assertEqual(digit3["restricted_jacobian_rank"], 17)
        self.assertFalse(digit3["all_18_corrections_consistent"])
        self.assertEqual(
            digit3["residual_syndrome_on_gradient_relations"], (1,)
        )
        sheet = digit3["nonzero_residual_correction_sheet"]["search"]
        self.assertEqual(sheet["points"], 729)
        self.assertEqual(sheet["digit2_hits"], 0)
        leave_one_out = digit3["leave_one_out_sheets"]
        self.assertEqual(
            sum(item["consistent"] for item in leave_one_out), 12
        )
        self.assertEqual(
            sum(not item["consistent"] for item in leave_one_out), 6
        )
        extra = result["delayed_e1_digit4_extra"]
        self.assertEqual(extra["value"], 0)
        self.assertEqual(extra["jacobian_rank_with_digit2"], 19)
        self.assertEqual(extra["quadratic_function_span_rank_after"], 19)

    def test_candidate2_comparison(self) -> None:
        result = self.candidate2
        self.assertEqual(
            result["semantic_sha256"],
            "51ec331f54c2a6530222d8418687647eb86695136f2ac9f60e568426127de901",
        )
        self.assertEqual(
            result["witness"]["delayed_e1_exact_A_Q"], (9, 6)
        )
        geometry = result["digit2_local_geometry"]
        self.assertEqual(geometry["jacobian_rank"], 18)
        self.assertEqual(geometry["tangent_dimension"], 17)
        self.assertEqual(geometry["common_radical_dimension"], 0)
        digit3 = result["digit3_linearization"]
        self.assertEqual(digit3["restricted_jacobian_rank"], 17)
        self.assertFalse(digit3["all_18_corrections_consistent"])
        self.assertEqual(
            digit3["residual_syndrome_on_gradient_relations"], (1,)
        )
        sheet = digit3["nonzero_residual_correction_sheet"]["search"]
        self.assertEqual(sheet["points"], 3)
        self.assertEqual(sheet["digit2_hits"], 0)
        leave_one_out = digit3["leave_one_out_sheets"]
        self.assertEqual(
            sum(item["consistent"] for item in leave_one_out), 14
        )
        self.assertEqual(
            sum(not item["consistent"] for item in leave_one_out), 4
        )

    def test_degree3_xl_is_negative(self) -> None:
        for result in (self.candidate0, self.candidate2):
            xl_result = result["degree3_xl_on_delayed_hyperplane"]
            self.assertEqual(xl_result["full_rank"], 666)
            self.assertEqual(xl_result["cubic_projection_rank"], 648)
            self.assertEqual(
                xl_result["quadratic_or_lower_intersection"], 18
            )
            self.assertEqual(xl_result["linear_or_lower_intersection"], 0)
            self.assertEqual(xl_result["constant_only_intersection"], 0)
            self.assertFalse(xl_result["degree3_refutation"])
            self.assertFalse(xl_result["new_linear_consequence"])
            self.assertFalse(xl_result["new_quadratic_consequence"])


if __name__ == "__main__":
    unittest.main()
