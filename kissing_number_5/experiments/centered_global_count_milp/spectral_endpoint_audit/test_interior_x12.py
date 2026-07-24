"""Tamper tests for the exact X=12 interior-shadow verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_interior_x12", HERE / "verify_interior_x12.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load X=12 verifier")
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class InteriorX12VerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = json.loads(verifier.SOURCE.read_text())

    def verify_modified(self, modified: dict[str, object]) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.json"
            path.write_text(json.dumps(modified))
            verifier.verify(path)

    def test_source_verifies(self) -> None:
        result = verifier.verify()
        self.assertEqual(result["X_equals_40V"], 12)
        self.assertEqual(result["Y_equals_800D"], -51)
        self.assertEqual(result["spectral_residual"], 10350)

    def test_edge_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.source)
        modified["final_edge_counts"][1] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_triangle_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.source)
        modified["final_triple_counts"][0] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_row_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.source)
        modified["final_degree_type_counts"][0] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_no_good_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.source)
        modified["excluded_spectral_x"] = []
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)


if __name__ == "__main__":
    unittest.main()
