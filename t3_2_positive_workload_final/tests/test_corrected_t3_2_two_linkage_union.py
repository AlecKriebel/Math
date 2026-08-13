from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

import corrected_t3_2_two_linkage_union as corrected_union


FROZEN_PAYLOAD = (
    Path(__file__).resolve().parents[1]
    / "research_notes"
    / "corrected_t3_2_two_linkage_union_frozen_payload.json"
)
EXPECTED_FROZEN_FILE_SHA256 = (
    "b84e6795a1d706271421e61ca7c4f8e3eec8b106134935011739ac2280b90890"
)


class CorrectedT32TwoLinkageUnionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = corrected_union.certificate()

    def test_corrected_baseline_is_used(self) -> None:
        self.assertEqual(
            self.result["corrected_interface"],
            {
                "criterion": "S-tier-superlevel cut",
                "positive_residual_pairs": 2312,
                "positive_residual_sha256": "0297ba35311c757cd5c6ec548d2af18410dfd37e791c7679de932fe4bf38695b",
                "signed_residual_pairs": 199,
                "signed_residual_sha256": "1a9c06123645855d3b4f23d4886b0ada3c3ff3614fc94a7d22c01f411c1355c8",
                "total_residual_pairs": 2511,
                "total_residual_sha256": "0c57f530eb44a688520cc1706f830afa18063f4d08d24e5006f47a5666edd0b3",
                "certificate_sha256": "77c7ce0d2325379acfed7b13a44f9577454279275918ee14f968e313b488a7e0",
            },
        )

    def test_exact_fourteen_branch_partition(self) -> None:
        expected = {
            "affine_stoichiometric_151": (151, 143, 8),
            "all_active_only_51": (51, 51, 0),
            "critical_one_active_15": (15, 15, 0),
            "easy_common_w_416": (416, 414, 2),
            "exact_common_w_26": (26, 26, 0),
            "hard_common_w_333": (333, 299, 34),
            "post_rank_one_one_active_92": (92, 92, 0),
            "rank_one_no_promotion_141": (141, 141, 0),
            "rank_two_14": (14, 14, 0),
            "rank_two_scalar_13": (13, 13, 0),
            "rank_two_stopped_7": (7, 7, 0),
            "suppressed_promotion_4": (4, 4, 0),
            "two_active_promotion_36": (36, 32, 4),
            "universal_one_active_net_1212": (1212, 1061, 151),
        }
        observed = {
            name: (entry["pairs"], entry["positive"], entry["signed"])
            for name, entry in self.result["branches"].items()
        }
        self.assertEqual(observed, expected)
        self.assertEqual(self.result["branch_count"], 14)
        self.assertTrue(self.result["pairwise_disjoint"])
        self.assertTrue(self.result["union_equals_corrected_baseline"])
        self.assertEqual(self.result["remaining_pairs"], 0)
        self.assertEqual(sum(value[0] for value in observed.values()), 2511)

    def test_exact_byte_analytic_manifest(self) -> None:
        corrected_union.verify_exact_dependencies()
        self.assertEqual(
            set(self.result["branches"]),
            set(corrected_union.ANALYTIC_DEPENDENCY_MANIFEST),
        )
        for entry in self.result["branches"].values():
            self.assertEqual(
                entry["analytic_dependency"]["status"],
                "analytic dependencies independently audited",
            )

    def test_hashes_and_claim_boundary(self) -> None:
        self.assertEqual(
            self.result["rows_sha256"], corrected_union.EXPECTED_ROWS_SHA256
        )
        self.assertEqual(
            self.result["payload_sha256"],
            corrected_union.EXPECTED_PAYLOAD_SHA256,
        )
        self.assertEqual(
            self.result["finite_code_role"],
            "finite identities only; no analytic proof",
        )
        self.assertEqual(
            self.result["global_claim_status"],
            "not asserted by this finite certificate",
        )
        self.assertNotIn("global_t3_2_certified", self.result)
        self.assertNotIn("global_t3_2_theorem_independently_audited", self.result)

    def test_frozen_payload(self) -> None:
        raw = FROZEN_PAYLOAD.read_bytes()
        self.assertEqual(sha256(raw).hexdigest(), EXPECTED_FROZEN_FILE_SHA256)
        self.assertEqual(json.loads(raw), self.result)


if __name__ == "__main__":
    unittest.main()
