#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_global_flag_exchangeability.py"
INDEPENDENT = HERE / "independent_flag_audit.py"
CERTIFICATE = HERE / "global_flag_exchangeability_certificate.json"
INDEPENDENT_SOURCE = (
    HERE.parent
    / "four_point_depth_projection"
    / "k7_product_audit"
    / "candidate_k7_product_extension.json"
)


class GlobalFlagExchangeabilityTest(unittest.TestCase):
    def run_verifier(self, path, optimized=False, argument=None):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.append(str(path))
        if argument is not None:
            command.append(str(argument))
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_exact_verifier(self):
        report = self.run_verifier(VERIFIER)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["D5_direct_global_square"], "646060")
        self.assertEqual(
            len(report["negative_pseudodistribution_rows"]), 8
        )

    def test_independent_audit(self):
        report = self.run_verifier(INDEPENDENT)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["abstract_sampling_identity"], "PASS")

    def test_optimized_mode_verifiers(self):
        for path in (VERIFIER, INDEPENDENT):
            report = self.run_verifier(path, optimized=True)
            self.assertEqual(report["status"], "PASS")

    def test_optimized_mode_rejects_tamper(self):
        certificate = json.loads(CERTIFICATE.read_text())
        certificate["D5"]["direct_global_square"] = "0"
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            tampered_certificate = temporary_path / "tampered_certificate.json"
            tampered_certificate.write_text(json.dumps(certificate))
            completed = subprocess.run(
                [
                    sys.executable,
                    "-O",
                    str(VERIFIER),
                    str(tampered_certificate),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                completed.returncode,
                0,
                "primary verifier accepted tampering under -O",
            )

            tampered_source = temporary_path / "tampered_source.json"
            tampered_source.write_bytes(INDEPENDENT_SOURCE.read_bytes() + b" ")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-O",
                    str(INDEPENDENT),
                    str(tampered_source),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(
                completed.returncode,
                0,
                "independent audit accepted tampering under -O",
            )


if __name__ == "__main__":
    unittest.main()
