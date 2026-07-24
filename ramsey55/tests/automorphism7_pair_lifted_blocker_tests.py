#!/usr/bin/env python3
"""Unit tests for selector-guarded order-7 cube-proof lifting."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT / "src", ROOT / "verify"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_pair_lifted_blocker_sample as lifting  # noqa: E402


class LiftedBlockerTests(unittest.TestCase):
    def test_mock_proof_is_guarded_cleaned_and_rederived(self) -> None:
        proof = ["1 -2 0", "d 1 -2 0", "3 0", "0"]
        blocker = (-7, 8)
        payload, record = lifting.lift_proof_segment(
            proof, selector=130, blocker=blocker
        )
        self.assertEqual(record["raw_deletion_record_count"], 1)
        self.assertEqual(record["raw_addition_record_count"], 3)
        self.assertEqual(record["guarded_addition_count"], 3)
        self.assertEqual(
            payload.decode("ascii").splitlines(),
            [
                "1 -2 -130 0",
                "3 -130 0",
                "-130 0",
                "-7 8 0",
                "d 1 -2 -130 0",
                "d 3 -130 0",
                "d -130 0",
                "-130 0",
            ],
        )

    def test_wrapper_contains_exact_selector_definition(self) -> None:
        base = ((1, 2), (-1, 3))
        samples = [
            {
                "selector": 130,
                "side_units": [4, -5],
            },
            {
                "selector": 131,
                "side_units": [-6, 7],
            },
        ]
        observed = lifting.wrapper_clauses(base, [8, -9], samples)
        self.assertEqual(
            observed,
            (
                (1, 2),
                (-1, 3),
                (8,),
                (-9,),
                (-130, 4),
                (-130, -5),
                (130, -4, 5),
                (-131, -6),
                (-131, 7),
                (131, 6, -7),
                (130, 131),
            ),
        )

    def test_clause_record_round_trip(self) -> None:
        for deletion in (False, True):
            record = lifting.clause_record((4, -9, 12), deletion=deletion)
            self.assertEqual(
                lifting.parse_proof_record(record),
                (deletion, (4, -9, 12)),
            )


if __name__ == "__main__":
    unittest.main()
