#!/bin/sh
set -eu

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3}"
GP_BIN="${GP_BIN:-/opt/homebrew/bin/gp}"

[ -x "$PYTHON_BIN" ] || {
    echo "FAIL missing Python interpreter: $PYTHON_BIN" >&2
    exit 1
}
[ -x "$GP_BIN" ] || {
    echo "FAIL missing PARI/GP interpreter: $GP_BIN" >&2
    exit 1
}

audit_tmp_dir="$(mktemp -d)"
trap 'rm -rf "$audit_tmp_dir"' EXIT HUP INT TERM

"$GP_BIN" -q verify_cube_hostile.gp >"$audit_tmp_dir/exact.out"
grep -F "CUBE_COMPONENT_HOSTILE_EXACT_PASS" "$audit_tmp_dir/exact.out" >/dev/null
cat "$audit_tmp_dir/exact.out"

"$PYTHON_BIN" -u verify_scope.py

if AUDIT_FAULT_INVERSE=1 "$GP_BIN" -q verify_cube_hostile.gp \
    >"$audit_tmp_dir/mutation.out" 2>&1; then
    echo "FAIL inverse-sign mutation was accepted" >&2
    exit 1
fi
if grep -F "CUBE_COMPONENT_HOSTILE_EXACT_PASS" \
    "$audit_tmp_dir/mutation.out" >/dev/null; then
    echo "FAIL inverse-sign mutation reached the terminal marker" >&2
    exit 1
fi
echo "PASS required-failure inverse-sign mutation rejected"

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" verify_scope.py \
    >"$audit_tmp_dir/optimized.out" 2>&1; then
    echo "FAIL optimized Python bypassed the assertion guard" >&2
    exit 1
fi
echo "PASS optimized-Python assertion bypass rejected"

echo "CUBE_COMPONENT_HOSTILE_AUDIT_PASS"
