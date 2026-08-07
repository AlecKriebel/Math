#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
python3 "$ROOT/reproducibility/verify_integrity.py"
python3 "$ROOT/reproducibility/publication/src/verify_multitriangle_exclusion.py"
python3 "$ROOT/reproducibility/verify_base_release_attestation.py"
python3 "$ROOT/reproducibility/publication/review/review_publication_release.py"
bash "$ROOT/reproducibility/build_paper.sh"
python3 "$ROOT/reproducibility/build_component_archives.py"
python3 "$ROOT/reproducibility/publication/review/review_submission_package.py"
python3 "$ROOT/reproducibility/verify_integrity.py"
echo 'AUTHOR-READY QUICK VERIFICATION PASSED'
