import unittest

import global_atlas_interface_closure as closure
import global_tier_interface as legacy
import s_tier_superlevel_interface as corrected


class SymbolicSuperlevelCutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = corrected.certificate()

    def test_legacy_necessity_counterexample(self) -> None:
        witness = self.result["counterexample_to_legacy_necessity"]
        self.assertEqual(witness["pair"][0], ("C", "2C"))
        self.assertEqual(witness["pair"][1], ("A", "2A", "AB", "AC"))
        self.assertEqual(witness["weight"], [0, 3, 1])
        self.assertEqual(witness["caps"], [0, 2, 2])
        self.assertEqual(witness["global_top_d"], ["AB"])
        self.assertEqual(witness["global_top_s"], ["2C"])
        self.assertEqual(witness["s_level_superlevels"][0], ["2C"])
        self.assertFalse(witness["legacy_global_top_d_cut"])
        self.assertTrue(witness["corrected_s_level_superlevel_cut"])

    def test_legacy_cut_is_sufficient_on_every_finite_identity(self) -> None:
        for masks in (
            closure.POSITIVE_SHIELDED_MASKS,
            closure.SIGNED_SHIELDED_MASKS,
        ):
            for pair in closure.residual_pairs(masks):
                for descriptor in legacy.tier_descriptors():
                    if legacy.universal_orientation_tier_condition(
                        pair,
                        descriptor,
                    ):
                        self.assertTrue(
                            corrected.universal_strong_orientation_condition(
                                pair,
                                descriptor,
                            )
                        )

    def test_pair_sets_are_unchanged(self) -> None:
        expected = {
            "positive": {
                "input_pre_tier_pairs": 3531,
                "tier_certified_pairs": 1219,
                "residual_pairs": 2312,
                "tier_certified_sha256": "744d872920309c361d6d7f806f140a696e3fc3ae0f75d760d8a07f304d562b6b",
                "residual_sha256": "0297ba35311c757cd5c6ec548d2af18410dfd37e791c7679de932fe4bf38695b",
            },
            "signed": {
                "input_pre_tier_pairs": 358,
                "tier_certified_pairs": 159,
                "residual_pairs": 199,
                "tier_certified_sha256": "7f59ea94fe876205ccb72dc97b026b2954feac62375122634aafa318084428ee",
                "residual_sha256": "1a9c06123645855d3b4f23d4886b0ada3c3ff3614fc94a7d22c01f411c1355c8",
            },
        }
        for family, values in expected.items():
            for key, value in values.items():
                self.assertEqual(self.result[family][key], value)
        self.assertEqual(self.result["total_tier_certified_pairs"], 1378)
        self.assertEqual(self.result["total_residual_pairs"], 2511)

    def test_corrected_incidence_counts(self) -> None:
        positive = self.result["positive"]
        self.assertEqual(positive["corrected_failing_incidences"], 12250)
        self.assertEqual(
            positive["corrected_feasible_failing_incidences"],
            9349,
        )
        self.assertEqual(
            positive["corrected_infeasible_failing_incidences"],
            2901,
        )
        self.assertEqual(positive["legacy_false_failure_incidences"], 200)
        self.assertEqual(positive["legacy_false_failure_affected_pairs"], 178)
        self.assertEqual(positive["legacy_false_failure_feasible"], 196)
        self.assertEqual(positive["legacy_false_failure_infeasible"], 4)

        signed = self.result["signed"]
        self.assertEqual(signed["corrected_failing_incidences"], 428)
        self.assertEqual(signed["corrected_feasible_failing_incidences"], 360)
        self.assertEqual(signed["corrected_infeasible_failing_incidences"], 68)
        self.assertEqual(signed["legacy_false_failure_incidences"], 8)
        self.assertEqual(signed["legacy_false_failure_affected_pairs"], 8)
        self.assertEqual(signed["legacy_false_failure_feasible"], 8)
        self.assertEqual(signed["legacy_false_failure_infeasible"], 0)

        self.assertEqual(self.result["total_corrected_failing_incidences"], 12678)
        self.assertEqual(
            self.result["total_corrected_feasible_failing_incidences"],
            9709,
        )
        self.assertEqual(
            self.result["total_corrected_infeasible_failing_incidences"],
            2969,
        )
        self.assertEqual(self.result["total_legacy_false_failure_incidences"], 208)
        self.assertEqual(
            positive["corrected_failing_incidence_sha256"],
            "d607340f62290c47fa03d209b0dbcd42f6dbc51320cdbaedb9e183f04187fd5f",
        )
        self.assertEqual(
            positive["corrected_feasible_incidence_sha256"],
            "e6403c2d36fbb74bf37a498aa0bf41d0f31a7b17a3df302d5b5688080fed9551",
        )
        self.assertEqual(
            signed["corrected_failing_incidence_sha256"],
            "82a3a3ee1c598ea3e79d288da39f3326a3ccec61e6ed85bfba4b38e4c3c2299d",
        )
        self.assertEqual(
            signed["corrected_feasible_incidence_sha256"],
            "3c106e959f2a4fb49bc03a5baaedc09e9de6ef6e6d109b9bfa526b8544278404",
        )

    def test_affine_151_set_is_unchanged(self) -> None:
        self.assertEqual(
            self.result["pairs_without_feasible_corrected_failure"],
            151,
        )
        self.assertEqual(
            self.result["pairs_with_feasible_corrected_failure"],
            2360,
        )
        self.assertEqual(
            self.result["without_feasible_sha256"],
            "55e243945f86d106b920a27e2249a20b7077b5dc718ec06918cca4368e4a6c96",
        )
        self.assertEqual(
            self.result["with_feasible_sha256"],
            "d81f56743d262e7251297306685fdfedba33659839b973516e0d796739bfe8a5",
        )

    def test_pre_tier_branch_counts(self) -> None:
        self.assertEqual(
            self.result["pre_tier_branch_counts"]["positive"],
            {
                "common_active_invariant": 110,
                "exact_residual_pair": 1,
                "exact_seven_support_seam": 6,
                "exact_signed_service_seam": 2,
                "finite_strict_invariant": 187,
                "full_deficiency_zero": 924,
                "residual": 3531,
            },
        )
        self.assertEqual(
            self.result["pre_tier_branch_counts"]["signed"],
            {"full_deficiency_zero": 50, "residual": 358},
        )
        self.assertEqual(
            self.result["certificate_sha256"],
            "77c7ce0d2325379acfed7b13a44f9577454279275918ee14f968e313b488a7e0",
        )


if __name__ == "__main__":
    unittest.main()
