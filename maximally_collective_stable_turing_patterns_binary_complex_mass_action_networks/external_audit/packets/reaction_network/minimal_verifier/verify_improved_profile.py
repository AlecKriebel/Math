#!/usr/bin/env python3
"""Aggregate wrapper for the improved-profile verifier layers.

This entrypoint adds no independent evidence beyond its child scripts.
"""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for name in [
 "dd_verify_critical_profile.py",
 "dd_verify_mode_isolation.py",
 "dd_verify_harmonic_corrections.py",
 "dd_verify_cubic_sign.py",
 "dd_verify_stable_contrast.py",
]:
    subprocess.run([sys.executable,str(HERE/name)],check=True)
print("IMPROVED_PROFILE_PASS")
