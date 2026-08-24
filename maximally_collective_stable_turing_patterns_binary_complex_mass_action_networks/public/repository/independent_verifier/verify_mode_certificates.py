#!/usr/bin/env python3
"""Aggregate wrapper for the exact half-plane certificate entrypoints."""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for name in ["dd_verify_mode_isolation.py","frontier_verify_mode_certificates.py"]:
    subprocess.run([sys.executable,str(HERE/name)],check=True)
print("MODE_CERTIFICATES_PASS")
