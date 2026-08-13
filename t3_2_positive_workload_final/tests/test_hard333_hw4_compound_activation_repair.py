from __future__ import annotations

from collections import Counter
import unittest

import hard333_hw4_compound_activation_repair as candidate


class Hard333HW4CompoundActivationRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_exact_selector_and_relabelled_geometry(self) -> None:
        selector = self.result["selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (4, 4, 0),
        )
        self.assertEqual(selector["pair_sha256"], candidate.EXPECTED_PAIR_SHA256)
        self.assertEqual(
            selector["activation_resistance_histogram"], {"1": 2, "2": 2}
        )
        rows = candidate.geometry_rows()
        self.assertEqual(len(rows), 4)
        self.assertEqual(
            Counter(row["unique_mixed_carrier"] for row in rows),
            {"XY": 2, "XC": 2},
        )
        self.assertTrue(
            all(
                row["pure_transverse_complexes"] == ["2Y", "YC", "2C"]
                for row in rows
            )
        )

    def test_false_linear_pf_regression(self) -> None:
        regression = self.result["linear_pf_regression"]
        self.assertFalse(regression["old_pointwise_pf_bound_valid"])
        self.assertEqual(regression["only_enabled_top_source"], "2C")
        self.assertIn("O(1)", regression["exact_top_drift"])
        self.assertIn("Theta(n)", regression["claimed_logistic_rhs"])

    def test_all_strong_digraphs_have_bounded_ignition(self) -> None:
        contraction = self.result["finite_cut_contraction"]
        self.assertEqual(contraction["strong_simple_digraphs"], 1606)
        self.assertEqual(
            contraction["ignition_profile"],
            {
                "no_mass_loss_length_2": 1420,
                "one_mass_loss_length_3": 186,
            },
        )
        witness = contraction["sparse_dip_witness"]
        self.assertEqual(witness["transverse_mass_path"], [2, 1, 2, 3])
        self.assertTrue(witness["one_unit_dip_is_necessary"])

    def test_full_chain_and_endpoint_targets_are_frozen(self) -> None:
        activation = self.result["candidate_compound_activation"]
        self.assertTrue(activation["all_reactions_retained"])
        self.assertIn("1-C/M-C*M/n", activation["contracted_trace_target"])
        endpoint = self.result["candidate_service_and_return"]
        self.assertEqual(endpoint["duration_and_endpoint_order"],
                         "one uniform integer p>8")
        self.assertEqual(endpoint["fractional_stop"],
                         "n<=rho*n0 or n>=2*n0")

    def test_all_claim_flags_false(self) -> None:
        for key in (
            "compound_trace_comparison_certified",
            "deterministic_service_integral_certified",
            "single_macroepisode_service_certified",
            "fractional_return_iteration_certified",
            "common_W_endpoint_certified",
            "H_w_4_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])


if __name__ == "__main__":
    unittest.main()
