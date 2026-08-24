#!/usr/bin/env python3
"""Aggregate exact checks for the equilibrium-scaled stable trade-off family.

All-dimensional claims are checked by the coefficient and comparison
certificates.  Direct symbolic matrix regressions are intentionally limited to
small representative dimensions so the public replay remains tractable.
This aggregate wrapper adds no independent evidence beyond its child scripts.
"""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
checks=[
 ("frontier_verify_family.py", []),
 ("frontier_verify_determinant_identity.py", []),
 ("frontier_verify_mode_certificates.py", []),
 ("frontier_verify_master_certificate.py", []),
 ("frontier_verify_cubic_bound.py", []),
 ("frontier_verify_normal_form.py", ["3","4"]),
 ("frontier_verify_pareto.py", []),
 ("frontier_verify_pareto_curve.py", ["3","4"]),
]
for name,args in checks:
    subprocess.run([sys.executable,str(HERE/name),*args],check=True)
print("PARETO_FAMILY_PASS")
