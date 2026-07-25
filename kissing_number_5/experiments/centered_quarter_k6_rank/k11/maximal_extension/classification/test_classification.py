from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "verify_k40_classification",
    HERE / "verify_classification.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load K40 classification verifier")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def write_tampered(data: dict, directory: str) -> tuple[Path, str]:
    path = Path(directory) / "tampered.json"
    path.write_text(json.dumps(data, sort_keys=True))
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


class CompletionClassificationTests(unittest.TestCase):
    def test_exact_classification(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["completions_checked"], 13)
        self.assertEqual(result["D5_atoms"], [6, 23])
        self.assertEqual(len(result["L5_atoms"]), 11)
        self.assertEqual(result["Q5_atoms"], [])
        self.assertEqual(result["R5_atoms"], [])

    def test_tampered_gram_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["entries"][0]["upper_triangle_gram_scaled_by_four"][1] += 1
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(
                VERIFY.ClassificationError,
                "stored Gram",
            ):
                VERIFY.verify(path, digest)

    def test_tampered_permutation_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        permutation = data["entries"][0]["completion_to_known_permutation"]
        permutation[0], permutation[1] = permutation[1], permutation[0]
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(
                VERIFY.ClassificationError,
                "claimed exact isometry fails",
            ):
                VERIFY.verify(path, digest)

    def test_tampered_coordinate_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["entries"][0]["coordinates_numerator_over_sqrt2"][0][0] = "1/3"
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(
                VERIFY.ClassificationError,
                "exported coordinates",
            ):
                VERIFY.verify(path, digest)

    def test_wrong_hash_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            VERIFY.ClassificationError,
            "SHA-256 mismatch",
        ):
            VERIFY.verify(expected_certificate_sha256="0" * 64)


if __name__ == "__main__":
    unittest.main()
