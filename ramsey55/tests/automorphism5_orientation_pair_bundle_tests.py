#!/usr/bin/env python3
"""Tests for the checkpointed order-5 orientation-pair bundle."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bundle = load(
    "orientation_pair_bundle",
    ROOT / "src" / "automorphism5_orientation_pair_bundle.py",
)
checker = load(
    "selector_checker",
    ROOT / "verify" / "automorphism5_selector_cover_check.py",
)


class Automorphism5OrientationPairBundleTests(unittest.TestCase):
    def test_pair_ids_partition_all_orientation_indices(self) -> None:
        pairs = [
            (start, start + 1, bundle.batch_id(start))
            for start in range(0, 80, 2)
        ]
        self.assertEqual(
            [index for start, stop, _ in pairs for index in (start, stop)],
            list(range(80)),
        )
        self.assertEqual(pairs[0][2], "pair_000_001")
        self.assertEqual(pairs[-1][2], "pair_078_079")

    def test_independent_orientation_quotient_has_size_eighty(self) -> None:
        self.assertEqual(len(checker.independent_orientations()), 80)

    def test_frozen_storage_gate_arithmetic(self) -> None:
        self.assertEqual(
            bundle.MAX_ARTIFACT_BYTES
            + bundle.MAX_TRANSIENT_BYTES
            + bundle.RESERVE_BYTES,
            7_294_967_296,
        )

    def test_each_pair_formula_is_small_and_exact(self) -> None:
        with self.subTest("pair 15-16"):
            import tempfile

            with tempfile.TemporaryDirectory() as raw:
                cnf, _, metadata = bundle.generate_formula(
                    Path(raw), 15, 2
                )
                self.assertEqual(metadata["batch_start"], 15)
                self.assertEqual(metadata["batch_count"], 2)
                self.assertEqual(metadata["variable_count"], 185)
                self.assertEqual(metadata["clause_count"], 384_196)
                self.assertEqual(
                    bundle.sha256_file(cnf),
                    "5578637178ba738676f6476561c8b6eb5eeff9ecac6249848eccfc4acbdc1a9a",
                )


if __name__ == "__main__":
    unittest.main()
