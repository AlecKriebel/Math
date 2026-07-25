#!/usr/bin/env python3

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import verify_uniform_conflict_charge_counterexample as verifier


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "uniform_conflict_charge_counterexample.json"
VERIFIER = HERE / "verify_uniform_conflict_charge_counterexample.py"


class UniformConflictChargeCounterexampleTests(unittest.TestCase):
    def run_cli(self, path, optimized=False):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([str(VERIFIER), str(path)])
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def load(self):
        with CERTIFICATE.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write_mutation(self, data):
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        )
        with handle:
            json.dump(data, handle)
        path = Path(handle.name)
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_valid_certificate_normal_and_optimized(self):
        for optimized in (False, True):
            result = self.run_cli(CERTIFICATE, optimized)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"uniform_charge": "13/12"', result.stdout)

    def test_coordinate_tamper_rejected_normal_and_optimized(self):
        data = self.load()
        data["points_scaled"][0][0] = "-805495/837679"
        path = self.write_mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_conflict_set_tamper_rejected_normal_and_optimized(self):
        data = self.load()
        data["claimed_full_conflict_sets"][0] = [0, 8]
        path = self.write_mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_charge_tamper_rejected_normal_and_optimized(self):
        data = self.load()
        data["claimed_uniform_charge"] = "1"
        path = self.write_mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_boolean_center_rejected(self):
        data = self.load()
        data["claimed_overloaded_center_index"] = True
        path = self.write_mutation(data)
        with self.assertRaises(verifier.VerificationError):
            verifier.verify(path)

    def test_duplicate_key_rejected_normal_and_optimized(self):
        text = CERTIFICATE.read_text(encoding="utf-8")
        text = text.replace(
            '"status": "EXACT_RATIONAL_COUNTEREXAMPLE",',
            '"status": "bad",\\n  "status": "EXACT_RATIONAL_COUNTEREXAMPLE",',
            1,
        )
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        )
        with handle:
            handle.write(text)
        path = Path(handle.name)
        self.addCleanup(path.unlink, missing_ok=True)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)


if __name__ == "__main__":
    unittest.main()
