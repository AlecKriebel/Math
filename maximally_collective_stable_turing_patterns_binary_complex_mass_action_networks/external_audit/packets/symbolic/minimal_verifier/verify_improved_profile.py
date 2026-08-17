#!/usr/bin/env python3
"""Aggregate exact checks for the improved unit-equilibrium stable design."""
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
