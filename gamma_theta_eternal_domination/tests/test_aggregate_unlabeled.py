from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.aggregate_unlabeled import aggregate_logs  # noqa: E402


class AggregateUnlabeledTests(unittest.TestCase):
    def _write_shard(
        self, root: Path, residue: int, *, status: str = "complete"
    ) -> Path:
        path = root / f"shard-{residue}.json"
        payload = {
            "status": status,
            "configuration": {
                "order": 4,
                "residue": residue,
                "modulus": 2,
                "connected_only": True,
                "check_all_guard_counts": True,
                "generator_command": [
                    "/pinned/geng",
                    "-cq",
                    "4",
                    f"{residue}/2",
                ],
            },
            "processed": 3,
            "counters": {
                "graphs": 3,
                "gamma_equals_gamma_infinity_less_than_theta": 0,
            },
            "parameter_histogram": {"1,1,1,1,1": 3},
            "nauty_archive_sha256": "a" * 64,
            "graph_stream_sha256": f"{residue + 1:064x}",
            "outcome": "all A/B comparisons agreed",
        }
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_complete_partition_aggregates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = tuple(self._write_shard(root, residue) for residue in range(2))
            result = aggregate_logs(
                paths, order=4, modulus=2, expected_count=6
            )
            self.assertEqual(result["coverage"]["processed"], 6)
            self.assertEqual(result["coverage"]["residues"], [0, 1])
            self.assertEqual(result["counters"]["graphs"], 6)

    def test_incomplete_or_misassigned_shard_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = [self._write_shard(root, residue) for residue in range(2)]
            payload = json.loads(paths[1].read_text(encoding="utf-8"))
            payload["configuration"]["residue"] = 0
            paths[1].write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                aggregate_logs(paths, order=4, modulus=2)
            paths[1] = self._write_shard(root, 1, status="running")
            with self.assertRaises(ValueError):
                aggregate_logs(paths, order=4, modulus=2)


if __name__ == "__main__":
    unittest.main()
