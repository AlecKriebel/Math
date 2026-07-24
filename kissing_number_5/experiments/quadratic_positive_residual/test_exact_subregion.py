from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from experiments.quadratic_positive_residual.verify_exact_subregion import (
    CERTIFICATE,
    VerificationError,
    verify,
)


class ExactSubregionTest(unittest.TestCase):
    def test_endpoint_constants(self) -> None:
        self.assertEqual(verify()["status"], "PASS")

    def test_tampered_certificate_is_rejected(self) -> None:
        data = json.loads(CERTIFICATE.read_text())
        data["epsilon"] = "1/49"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_optimized_mode_normal_and_tamper(self) -> None:
        module = (
            "experiments.quadratic_positive_residual.verify_exact_subregion"
        )
        valid = subprocess.run(
            [sys.executable, "-O", "-m", module],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertIn('"status": "PASS"', valid.stdout)

        data = json.loads(CERTIFICATE.read_text())
        data["epsilon"] = "1/49"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            code = (
                "from pathlib import Path;"
                "from experiments.quadratic_positive_residual."
                "verify_exact_subregion import verify;"
                f"verify(Path({str(path)!r}))"
            )
            tampered = subprocess.run(
                [sys.executable, "-O", "-c", code],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(tampered.returncode, 0)
        self.assertIn("wrong epsilon", tampered.stderr)


if __name__ == "__main__":
    unittest.main()
