from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_antipodal_deep_graph_branches import (
    DEFAULT_CERTIFICATE,
    VerificationError,
    verify,
)


class AntipodalDeepGraphBranchTests(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["r15_deep_edge_upper"], 41)
        self.assertEqual(result["r16_deep_edge_upper"], 33)
        self.assertEqual(result["r18_deep_edge_upper"], 23)

    def test_tampered_endpoint_is_rejected(self) -> None:
        data = json.loads(DEFAULT_CERTIFICATE.read_text())
        data["branches"][18]["deep_edge_upper"] = 24
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)

    def test_missing_branch_is_rejected(self) -> None:
        data = json.loads(DEFAULT_CERTIFICATE.read_text())
        data["branches"].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(VerificationError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
