from __future__ import annotations

import unittest

from experiments.quadratic_positive_locus.verify_enlarged_cap_minus_1_over_50 import (
    verify,
)


class EnlargedCapMinusOneOverFiftyTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["integer_bound"], 39)


if __name__ == "__main__":
    unittest.main()
