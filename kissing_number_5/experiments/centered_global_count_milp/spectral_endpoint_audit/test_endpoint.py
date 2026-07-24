"""Tamper tests for the exact spectral-endpoint verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_spectral_endpoint", HERE / "verify_endpoint.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load endpoint verifier")
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class EndpointVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.certificate = json.loads(verifier.CERTIFICATE.read_text())

    def verify_modified(self, modified: dict[str, object]) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            path.write_text(json.dumps(modified))
            verifier.verify(
                certificate_path=path,
                source_path=(
                    HERE.parent / "result_degree_lift_exact_spectral_d0.json"
                ),
            )

    def test_certificate_verifies(self) -> None:
        result = verifier.verify()
        self.assertEqual(result["Y_equals_800D"], -6)
        self.assertEqual(
            [item["zero_height_count"] for item in result["marginal_shadows"]],
            [33, 25],
        )

    def test_edge_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.certificate)
        modified["edge_counts"][1] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_triangle_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.certificate)
        modified["shadows"][0]["triple_counts"][4] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_row_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.certificate)
        modified["shadows"][1]["row_type_counts"][0]["degree"][3] += 1
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_z_square_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.certificate)
        modified["shadows"][0]["row_type_counts"][0]["z_square"] = "1"
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)

    def test_source_hash_tamper_fails(self) -> None:
        modified = copy.deepcopy(self.certificate)
        modified["source_result_sha256"] = "0" * 64
        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(modified)


if __name__ == "__main__":
    unittest.main()
