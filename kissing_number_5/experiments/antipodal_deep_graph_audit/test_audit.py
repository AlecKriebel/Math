"""Regression and tamper tests for the odd-deficit audit."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verifier = load_module("odd_deficit_audit_verifier", HERE / "verify.py")


class OddDeficitAuditTests(unittest.TestCase):
    def verify_modified(self, source: dict[str, object]) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.json"
            path.write_text(json.dumps(source, indent=2) + "\n")
            verifier.verify(path, enforce_pinned_hash=False)

    def test_original_verifies(self) -> None:
        report = verifier.verify()
        self.assertEqual(report["a4_triangle_free_violations"], 0)

    def test_independent_set_primitive(self) -> None:
        cycle_five = [0] * 5
        for vertex in range(5):
            neighbor = (vertex + 1) % 5
            cycle_five[vertex] |= 1 << neighbor
            cycle_five[neighbor] |= 1 << vertex
        self.assertTrue(
            verifier.has_independent_set(cycle_five, 2)
        )
        self.assertFalse(
            verifier.has_independent_set(cycle_five, 3)
        )

    def test_histogram_tamper_fails(self) -> None:
        source = json.loads(verifier.SOURCE.read_bytes())
        modified = copy.deepcopy(source)
        modified["full_labeled_enumerations"][1][
            "edge_count_histogram"
        ]["10"] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_example_tamper_fails(self) -> None:
        source = json.loads(verifier.SOURCE.read_bytes())
        modified = copy.deepcopy(source)
        modified["full_labeled_enumerations"][0][
            "maximum_example_edges"
        ][0] = [0, 1]
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_a4_survivor_tamper_fails(self) -> None:
        source = json.loads(verifier.SOURCE.read_bytes())
        modified = copy.deepcopy(source)
        modified["a4_violation_enumeration"][
            "triangle_free_survivors"
        ] = 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_status_tamper_fails(self) -> None:
        source = json.loads(verifier.SOURCE.read_bytes())
        modified = copy.deepcopy(source)
        modified["evidence_status"] = "GENERAL LEMMA PROVED BY SEARCH"
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)


if __name__ == "__main__":
    unittest.main()
