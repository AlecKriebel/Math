from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from verify_good_167_stream import SplitMix64, replay_trial_state, verify_checkpoint


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "output" / "good_167_stream_smoke.json"
SB_FIXTURE = HERE / "output" / "good_167_stream_sb_smoke.json"


class Good167StreamTests(unittest.TestCase):
    def test_splitmix_and_trial_replay_are_frozen(self) -> None:
        rng = SplitMix64(668)
        self.assertEqual(
            tuple(rng.next() for _ in range(4)),
            (
                0xC33416AAE473D238,
                0x3B8136E0FF77E131,
                0x60589B6AE8406F3F,
                0x58EDD5F5ED8CB9C0,
            ),
        )
        a_mask, b_mask, next_state = replay_trial_state(0xA5A5A5A5A5A5A5A5)
        self.assertEqual(a_mask & 1, 0)
        self.assertEqual(b_mask.bit_count(), 38)
        self.assertNotEqual(next_state, 0xA5A5A5A5A5A5A5A5)

    def test_cpp_checkpoint_matches_python_reducer(self) -> None:
        diagnostics = verify_checkpoint(json.loads(FIXTURE.read_text()))
        self.assertEqual(
            diagnostics,
            {
                "rank": 82,
                "energy": 4768,
                "bad_lags": 66,
                "max_abs_quarter": 20,
            },
        )

    def test_sb_checkpoint_matches_python_reducer(self) -> None:
        diagnostics = verify_checkpoint(json.loads(SB_FIXTURE.read_text()))
        self.assertEqual(
            diagnostics,
            {
                "rank": 82,
                "energy": 5440,
                "bad_lags": 66,
                "max_abs_quarter": 20,
            },
        )

    def test_checkpoint_tampering_is_rejected(self) -> None:
        payload = json.loads(FIXTURE.read_text())
        corrupted = copy.deepcopy(payload)
        corrupted["quarter_residuals"][0] += 1
        with self.assertRaisesRegex(ValueError, "quarter residual vector"):
            verify_checkpoint(corrupted)


if __name__ == "__main__":
    unittest.main()
