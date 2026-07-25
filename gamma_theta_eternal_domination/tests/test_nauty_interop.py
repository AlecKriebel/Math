from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import BitGraph  # noqa: E402


class NautyGraph6Interop(unittest.TestCase):
    def test_connected_unlabeled_graph6_through_order_seven(self) -> None:
        geng = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
        if not geng.exists():
            self.skipTest("run tools/bootstrap_nauty.sh first")
        expected = {1: 1, 2: 1, 3: 2, 4: 6, 5: 21, 6: 112, 7: 853}
        for n, count in expected.items():
            completed = subprocess.run(
                [str(geng), "-cq", str(n)],
                check=True,
                capture_output=True,
                text=True,
            )
            records = completed.stdout.splitlines()
            self.assertEqual(len(records), count)
            for record in records:
                graph = BitGraph.from_graph6(record)
                self.assertEqual(graph.n, n)
                self.assertEqual(graph.to_graph6(), record)


if __name__ == "__main__":
    unittest.main()
