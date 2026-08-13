"""Regression tests for the exact 11,842 top-S/top-D identity."""

from __future__ import annotations

import unittest

import no_failure_11842_top_s_top_d_certificate as target


class TopSTopDCertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = target.certificate()

    def test_dependencies_are_exact(self) -> None:
        self.assertEqual(
            target.dependency_sha256(),
            target.EXPECTED_DEPENDENCY_SHA256,
        )

    def test_exact_family(self) -> None:
        self.assertEqual(self.result["pairs"], 11_842)
        self.assertEqual(
            self.result["pair_sha256"],
            target.remainder.EXPECTED_NO_FAILURE_PAIR_SHA256,
        )

    def test_every_feasible_descriptor_passes_the_corrected_cut(self) -> None:
        self.assertGreater(self.result["feasible_incidences"], 0)
        self.assertEqual(self.result["corrected_cut_failures"], 0)

    def test_top_s_is_nonempty_and_globally_top_d(self) -> None:
        self.assertEqual(self.result["empty_top_s"], 0)
        self.assertEqual(self.result["top_s_not_subset_global_top_d"], 0)

    def test_fingerprints_are_pinned(self) -> None:
        self.assertEqual(
            self.result["feasible_incidence_sha256"],
            target.EXPECTED_FEASIBLE_INCIDENCE_SHA256,
        )
        self.assertEqual(
            self.result["top_identity_sha256"],
            target.EXPECTED_TOP_IDENTITY_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
