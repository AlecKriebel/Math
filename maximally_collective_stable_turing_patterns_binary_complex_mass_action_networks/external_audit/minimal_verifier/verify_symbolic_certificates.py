#!/usr/bin/env python3
"""One-command exact verification of all load-bearing symbolic certificates."""
import subprocess,sys
from pathlib import Path

if not __debug__:
    raise SystemExit(
        "Exact certificate verification requires assertions; "
        "unset PYTHONOPTIMIZE and do not use python -O"
    )

HERE=Path(__file__).resolve().parent
checks=[
 "verify_all_spectrum.py",
 "verify_principal_minor_diffusion_ray.py",
 "verify_network_one_bad_minor.py",
 "dd_verify_order_m_minors.py",
 "dd_verify_diffusion_criterion.py",
 "dd_verify_contrast_bounds.py",
 "dd_verify_mode_isolation.py",
 "dd_verify_harmonic_corrections.py",
 "dd_verify_cubic_sign.py",
 "frontier_verify_determinant_identity.py",
 "frontier_verify_mode_certificates.py",
 "frontier_verify_master_certificate.py",
 "frontier_verify_cubic_bound.py",
 "frontier_verify_exposition_identities.py",
]
for name in checks:
    subprocess.run([sys.executable,str(HERE/name)],check=True)
print("ALL_SYMBOLIC_CERTIFICATES_PASS")
