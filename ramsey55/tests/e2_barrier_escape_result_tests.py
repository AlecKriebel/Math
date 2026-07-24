#!/usr/bin/env python3
"""Tests for the retained E=2 barrier-escape result checker."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from e2_barrier_escape_result_check import check  # noqa: E402


ARTIFACT = (
    ROOT / "results/verification/e2_barrier_escape_atomic_ceiling15_v1.json"
)


class BarrierEscapeResultTests(unittest.TestCase):
    def test_retained_result_bindings_and_identities(self) -> None:
        result = check(ARTIFACT)
        self.assertTrue(result["accepted"])
        self.assertTrue(all(result["checks"].values()))

    def test_pair_coverage_tamper_is_rejected(self) -> None:
        record = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        record["result"]["pair_checks"] -= 1
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / "changed.json"
            changed.write_text(json.dumps(record), encoding="utf-8")
            result = check(changed)
        self.assertFalse(result["accepted"])
        self.assertFalse(result["checks"]["pair_coverage_identity"])


if __name__ == "__main__":
    unittest.main()
