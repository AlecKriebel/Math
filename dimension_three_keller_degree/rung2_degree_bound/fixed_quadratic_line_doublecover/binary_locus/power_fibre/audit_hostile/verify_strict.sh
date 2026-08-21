#!/bin/sh
set -eu

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3}"
GP_BIN="${GP_BIN:-/opt/homebrew/bin/gp}"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "FAIL missing Python interpreter: $PYTHON_BIN" >&2
    exit 1
fi
if [ ! -x "$GP_BIN" ]; then
    echo "FAIL missing PARI/GP interpreter: $GP_BIN" >&2
    exit 1
fi

audit_tmp_dir="$(mktemp -d)"
trap 'rm -rf "$audit_tmp_dir"' EXIT HUP INT TERM

"$GP_BIN" -q verify_hostile_pari.gp >"$audit_tmp_dir/pari.out"
grep -F "ALL HOSTILE PARI ALGEBRA CHECKS PASSED" "$audit_tmp_dir/pari.out" >/dev/null
cat "$audit_tmp_dir/pari.out"

"$PYTHON_BIN" -u verify_structure.py
"$PYTHON_BIN" -u verify_frozen_bridge.py

run_gp_fault() {
    fault_name="$1"
    environment_name="$2"
    output="$audit_tmp_dir/${fault_name}.out"
    if env "${environment_name}=1" "$GP_BIN" -q verify_hostile_pari.gp \
        >"$output" 2>&1; then
        echo "FAIL ${fault_name} mutation was accepted" >&2
        exit 1
    fi
    if grep -F "ALL HOSTILE PARI ALGEBRA CHECKS PASSED" "$output" >/dev/null; then
        echo "FAIL ${fault_name} mutation reached the terminal marker" >&2
        exit 1
    fi
    echo "PASS required-failure mutation rejected: ${fault_name}"
}

run_gp_fault "sign" "AUDIT_FAULT_SIGN"
run_gp_fault "coefficient" "AUDIT_FAULT_COEFF"
run_gp_fault "orbit_normalization" "AUDIT_FAULT_ORBIT"

if "$PYTHON_BIN" verify_structure.py --fault-orbit \
    >"$audit_tmp_dir/orbit_python.out" 2>&1; then
    echo "FAIL independent orbit-action mutation was accepted" >&2
    exit 1
fi
echo "PASS independent orbit-action mutation rejected"

for script in verify_structure.py verify_frozen_bridge.py; do
    if PYTHONOPTIMIZE=1 "$PYTHON_BIN" "$script" \
        >"$audit_tmp_dir/optimized.out" 2>&1; then
        echo "FAIL optimized Python bypassed assertion guard in $script" >&2
        exit 1
    fi
done
echo "PASS optimized-Python assertion bypass rejected"

echo "ALL POWER-FIBRE HOSTILE AUDIT CHECKS PASSED"
