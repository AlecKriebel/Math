from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "check_k11_completion_probe",
    HERE / "check_results.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load construction-probe checker")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def write_tampered(data: dict, directory: str) -> tuple[Path, str]:
    path = Path(directory) / "tampered.json"
    path.write_text(json.dumps(data, sort_keys=True))
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


class ConstructionProbeResultsTests(unittest.TestCase):
    def test_results_consistency(self) -> None:
        result = CHECK.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["runs_checked"], 26)
        self.assertTrue(result["all_runs_remain_above_half"])

    def test_tampered_coordinate_is_rejected(self) -> None:
        data = json.loads(CHECK.RESULTS_PATH.read_text())
        data["runs"][0]["final_coordinates_float64"][0][0] += 1e-5
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaises(CHECK.ResultsError):
                CHECK.verify(path, digest)

    def test_tampered_best_summary_is_rejected(self) -> None:
        data = json.loads(CHECK.RESULTS_PATH.read_text())
        data["best"]["run_index"] = 0
        with tempfile.TemporaryDirectory() as directory:
            path, digest = write_tampered(data, directory)
            with self.assertRaisesRegex(CHECK.ResultsError, "best run index"):
                CHECK.verify(path, digest)

    def test_wrong_hash_is_rejected(self) -> None:
        with self.assertRaisesRegex(CHECK.ResultsError, "SHA-256 mismatch"):
            CHECK.verify(expected_results_sha256="0" * 64)


if __name__ == "__main__":
    unittest.main()
