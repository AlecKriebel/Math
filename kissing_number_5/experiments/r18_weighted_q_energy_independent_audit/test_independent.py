from __future__ import annotations

import subprocess
import sys
import unittest

from experiments.r18_weighted_q_energy_independent_audit.verify_independent import (
    verify,
)


class IndependentR18WeightedQEnergyAudit(unittest.TestCase):
    def test_exact_audit(self) -> None:
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["ordered_antipodal_count"], 36)
        self.assertEqual(result["ordered_cycle_count"], 10)
        self.assertEqual(result["representative_weight"], "A/3")
        self.assertEqual(result["copositive_constant"], "32/45")
        self.assertEqual(result["unit_weight_cycle_lower_bound"], "64/9")

    def test_exact_audit_under_optimized_python(self) -> None:
        module = (
            "experiments.r18_weighted_q_energy_independent_audit."
            "verify_independent"
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
