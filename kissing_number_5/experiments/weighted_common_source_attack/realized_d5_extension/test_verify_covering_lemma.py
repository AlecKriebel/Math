#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import unittest

import verify_covering_lemma


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_covering_lemma.py"


class CoveringVerifierTests(unittest.TestCase):
    def test_exact_verifier_normal_and_optimized(self):
        for optimized in (False, True):
            command = [sys.executable]
            if optimized:
                command.append("-O")
            command.append(str(VERIFIER))
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"covering_inner_product": "3/4"', result.stdout)

    def test_sign_cases_have_exact_constraint_count(self):
        for sigma in (-1, 1):
            for tau in (-1, 1):
                system = verify_covering_lemma.constraints(sigma, tau)
                self.assertEqual(len(system), 19)
                self.assertEqual(len({name for _, _, name in system}), 19)

    def test_invalid_sign_rejected(self):
        with self.assertRaises(verify_covering_lemma.VerificationError):
            verify_covering_lemma.constraints(0, 1)

    def test_singular_basis_returns_none(self):
        rows = [(1, 0, 0, 0, 0)] * 5
        self.assertIsNone(verify_covering_lemma.solve_basis(rows, [0] * 5))


if __name__ == "__main__":
    unittest.main()
