import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Fixed41RankMixtureSeparatorTest(unittest.TestCase):
    def test_exact_separator(self):
        script = ROOT / "verifiers" / "verify_fixed41_rank_mixture_separator.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(ROOT),
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)
        self.assertIn("every theta>0 fails", result.stdout)


if __name__ == "__main__":
    unittest.main()
