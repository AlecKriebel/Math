#!/usr/bin/env python3
"""Focused regression for the asymmetric h=0 higher-digit checkpoint."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_h0_asymmetric_higher_digits as verifier


class AsymmetricHigherDigitTest(unittest.TestCase):
    def test_certificate(self) -> None:
        result = verifier.audit()
        self.assertEqual(result["first_layer"], (18, 36))
        self.assertEqual(result["halfturn_dimensions"], (21, 15))
        self.assertEqual(result["asymmetric_slice"], (6, 15))
        self.assertEqual(result["zero_digit_prefix"], 2)
        self.assertEqual(result["digit_3_nonzero_rows"], 13)
        self.assertFalse(result["row_margin_catalog_member"])
        self.assertEqual(result["bounded_digit3_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
