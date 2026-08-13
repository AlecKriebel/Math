from __future__ import annotations

import unittest

import remaining_18496_globally_nonmixed_certificate as certificate


class Remaining18496GloballyNonmixedCertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = certificate.certificate()

    def test_exact_remainder_count(self) -> None:
        self.assertEqual(self.result["remainder_pairs"], 18_496)

    def test_literal_global_nonmixing(self) -> None:
        self.assertEqual(self.result["globally_nonmixed_pairs"], 18_496)
        self.assertEqual(self.result["violations"], 0)

    def test_complete_cell_menu(self) -> None:
        self.assertEqual(self.result["active_coordinate_pairs"], 3)
        self.assertEqual(self.result["workload_cells_per_active_pair"], 7)

    def test_claim_boundary(self) -> None:
        self.assertIn("no recurrence claim", self.result["claim_scope"])


if __name__ == "__main__":
    unittest.main()
