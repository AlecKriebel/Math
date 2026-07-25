#!/usr/bin/env python3

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import verify_small_union_hall


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "small_union_hall_certificate.json"
VERIFIER = HERE / "verify_small_union_hall.py"


class SmallUnionHallVerifierTests(unittest.TestCase):
    def run_cli(self, path, optimized=False):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend((str(VERIFIER), str(path)))
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def load(self):
        return json.loads(CERTIFICATE.read_text(encoding="utf-8"))

    def mutation(self, data):
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        )
        with handle:
            json.dump(data, handle)
        path = Path(handle.name)
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_valid_normal_and_optimized(self):
        for optimized in (False, True):
            result = self.run_cli(CERTIFICATE, optimized)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"proved_hall_union_size": 3', result.stdout)

    def test_tampered_pair_count_rejected_normal_and_optimized(self):
        data = self.load()
        data["pair_signature_counts"]["1,1"] = 239
        path = self.mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_tampered_triangle_rejected_normal_and_optimized(self):
        data = self.load()
        data["coordinate_cycle_triples"][0] = [0, 8, 13]
        path = self.mutation(data)
        for optimized in (False, True):
            self.assertNotEqual(self.run_cli(path, optimized).returncode, 0)

    def test_tampered_stabilizer_rejected(self):
        data = self.load()
        data["support_stabilizer_order"] = 15
        path = self.mutation(data)
        with self.assertRaises(verify_small_union_hall.VerificationError):
            verify_small_union_hall.verify(path)

    def test_boolean_integer_rejected(self):
        data = self.load()
        data["proved_hall_union_size"] = True
        path = self.mutation(data)
        with self.assertRaises(verify_small_union_hall.VerificationError):
            verify_small_union_hall.verify(path)

    def test_duplicate_key_rejected_normal_and_optimized(self):
        text = CERTIFICATE.read_text(encoding="utf-8")
        text = text.replace(
            '"support_stabilizer_order": 16,',
            '"support_stabilizer_order": 15,\\n'
            '  "support_stabilizer_order": 16,',
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
