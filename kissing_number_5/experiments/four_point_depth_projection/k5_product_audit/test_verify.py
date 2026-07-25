from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path
import tempfile
import unittest

from .verify import (
    common_neighbor,
    common_pair_capacity,
    negative_sum_tail,
    verify,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXTENSION = ROOT / "certificates" / "centered_quarter_k5_extension.json"


class K5ProductAuditTests(unittest.TestCase):
    def test_exact_product_audit(self) -> None:
        report = verify(SOURCE, EXTENSION)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(
            report["violating_rows"],
            [
                "q=-1/2,b=1/2,M=1",
                "q=-1/4,b=1/2,M=3",
            ],
        )

    def test_strict_and_nonstrict_boundaries(self) -> None:
        # At q=-1/2 the radical is exactly one, so total=-1/300 is
        # equality in the strict tail and must not be counted.
        self.assertFalse(negative_sum_tail(Q(-1, 2), Q(-1, 300), Q(0)))
        self.assertTrue(negative_sum_tail(Q(-1, 2), Q(-1, 299), Q(0)))
        self.assertFalse(negative_sum_tail(Q(-1, 2), Q(0), Q(0)))
        with self.assertRaises(ValueError):
            negative_sum_tail(Q(-1), Q(-1, 2), Q(0))

        # Common-neighbor threshold equality is included.
        self.assertTrue(common_neighbor(Q(1, 2), Q(1, 2), Q(1, 2)))
        self.assertFalse(common_neighbor(Q(1, 4), Q(1, 2), Q(1, 2)))

        # Capacity-table endpoints are deliberately on the weaker side.
        self.assertEqual(common_pair_capacity(Q(-1, 2), Q(1, 2)), 1)
        self.assertEqual(common_pair_capacity(Q(-1, 4), Q(1, 2)), 3)
        self.assertEqual(common_pair_capacity(Q(0), Q(1, 2)), 6)

    def test_source_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / EXTENSION.name
            data = json.loads(EXTENSION.read_text())
            data["atoms"][0]["weight"] = "1"
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                verify(SOURCE, path)


if __name__ == "__main__":
    unittest.main()
