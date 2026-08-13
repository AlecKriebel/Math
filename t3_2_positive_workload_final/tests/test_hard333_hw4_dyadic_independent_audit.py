from __future__ import annotations

import unittest

import hard333_hw4_dyadic_independent_audit as audit


class Hard333HW4DyadicIndependentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.certificate()

    def test_frozen_candidate_and_note(self) -> None:
        self.assertEqual(
            self.result["audited_candidate_payload_sha256"],
            audit.AUDITED_CANDIDATE_PAYLOAD_SHA256,
        )
        self.assertEqual(
            self.result["audit_note_sha256"], audit.EXPECTED_NOTE_SHA256
        )

    def test_all_strong_orientation_obligations(self) -> None:
        self.assertEqual(self.result["strong_digraphs"], 1606)
        self.assertEqual(
            self.result["orientation_rows_sha256"],
            audit.EXPECTED_ORIENTATION_SHA256,
        )
        histogram = self.result["orientation_histogram"]
        self.assertEqual(sum(histogram.values()), 1606)
        self.assertEqual(
            sum(
                value
                for key, value in histogram.items()
                if "dP=1,dB=1" in key
            ),
            1234,
        )
        self.assertEqual(
            sum(
                value
                for key, value in histogram.items()
                if "dP=0,dB=1" in key
            ),
            186,
        )
        self.assertEqual(
            sum(
                value
                for key, value in histogram.items()
                if "dP=1,dB=0" in key
            ),
            186,
        )

    def test_strict_claim_neutral_verdict(self) -> None:
        self.assertEqual(
            self.result["strict_verdict"],
            "PASS_LOCAL_COMMON_W_STOPPED_EPISODE",
        )
        self.assertTrue(self.result["event_skeleton_replacement_audited"])
        self.assertTrue(self.result["local_service_and_endpoint_audited"])
        self.assertTrue(self.result["canonical_replacement_present"])
        self.assertFalse(self.result["exact_counterexample_found"])
        for key in (
            "dyadic_activation_certified",
            "H_w_4_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])

    def test_payload_frozen(self) -> None:
        self.assertEqual(self.result["payload_sha256"], audit.EXPECTED_PAYLOAD_SHA256)


if __name__ == "__main__":
    unittest.main()
