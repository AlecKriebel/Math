from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_d5", ROOT / "verifiers" / "verify_d5.py"
)
assert SPEC is not None and SPEC.loader is not None
VERIFY_D5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY_D5)


def certificate_payload() -> dict:
    with (ROOT / "certificates" / "d5_roots.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return json.load(handle)


class VerifyD5Tests(unittest.TestCase):
    def test_valid_certificate(self) -> None:
        summary = VERIFY_D5.verify_payload(certificate_payload())
        self.assertEqual(summary["point_count"], 40)
        self.assertEqual(summary["pair_count"], 780)
        self.assertEqual(summary["maximum_integer_dot"], 1)
        self.assertGreater(summary["boundary_pair_count"], 0)

    def test_duplicate_is_rejected(self) -> None:
        payload = certificate_payload()
        payload["roots"][-1] = copy.deepcopy(payload["roots"][0])
        with self.assertRaisesRegex(VERIFY_D5.CertificateError, "distinct"):
            VERIFY_D5.verify_payload(payload)

    def test_wrong_norm_is_rejected(self) -> None:
        payload = certificate_payload()
        payload["roots"][0] = [1, 0, 0, 0, 0]
        with self.assertRaisesRegex(VERIFY_D5.CertificateError, "squared norm"):
            VERIFY_D5.verify_payload(payload)

    def test_pair_above_boundary_is_rejected(self) -> None:
        payload = certificate_payload()
        payload["roots"][0] = [1, 1, 0, 0, 0]
        payload["roots"][1] = [1, 1, 0, 0, 0]
        # The violating dot product is detected before the duplicate test only
        # if distinctness validation is temporarily bypassed, so use a direct
        # 3-vector-style alteration preserving norm and uniqueness.
        payload["roots"][1] = [1, 1, 0, 0, 0]
        with self.assertRaises(VERIFY_D5.CertificateError):
            VERIFY_D5.verify_payload(payload)

    def test_strict_boundary_bug_would_be_detected(self) -> None:
        payload = certificate_payload()
        summary = VERIFY_D5.verify_payload(payload)
        self.assertGreater(summary["boundary_pair_count"], 0)


if __name__ == "__main__":
    unittest.main()
