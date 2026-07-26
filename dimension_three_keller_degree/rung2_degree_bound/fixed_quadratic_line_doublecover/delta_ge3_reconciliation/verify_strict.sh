#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}

PYTHON_BIN="$PYTHON_BIN" "$HERE/../binary_locus/delta_ge3_universal/verify_all_strict.sh"
"$HERE/../audit_delta_ge3_denominator/verify_strict.sh"
"$PYTHON_BIN" "$HERE/verify_reconciliation.py"
"$PYTHON_BIN" "$HERE/verify_freeze.py"

echo "DELTA_GE3_RECONCILIATION_STRICT_PASS_26"
