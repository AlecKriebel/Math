#!/usr/bin/env python3

import json
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_global_flag_exchangeability.py"


class GlobalFlagExchangeabilityTest(unittest.TestCase):
    def test_exact_verifier(self):
        completed = subprocess.run(
            [sys.executable, str(VERIFIER)],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["D5_direct_global_square"], "646060")
        self.assertEqual(
            len(report["negative_pseudodistribution_rows"]), 8
        )


if __name__ == "__main__":
    unittest.main()
