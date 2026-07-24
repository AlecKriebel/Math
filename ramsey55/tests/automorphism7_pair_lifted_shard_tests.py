#!/usr/bin/env python3
"""Unit tests for the fail-closed C7 lifted-shard pipeline."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

from pysat.solvers import Glucose3


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT / "src", ROOT / "verify"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_pair_lifted_blocker_sample as lifting  # noqa: E402


class LiftedShardTests(unittest.TestCase):
    def test_shard_73_is_full_size_and_contains_worst_sample(self) -> None:
        indices = [index for index in range(37194) if index % 128 == 73]
        self.assertEqual(len(indices), 291)
        self.assertEqual(indices[0], 73)
        self.assertEqual(indices[-1], 37193)

    def test_all_shards_partition_the_schedule(self) -> None:
        shards = [
            [index for index in range(37194) if index % 128 == shard]
            for shard in range(128)
        ]
        flattened = [index for shard in shards for index in shard]
        self.assertEqual(len(flattened), 37194)
        self.assertEqual(set(flattened), set(range(37194)))
        self.assertEqual({len(shard) for shard in shards}, {290, 291})

    def test_global_selector_definition(self) -> None:
        clauses = lifting.wrapper_clauses(
            ((1,),),
            [2],
            [{"selector": 37323, "side_units": [3, -4]}],
        )
        self.assertEqual(
            clauses,
            (
                (1,),
                (2,),
                (-37323, 3),
                (-37323, -4),
                (37323, -3, 4),
                (37323,),
            ),
        )

    def test_limited_proof_api_produces_unsat_proof(self) -> None:
        with Glucose3(
            bootstrap_with=(
                (1, 2),
                (1, -2),
                (-1, 2),
                (-1, -2),
            ),
            with_proof=True,
        ) as solver:
            solver.conf_budget(10)
            outcome = solver.solve_limited()
            proof = solver.get_proof()
        self.assertFalse(outcome)
        self.assertIsNotNone(proof)
        self.assertEqual(proof[-1], "0")


if __name__ == "__main__":
    unittest.main()
