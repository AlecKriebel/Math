from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_frozen_support_size.py"
SPEC = importlib.util.spec_from_file_location("verify_k10_size", PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class FrozenK9SupportSizeTests(unittest.TestCase):
    def test_constant_and_single_edge_orbits(self) -> None:
        zero = (0,) * 36
        one_edge = (1,) + (0,) * 35
        result = VERIFY.run_core([zero, one_edge])
        self.assertEqual(
            result,
            {
                "k9_orbits": 2,
                "labeled_k9_support": 37,
                "orbit_size_distribution": {1: 1, 36: 1},
                "automorphism_size_distribution": {10080: 1, 362880: 1},
                "minimum_k10_color_trials": 259,
                "packed_support_bytes_at_16_per_pattern": 592,
            },
        )

    def test_exact_size(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["labeled_k9_support"], 16057440)

    def test_tampered_source_hash_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["source_k9_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
