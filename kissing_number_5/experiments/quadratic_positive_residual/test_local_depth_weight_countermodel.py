from __future__ import annotations

import subprocess
import sys
import unittest

from experiments.quadratic_positive_residual.verify_local_depth_weight_countermodel import (
    verify,
)


class LocalDepthWeightCountermodelTest(unittest.TestCase):
    def test_exact_countermodel(self) -> None:
        self.assertEqual(verify()["status"], "PASS")

    def test_optimized_mode(self) -> None:
        module = (
            "experiments.quadratic_positive_residual."
            "verify_local_depth_weight_countermodel"
        )
        completed = subprocess.run(
            [sys.executable, "-O", "-m", module],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('"status": "PASS"', completed.stdout)


if __name__ == "__main__":
    unittest.main()
