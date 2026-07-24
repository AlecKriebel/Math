#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class CenteredDegreeTwoRepairTest(unittest.TestCase):
    def run_verifier(self, filename, optimized=False, certificate=None):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.append(str(HERE / filename))
        if certificate is not None:
            command.append(str(certificate))
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_primary_verifier(self):
        report = self.run_verifier("verify_centered_degree2_repair.py")
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["atoms"], 73)
        self.assertEqual(report["centered_kernel_dimension"], 11)
        self.assertEqual(report["full_moment_rank"], 7)
        self.assertEqual(report["quotient_matrix"], "positive definite")

    def test_independent_audit(self):
        report = self.run_verifier(
            "independent_centered_degree2_audit.py"
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(
            report["centered_kernel_radical"], "dimension 11"
        )
        self.assertEqual(report["full_moment_rank"], 7)
        self.assertEqual(
            report["quotient_LDL_pivots"], "all positive"
        )

    def test_optimized_mode_verifiers(self):
        for filename in (
            "verify_centered_degree2_repair.py",
            "independent_centered_degree2_audit.py",
        ):
            report = self.run_verifier(filename, optimized=True)
            self.assertEqual(report["status"], "PASS")

    def test_optimized_mode_rejects_tamper(self):
        data = json.loads(
            (HERE / "centered_degree2_repair_certificate.json").read_text()
        )
        data["atoms"][0]["weight"] = "0"
        with tempfile.TemporaryDirectory() as temporary:
            tampered = Path(temporary) / "tampered_degree2.json"
            tampered.write_text(json.dumps(data))
            for filename in (
                "verify_centered_degree2_repair.py",
                "independent_centered_degree2_audit.py",
            ):
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-O",
                        str(HERE / filename),
                        str(tampered),
                    ],
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(
                    completed.returncode,
                    0,
                    f"{filename} accepted a tampered certificate under -O",
                )


if __name__ == "__main__":
    unittest.main()
