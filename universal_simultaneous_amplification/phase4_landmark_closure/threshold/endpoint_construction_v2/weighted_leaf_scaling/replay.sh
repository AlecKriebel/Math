#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../../../.." && pwd)

"$ROOT/.venv/bin/python" "$HERE/verify_weighted_leaf_coefficients.py"
"$ROOT/.venv/bin/python" "$HERE/verify_weighted_leaf_lumping.py"
OPENBLAS_NUM_THREADS=1 "$ROOT/.venv/bin/python" \
  "$HERE/audit_weighted_leaf_convergence.py"

