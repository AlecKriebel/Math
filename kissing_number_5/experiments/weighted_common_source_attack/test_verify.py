from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from verify import CERTIFICATE, verify, verify_row_counterexample


class WeightedCommonSourceTests(unittest.TestCase):
    def test_authentic_certificate(self) -> None:
        self.assertEqual(verify()["status"], "PASS")

    def mutate_and_reject(self, mutation) -> None:
        data = json.loads(CERTIFICATE.read_text())
        mutation(data)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                verify_row_counterexample(path)

    def test_rejects_nonunit_point(self) -> None:
        self.mutate_and_reject(
            lambda data: data["points"][1].__setitem__(0, "0")
        )

    def test_rejects_false_claimed_maximum(self) -> None:
        self.mutate_and_reject(
            lambda data: data.__setitem__(
                "claimed_exact_maximum_inner_product", "0"
            )
        )

    def test_rejects_false_claimed_energy(self) -> None:
        self.mutate_and_reject(
            lambda data: data.__setitem__(
                "claimed_exact_anchor_row_energy", "9"
            )
        )


if __name__ == "__main__":
    unittest.main()
