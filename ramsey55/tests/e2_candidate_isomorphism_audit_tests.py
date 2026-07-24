#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e2_candidate_isomorphism_audit import (  # noqa: E402
    normalized_labels,
    partition,
)


class E2CandidateIsomorphismAuditTests(unittest.TestCase):
    def test_partition_ignores_label_names(self) -> None:
        self.assertEqual(partition(["a", "b", "a", "c", "b"]), [[0, 2], [1, 4], [3]])
        self.assertEqual(
            partition(["x", "y", "x", "z", "y"]), [[0, 2], [1, 4], [3]]
        )

    def test_complement_normalization(self) -> None:
        self.assertEqual(
            normalized_labels(["b", "a", "z"], ["a", "c", "y"]),
            ["a", "a", "y"],
        )


if __name__ == "__main__":
    unittest.main()
