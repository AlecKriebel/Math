#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."
PYTHON="${PYTHON:-../.venv/bin/python}"
REVIEW="reviews/compact_probe_format/final_n4_cleanroom"

"$PYTHON" -m py_compile \
  "$REVIEW/engine.py" \
  "$REVIEW/audit_final_n4.py" \
  "$REVIEW/mutation_tests.py" \
  "$REVIEW/merger_mutations.py" \
  "$REVIEW/finalize_certificate.py"
"$PYTHON" "$REVIEW/finalize_certificate.py"
