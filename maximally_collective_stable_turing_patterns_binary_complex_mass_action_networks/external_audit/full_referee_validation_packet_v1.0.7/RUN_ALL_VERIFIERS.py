#!/usr/bin/env python3
"""Run every verifier entrypoint supplied in the portable repository."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import time


EXPECTED = [
    "dd_verify_contrast_bounds.py",
    "dd_verify_critical_profile.py",
    "dd_verify_cubic_sign.py",
    "dd_verify_diffusion_criterion.py",
    "dd_verify_harmonic_corrections.py",
    "dd_verify_mode_isolation.py",
    "dd_verify_order_m_minors.py",
    "dd_verify_stable_contrast.py",
    "frontier_verify_cubic_bound.py",
    "frontier_verify_determinant_identity.py",
    "frontier_verify_exposition_identities.py",
    "frontier_verify_family.py",
    "frontier_verify_master_certificate.py",
    "frontier_verify_mode_certificates.py",
    "frontier_verify_near_threshold.py",
    "frontier_verify_normal_form.py",
    "frontier_verify_pareto.py",
    "frontier_verify_pareto_curve.py",
    "verify_all_spectrum.py",
    "verify_branch_stability.py",
    "verify_contrast_bounds.py",
    "verify_critical_profile.py",
    "verify_cubic_sign.py",
    "verify_current_numerical_provenance.py",
    "verify_diffusion_criterion.py",
    "verify_exchange_of_stability.py",
    "verify_family.py",
    "verify_harmonic_corrections.py",
    "verify_improved_profile.py",
    "verify_mode_certificates.py",
    "verify_mode_isolation.py",
    "verify_network_one_bad_minor.py",
    "verify_order_m_minors.py",
    "verify_pareto_family.py",
    "verify_principal_minor_diffusion_ray.py",
    "verify_realization_space.py",
    "verify_stable_contrast.py",
    "verify_symbolic_certificates.py",
]


def main() -> None:
    if not __debug__:
        raise SystemExit("Assertions are disabled; do not use python -O")

    packet = Path(__file__).resolve().parent
    repository = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else packet / "repository"
    verifier = repository / "independent_verifier"
    if not verifier.is_dir():
        raise SystemExit(f"Verifier directory not found: {verifier}")

    patterns = ("verify_*.py", "dd_verify_*.py", "frontier_verify_*.py")
    actual = sorted({path.name for pattern in patterns for path in verifier.glob(pattern)})
    if actual != EXPECTED:
        missing = sorted(set(EXPECTED) - set(actual))
        unexpected = sorted(set(actual) - set(EXPECTED))
        raise SystemExit(
            "Verifier inventory mismatch\n"
            f"missing={missing}\n"
            f"unexpected={unexpected}"
        )

    env = os.environ.copy()
    env.update(
        {
            "PYTHONOPTIMIZE": "0",
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
            "MPLBACKEND": "Agg",
            "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "VECLIB_MAXIMUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1",
        }
    )

    started = time.perf_counter()
    for index, name in enumerate(EXPECTED, start=1):
        command = [sys.executable, str(verifier / name)]
        print(f"[{index:02d}/{len(EXPECTED)}] RUN {' '.join(command)}", flush=True)
        one_start = time.perf_counter()
        subprocess.run(command, cwd=repository, env=env, check=True)
        elapsed = time.perf_counter() - one_start
        print(f"[{index:02d}/{len(EXPECTED)}] PASS {name} ({elapsed:.3f}s)", flush=True)

    elapsed = time.perf_counter() - started
    print(f"ALL_38_VERIFIER_ENTRYPOINTS_PASS ({elapsed:.3f}s)")


if __name__ == "__main__":
    main()
