#!/usr/bin/env python3
"""External guard for the unchanged assertion-based audit A checker."""
import runpy
import sys
from pathlib import Path

if sys.flags.optimize != 0:
    raise SystemExit('REFUSED: audit A requires normal Python; optimized assertions are unsafe')
root = Path(__file__).resolve().parent
runpy.run_path(str(root / 'audit_a' / 'independent_checks.py'), run_name='__main__')
