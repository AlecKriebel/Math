from __future__ import annotations

import unittest

import hard333_hw4_dyadic_patch_replay as replay


class Hard333HW4DyadicPatchReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = replay.certificate()

    def test_frozen_candidate_and_orientation_rows(self) -> None:
        self.assertEqual(
            self.result["candidate_payload_sha256"],
            replay.EXPECTED_CANDIDATE_PAYLOAD_SHA256,
        )
        self.assertEqual(self.result["orientation_rows"], 1606)

    def test_frozen_bytes(self) -> None:
        files = self.result["frozen_files"]
        self.assertEqual(
            files["canonical_note"], replay.EXPECTED_CANONICAL_NOTE_SHA256
        )
        self.assertEqual(
            files["canonical_source"], replay.EXPECTED_CANONICAL_SOURCE_SHA256
        )
        self.assertEqual(
            files["canonical_test"], replay.EXPECTED_CANONICAL_TEST_SHA256
        )
        self.assertEqual(files["replay_note"], replay.EXPECTED_REPLAY_NOTE_SHA256)

    def test_strict_scope(self) -> None:
        self.assertEqual(
            self.result["strict_verdict"],
            "PASS_LOCAL_COMMON_W_STOPPED_EPISODE",
        )
        self.assertTrue(self.result["local_event_skeleton_audited"])
        self.assertTrue(self.result["local_service_and_endpoint_audited"])
        self.assertFalse(self.result["pair_composition_replayed"])
        self.assertFalse(self.result["H_w_4_pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])

    def test_payload_frozen(self) -> None:
        self.assertEqual(self.result["payload_sha256"], replay.EXPECTED_PAYLOAD_SHA256)


if __name__ == "__main__":
    unittest.main()
