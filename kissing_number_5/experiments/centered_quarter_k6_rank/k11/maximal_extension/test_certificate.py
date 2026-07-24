from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from collections import Counter


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_k11_maximal_extensions",
    HERE / "verify_certificate.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load maximal-extension verifier")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def write_tampered(data: dict, directory: str) -> tuple[Path, str]:
    path = Path(directory) / "tampered.json"
    path.write_text(json.dumps(data, sort_keys=True))
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


class MaximalQuarterGridExtensionTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["atoms_checked"], 51)
        self.assertEqual(result["basis_rows_tested_per_atom"], 7**5)
        self.assertEqual(result["maximum_total_points_maximum"], 40)
        self.assertEqual(result["maximum_additional_points_maximum"], 29)

    def test_tampered_coloring_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        entry = data["entries"][0]
        counts = Counter(entry["candidate_colors"])
        first = entry["clique_candidate_indices"][0]
        second = next(
            vertex
            for vertex in entry["clique_candidate_indices"][1:]
            if counts[entry["candidate_colors"][vertex]] > 1
        )
        entry["candidate_colors"][second] = entry["candidate_colors"][first]
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(
                VERIFY.VerificationError,
                "share color",
            ):
                VERIFY.verify(
                    certificate_path=path,
                    expected_certificate_sha256=digest,
                )

    def test_tampered_clique_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        entry = data["entries"][0]
        entry["clique_candidate_indices"][1] = entry[
            "clique_candidate_indices"
        ][0]
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(
                VERIFY.VerificationError,
                "repeated clique vertex",
            ):
                VERIFY.verify(
                    certificate_path=path,
                    expected_certificate_sha256=digest,
                )

    def test_tampered_candidate_count_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["entries"][0]["candidate_count"] += 1
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(
                VERIFY.VerificationError,
                "candidate list is incomplete",
            ):
                VERIFY.verify(
                    certificate_path=path,
                    expected_certificate_sha256=digest,
                )

    def test_wrong_hash_is_rejected_before_parsing(self) -> None:
        with self.assertRaisesRegex(
            VERIFY.VerificationError,
            "certificate SHA-256 mismatch",
        ):
            VERIFY.verify(expected_certificate_sha256="0" * 64)


if __name__ == "__main__":
    unittest.main()
