from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from experiments.four_point_depth_projection.k7_product_audit import (
    verify_k7_product_semantics as semantics,
)


class K7ProductSemanticsTests(unittest.TestCase):
    def test_full_exact_audit(self) -> None:
        report = semantics.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(
            report["stored_direct_k7_audit"]["negative_rows"], 45
        )
        self.assertEqual(
            report["candidate_k7_deletion_crosscheck"][
                "atom_state_deletion_identities"
            ],
            53 * 560,
        )

    def test_abstract_deletion_identity(self) -> None:
        report = semantics.verify_sampling_and_abstract_identity()
        self.assertEqual(
            report["one_point_inclusion_probability"], "5/39"
        )
        self.assertEqual(
            report[
                "ordered_distinct_pair_inclusion_probability"
            ],
            "10/741",
        )
        self.assertEqual(
            report["abstract_membership_identities"],
            7 * 8 * 32 * 32,
        )

    def test_wrong_k7_pair_coefficient_breaks_identity(self) -> None:
        # H={0,1}, Gamma={1,2}; hence h=2,g=2,i=1,c=3.
        depth_mask = 0b00011
        common_mask = 0b00110
        capacity = 3
        required = 5
        correct = semantics.set_pattern_k7_slack(
            depth_mask, common_mask, capacity, required
        )
        deleted = semantics.set_pattern_deleted_sum(
            depth_mask, common_mask, capacity, required
        )
        self.assertEqual(deleted, 2 * correct)
        # Replacing the exact coefficient 741 by 740 raises the primitive
        # slack by c=3, so the identity must fail.
        wrong = correct + 3
        self.assertNotEqual(deleted, 2 * wrong)

    def test_tampered_direct_certificate_is_rejected(self) -> None:
        data = json.loads(semantics.DIRECT_K7.read_text())
        data["atoms"][0]["weight"] = "1/2"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                semantics.verify(direct_k7_path=path)


if __name__ == "__main__":
    unittest.main()
