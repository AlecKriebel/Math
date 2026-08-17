#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python verify_principal_minor_diffusion_ray.py
python verify_symbolic_certificates.py
python verify_improved_profile.py
python frontier_verify_family.py 3 4 5 6 8 10
python frontier_verify_normal_form.py 3
python frontier_verify_pareto.py 3 4 5 6 8 10
python verify_exchange_of_stability.py
python verify_branch_stability.py
echo MINIMAL_VERIFIER_PASS
