#!/usr/bin/env python3
"""Regression test for the bounded dense-shell classifier pilot."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_dense_shell_classifier_pilot import verify


class DenseShellClassifierPilotTest(unittest.TestCase):
    def test_pinned_shards_and_independent_replay(self) -> None:
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["h1_canonical_decorations"], 100)
        self.assertEqual(result["h0_canonical_decorations"], 10)
        self.assertEqual(result["h1_total_canonical_decorations"], 22_426_752)
        self.assertEqual(result["h0_total_canonical_decorations"], 1_999_128)
        self.assertEqual(result["joint_char2_mod9_hits"], 0)
        self.assertEqual(result["exact_zero_hits"], 0)
        self.assertEqual(result["prefix_partition_shards"], 1_458)
        self.assertEqual(
            result["residue_union_affine_upper"],
            47_855_051_781_696,
        )
        self.assertEqual(
            result["primitive_leaf_upper"],
            71_779_465_554_048,
        )
        self.assertGreaterEqual(result["independent_witness_replays"], 8)


if __name__ == "__main__":
    unittest.main()
