from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
VERIFIER_PATH = HERE / "verify_direct_k6_independent.py"
SPEC = importlib.util.spec_from_file_location("k6_independent", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class IndependentK6AuditTests(unittest.TestCase):
    def test_exact_certificate_and_face_scaling(self) -> None:
        report = VERIFY.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["k6_rank"], 5)
        self.assertEqual(report["positive_orbit_masses"], 51)
        self.assertEqual(report["k6_distinct_orbits"], 51)
        self.assertEqual(report["k6_labeled_support_union"], 26820)
        self.assertEqual(report["induced_k5"]["positive_orbits"], 266)
        self.assertEqual(report["induced_k4"]["positive_orbits"], 383)
        self.assertTrue(report["induced_k4"]["direct_equals_via_k5"])

    def verify_tampered(self, data: dict) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                VERIFY.verify(
                    certificate_path=path, pin_certificate_hash=False
                )

    def test_underlying_equations_reject_weight_tamper(self) -> None:
        data = json.loads(VERIFY.K6_PATH.read_text())
        data["atoms"][0]["weight"] = str(
            Q(data["atoms"][0]["weight"]) + Q(1, 10**12)
        )
        self.verify_tampered(data)

    def test_underlying_geometry_rejects_edge_tamper(self) -> None:
        data = json.loads(VERIFY.K6_PATH.read_text())
        data["atoms"][0][VERIFY.EDGE_KEY6][0] = 0
        self.verify_tampered(data)

    def test_orbit_semantics_reject_duplicate_orbit(self) -> None:
        data = json.loads(VERIFY.K6_PATH.read_text())
        data["atoms"][1][VERIFY.EDGE_KEY6] = list(
            data["atoms"][0][VERIFY.EDGE_KEY6]
        )
        data["atoms"][1]["triangle_orbit_indices"] = list(
            data["atoms"][0]["triangle_orbit_indices"]
        )
        self.verify_tampered(data)


if __name__ == "__main__":
    unittest.main()
