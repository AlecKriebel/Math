from __future__ import annotations

import unittest

from experiments.quadratic_positive_residual.verify_exact_subregion import verify


class ExactSubregionTest(unittest.TestCase):
    def test_endpoint_constants(self) -> None:
        self.assertEqual(verify()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
