#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python src/verify_root_zipper_structure.py >/dev/null
python src/verify_cleanup_jc.py >/dev/null
python review/independent_cleanup_model.py >/dev/null
python reproducibility/verify_release.py
printf 'CONVENTION-CLOSURE QUICK VERIFICATION PASSED\n'
