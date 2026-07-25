#!/usr/bin/env python3
"""Regression tests for the quarter-grid antipodal moment identity."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_quarter_grid_antipodal_pair_moment_obstruction import (
    DEFAULT_CERTIFICATE,
    VerificationError,
    verify,
)


class QuarterGridAntipodalPairMomentObstructionTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(
            [branch["r"] for branch in result["branches_verified"]],
            [14, 15, 16],
        )
        self.assertEqual(
            result["identity_coefficients"],
            ["0", "-126", "0", "-63", "-252", "0", "0", "-126", "0"],
        )

    def test_tampered_multiplier_is_rejected(self) -> None:
        certificate = json.loads(DEFAULT_CERTIFICATE.read_text())
        certificate["multipliers"]["M_3"] += 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / DEFAULT_CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_tampered_branch_gap_is_rejected(self) -> None:
        certificate = json.loads(DEFAULT_CERTIFICATE.read_text())
        certificate["excluded_antipode_pair_branches"][2]["rank_gap"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / DEFAULT_CERTIFICATE.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(VerificationError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
