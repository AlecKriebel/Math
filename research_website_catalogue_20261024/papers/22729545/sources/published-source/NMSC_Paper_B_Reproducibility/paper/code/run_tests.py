#!/usr/bin/env python3
"""Compatibility entry point for the skip-aware exact-suite runner."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
runner = ROOT / "scripts" / "run_exact_suite.py"
completed = subprocess.run([sys.executable, str(runner)], cwd=ROOT, check=False)
if completed.returncode:
    raise SystemExit(completed.returncode)
print("ALL_EXACT_CLOUD_TESTS_PASSED_WITH_SKIP_CONTRACT")
