#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalog42_e2_extension_proof_batch import (  # noqa: E402
    check_primary_model,
    decode_graph6,
    proof_verified,
)


class Catalog42E2ExtensionProofBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lines = [
            line.strip()
            for line in (ROOT / "data" / "r55_42some.g6")
            .read_text(encoding="ascii")
            .splitlines()
            if line.strip() and not line.startswith("#")
        ]

    def test_known_models_are_checked_as_exact_e2_extensions(self) -> None:
        models = {
            42: "111111111011010000110000001110010111100000",
            256: "111111111000010111001000010111101000000000",
        }
        for line_number, bits in models.items():
            checked = check_primary_model(self.lines[line_number - 1], bits)
            self.assertTrue(checked["valid"])
            self.assertEqual(checked["conflict_count"], 2)
            self.assertTrue(
                all(42 in conflict["vertices"] for conflict in checked["conflicts"])
            )

    def test_batch_decoder_agrees_on_order_and_symmetry(self) -> None:
        adjacency = decode_graph6(self.lines[0])
        self.assertEqual(len(adjacency), 42)
        for left, row in enumerate(adjacency):
            self.assertEqual((row >> left) & 1, 0)
            for right in range(42):
                self.assertEqual((row >> right) & 1, (adjacency[right] >> left) & 1)

    def test_proof_transcript_requires_verified_status_line(self) -> None:
        self.assertTrue(proof_verified("c details\ns VERIFIED\n"))
        self.assertFalse(proof_verified("c contains s VERIFIED text\n"))
        self.assertFalse(proof_verified("s NOT VERIFIED\n"))


if __name__ == "__main__":
    unittest.main()
