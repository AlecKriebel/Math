"""Regression test for the independent E6 shadow-countermodel audit."""

import unittest

from experiments.four_point_depth_projection.audit_e6_rank6_shadow_countermodel import (
    audit,
)


class E6RankSixShadowAdversarialAuditTest(unittest.TestCase):
    def test_independent_exact_audit(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rank_witness_det_two_gram"], 3)
        self.assertEqual(
            result["common_contact_maxima"],
            {-2: 0, -1: 1, 0: 5, 1: 7},
        )
        self.assertEqual(
            result["contact_clique_link_maxima"],
            [13, 7, 4, 1, 0],
        )
        self.assertEqual(
            result["frame_cases_checked_by_fraction_ldl"],
            38760,
        )


if __name__ == "__main__":
    unittest.main()
