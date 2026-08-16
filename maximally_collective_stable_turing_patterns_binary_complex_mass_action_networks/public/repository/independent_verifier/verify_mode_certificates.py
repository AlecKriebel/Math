#!/usr/bin/env python3
"""Verify every exact half-plane coefficient certificate used in the paper."""
import subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for name in ["dd_verify_mode_isolation.py","frontier_verify_mode_certificates.py"]:
    subprocess.run([sys.executable,str(HERE/name)],check=True)
print("MODE_CERTIFICATES_PASS")
