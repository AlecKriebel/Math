from __future__ import annotations

import unittest

from experiments.quadratic_positive_residual.verify_local_depth_weight_countermodel import (
    verify,
)


class LocalDepthWeightCountermodelTest(unittest.TestCase):
    def test_exact_countermodel(self) -> None:
        self.assertEqual(verify()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
