#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../../.." && pwd)"
PYTHON="$PROJECT/../.venv/bin/python"

cd "$PROJECT"
export PYTHONHASHSEED=0

"$PYTHON" "$HERE/reproduce_first_mismatch.py"
"$PYTHON" "$HERE/mutation_tests.py"
"$PYTHON" "$HERE/merger_mutations.py"
"$PYTHON" "$HERE/adversarial_release_review.py"
"$PYTHON" "$HERE/finalize_certificate.py"
"$PYTHON" "$HERE/build_manifest.py"
