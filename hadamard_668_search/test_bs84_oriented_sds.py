"""Regression tests for the prime-83 oriented-SDS verifier."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from verify_bs84_oriented_sds import (
    canonical_profiles,
    goethals_seidel,
    verify_hadamard,
    verify_payload,
)


HERE = Path(__file__).resolve().parent
CHECKPOINT = HERE / "output/bs84_oriented_sds_local_p19.json"


class OrientedSdsVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(CHECKPOINT.read_text(encoding="utf-8"))

    def test_canonical_profile_catalog(self) -> None:
        profiles = canonical_profiles()
        self.assertEqual(len(profiles), 45)
        self.assertEqual(profiles[19], (37, 37, 35, 41))
        self.assertEqual(len(set(profiles)), len(profiles))

    def test_retained_checkpoint_replays(self) -> None:
        result = verify_payload(self.payload, allow_checkpoint=True)
        self.assertTrue(result["checkpoint_verified"])
        self.assertFalse(result["prime_fold_verified"])
        self.assertEqual(result["quarter_energy"], 14)
        self.assertEqual(result["bad_independent_lags"], 11)
        self.assertFalse(result["hadamard_verified"])

    def test_nonexact_checkpoint_is_rejected_by_default(self) -> None:
        with self.assertRaisesRegex(ValueError, "format must be"):
            verify_payload(self.payload)

    def test_paf_tamper_is_detected(self) -> None:
        tampered = copy.deepcopy(self.payload)
        tampered["periodic_paf_sum"][2] += 4
        with self.assertRaisesRegex(ValueError, "periodic_paf_sum"):
            verify_payload(tampered, allow_checkpoint=True)

    def test_energy_tamper_is_detected(self) -> None:
        tampered = copy.deepcopy(self.payload)
        tampered["quarter_energy"] = 12
        with self.assertRaisesRegex(ValueError, "quarter_energy"):
            verify_payload(tampered, allow_checkpoint=True)

    def test_dependency_free_goethals_seidel_kernel(self) -> None:
        matrix = goethals_seidel(((1,), (1,), (1,), (1,)))
        self.assertEqual(len(matrix), 4)
        verify_hadamard(matrix)


if __name__ == "__main__":
    unittest.main()
