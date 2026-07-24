from __future__ import annotations

import unittest

from .verify_productpool_via_deleted_k5 import verify


class ProductPoolViaDeletedK5Tests(unittest.TestCase):
    def test_exact_cross_check(self) -> None:
        report = verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["positive_k6_atoms"], 74)
        self.assertEqual(report["product_rows_checked"], 560)
        self.assertEqual(report["negative_rows"], 0)
        self.assertEqual(report["zero_rows"], 113)
        self.assertEqual(
            report["atomwise_k6_equals_deleted_k5_checks"], 74 * 560
        )


if __name__ == "__main__":
    unittest.main()
