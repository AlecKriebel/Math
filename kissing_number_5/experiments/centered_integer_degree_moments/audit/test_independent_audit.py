#!/usr/bin/env python3
"""Tamper tests for the independent centered degree-moment audit."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from .independent_audit import (
    audit_mixture,
    audit_one,
    centered_rows,
    default_mixture_pair,
    default_pairs,
)


class IndependentAuditTest(unittest.TestCase):
    def test_independent_row_enumeration(self) -> None:
        rows = centered_rows()
        self.assertEqual(len(rows), 27041)
        self.assertEqual(sum(row[0] == 0 for row in rows), 14720)
        self.assertEqual(sum(row[0] == 1 for row in rows), 12321)

    def test_all_present_certificates(self) -> None:
        results = [
            audit_one(certificate, source)
            for certificate, source in default_pairs()
        ]
        self.assertGreaterEqual(len(results), 3)
        self.assertTrue(all(result["expected_value"].startswith("-") for result in results))

    def test_exact_repaired_mixture(self) -> None:
        pair = default_mixture_pair()
        self.assertIsNotNone(pair)
        result = audit_mixture(*pair)
        self.assertEqual(result["positive_atoms"], 18)
        self.assertTrue(result["exact_second_moment_match"])

    def test_tampered_expected_value_is_rejected(self) -> None:
        certificate_path, source_path = default_pairs()[1]
        certificate = json.loads(certificate_path.read_text())
        certificate["expected_value"] = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / certificate_path.name
            path.write_text(json.dumps(certificate))
            with self.assertRaises(AssertionError):
                audit_one(path, source_path)

    def test_tampered_source_is_rejected(self) -> None:
        certificate_path, source_path = default_pairs()[2]
        source = json.loads(source_path.read_text())
        source["nu"][0] = str(int(source["nu"][0].split("/")[0]) + 1) + "/" + source["nu"][0].split("/")[1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / source_path.name
            path.write_text(json.dumps(source))
            with self.assertRaises(AssertionError):
                audit_one(certificate_path, path)


if __name__ == "__main__":
    unittest.main()
