from __future__ import annotations

import unittest

from experiments.quadratic_positive_locus.verify_exact_reduction import verify


class ExactReductionTest(unittest.TestCase):
    def test_exact_reduction(self) -> None:
        self.assertEqual(verify()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
