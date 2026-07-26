#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON=/Users/alec/Documents/Math/.venv/bin/python

if [ ! -x "$PYTHON" ]; then
    echo "FAIL: expected project Python is unavailable: $PYTHON" >&2
    exit 1
fi

OUTPUT=$("$PYTHON" "$SCRIPT_DIR/hostile_verify.py" 2>&1)
printf '%s\n' "$OUTPUT"
printf '%s\n' "$OUTPUT" | grep -Fqx \
    'D4_DN3_HOSTILE_FULL_E6_CONTACT_ATLAS_PASS'

OPTIMIZED_OUTPUT_FILE=$(mktemp)
trap 'rm -f "$OPTIMIZED_OUTPUT_FILE"' EXIT HUP INT TERM
if "$PYTHON" -O "$SCRIPT_DIR/hostile_verify.py" >"$OPTIMIZED_OUTPUT_FILE" 2>&1; then
    echo "FAIL: optimized Python unexpectedly passed" >&2
    cat "$OPTIMIZED_OUTPUT_FILE" >&2
    exit 1
fi
grep -Fq 'FAIL: assertions disabled' "$OPTIMIZED_OUTPUT_FILE"

echo "D4_DN3_HOSTILE_AUDIT_STRICT_PASS"
