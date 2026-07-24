from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from verify_scalar_extension_countermodel import CERTIFICATE, verify


class ScalarExtensionCountermodelTests(unittest.TestCase):
    def test_authentic_certificate(self) -> None:
        self.assertEqual(verify()["status"], "PASS")

    def mutate_and_reject(self, mutation) -> None:
        data = json.loads(CERTIFICATE.read_text())
        mutation(data)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                verify(path)

    def test_rejects_bad_profile_moment(self) -> None:
        self.mutate_and_reject(
            lambda data: data["profiles"].__setitem__(
                0, "+" + data["profiles"][0][1:]
            )
        )

    def test_rejects_duplicate(self) -> None:
        self.mutate_and_reject(
            lambda data: data["profiles"].__setitem__(
                1, data["profiles"][0]
            )
        )

    def test_rejects_false_rank(self) -> None:
        self.mutate_and_reject(
            lambda data: data.__setitem__("claimed_profile_rank", 5)
        )


if __name__ == "__main__":
    unittest.main()
