#!/usr/bin/env python3

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import verify_known_28


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "known_28_completion.json"
VERIFIER = HERE / "verify_known_28.py"


class Known28VerifierTests(unittest.TestCase):
    def run_cli(self, path, optimized=False):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([str(VERIFIER), str(path)])
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def write_mutation(self, data):
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        )
        with handle:
            json.dump(data, handle)
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return Path(handle.name)

    def load(self):
        with CERTIFICATE.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def test_valid_certificate_normal_and_optimized(self):
        for optimized in (False, True):
            result = self.run_cli(CERTIFICATE, optimized=optimized)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"points": 28', result.stdout)

    def test_tampered_root_rejected_normal_and_optimized(self):
        data = self.load()
        data["roots"][0] = [1, 1, 0, 0, 0]
        path = self.write_mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_tampered_frame_potential_rejected_normal_and_optimized(self):
        data = self.load()
        data["claimed_frame_potential"] = "157"
        path = self.write_mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_boolean_coordinate_rejected(self):
        data = self.load()
        data["roots"][0][0] = True
        path = self.write_mutation(data)
        with self.assertRaises(verify_known_28.VerificationError):
            verify_known_28.verify(path)

    def test_duplicate_key_rejected_normal_and_optimized(self):
        text = CERTIFICATE.read_text(encoding="utf-8")
        text = text.replace(
            '"schema": "kissing5.realized_d5_extension.known28.v1",',
            '"schema": "bad",\\n'
            '  "schema": "kissing5.realized_d5_extension.known28.v1",',
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
