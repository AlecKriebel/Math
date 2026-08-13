from __future__ import annotations

from collections import Counter
import unittest

import rank_two_mixed_profile_7_stopped_service as candidate


class RankTwoMixedProfile7StoppedServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_exact_selector_and_dormant_vertices(self) -> None:
        self.assertEqual(self.result["selector"]["pairs"], 7)
        self.assertEqual(
            self.result["selector"]["pair_sha256"],
            candidate.EXPECTED_PAIR_SHA256,
        )
        self.assertEqual(self.result["selector"]["nonservice_dormant_vertices"], 8)
        self.assertEqual(
            Counter(row["vertex"] for row in candidate.dormant_vertex_rows()),
            {"A": 4, "B": 4},
        )

    def test_service_zero_boundary_geometry(self) -> None:
        rows = candidate.pair_rows()
        self.assertTrue(all(row["lower_support"] == ["0", "C"] for row in rows))
        self.assertTrue(all(row["service_zero_face_contains_AB"] for row in rows))
        self.assertTrue(all(row["top_stoichiometric_rank"] == 2 for row in rows))
        self.assertEqual(
            Counter(",".join(row["service_zero_sources"]) for row in rows),
            {"2A,AB": 3, "2B,AB": 3, "AB": 1},
        )

    def test_local_pf_contract_is_frozen(self) -> None:
        self.assertTrue(
            all(
                row["local_pf_inequality"]
                == "L_top R >= c*X*R-K*R^2"
                for row in candidate.dormant_vertex_rows()
            )
        )
        self.assertEqual(
            self.result["all_reactions_retained_stopping_contract"][
                "required_audit_moment"
            ],
            "choose m>8",
        )
        stopping = self.result["all_reactions_retained_stopping_contract"]
        self.assertIn("O(log(N)/N)", stopping["pf_survival_and_trial_time"])
        self.assertIn("uniform exponential moment", stopping["activation_births"])
        self.assertIn(
            "N_a=N_0+K-D_pre",
            stopping["exact_population_bookkeeping"],
        )
        self.assertIn("mixed Poisson", stopping["mixed_poisson_control"])
        self.assertIn(
            "E[K;regular]<=E[K]",
            stopping["regular_event_weighting"],
        )
        self.assertIn(
            "no conditional bound",
            stopping["regular_event_weighting"],
        )

    def test_endpoint_envelope_and_shell_contract(self) -> None:
        endpoint = self.result["endpoint_scalar_orders"]
        self.assertIn("maximal factorial/total", endpoint["deterministic_envelope"])
        self.assertIn("D_pre remains", endpoint["deterministic_envelope"])
        self.assertIn("downward exits", endpoint["shell_exits"])
        self.assertTrue(endpoint["strict_polynomial_margin"])

    def test_certified_arithmetic(self) -> None:
        arithmetic = self.result["certified_pair_arithmetic"]
        self.assertEqual(
            (
                arithmetic["certified_before_branch"]["positive"],
                arithmetic["certified_before_branch"]["signed"],
                arithmetic["certified_before_branch"]["total"],
            ),
            (306, 34, 340),
        )
        self.assertEqual(
            (
                arithmetic["certified_final_7"]["positive"],
                arithmetic["certified_final_7"]["signed"],
                arithmetic["certified_final_7"]["total"],
            ),
            (7, 0, 7),
        )
        self.assertEqual(
            (
                arithmetic["certified_after_branch"]["positive"],
                arithmetic["certified_after_branch"]["signed"],
                arithmetic["certified_after_branch"]["total"],
            ),
            (299, 34, 333),
        )
        self.assertTrue(
            arithmetic["certified_after_branch"][
                "equals_exact_hard_333_family"
            ]
        )

    def test_scoped_claim_flags_true_global_false(self) -> None:
        for key in (
            "independent_audit_passed",
            "analytic_activation_survival_certified",
            "analytic_integrated_service_certified",
            "analytic_common_scalar_gluing_certified",
            "candidate_7_pair_recurrence_certified",
        ):
            self.assertTrue(self.result[key])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
