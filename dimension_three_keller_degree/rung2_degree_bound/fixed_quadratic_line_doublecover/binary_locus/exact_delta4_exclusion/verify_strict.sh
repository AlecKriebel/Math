#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
reconciliation_dir="$certificate_dir/../../delta_ge3_reconciliation"
manifest_output=$(mktemp "${TMPDIR:-/tmp}/exact-delta4-manifest.XXXXXX")
fault_output=$(mktemp "${TMPDIR:-/tmp}/exact-delta4-manifest-fault.XXXXXX")
reconciliation_output=$(mktemp "${TMPDIR:-/tmp}/exact-delta4-reconcile.XXXXXX")
family_output=$(mktemp "${TMPDIR:-/tmp}/exact-delta4-family.XXXXXX")
plan_output=$(mktemp "${TMPDIR:-/tmp}/exact-delta4-plan.XXXXXX")
trap 'rm -f "$manifest_output" "$fault_output" "$reconciliation_output" "$family_output" "$plan_output"' EXIT HUP INT TERM

"$python_bin" "$certificate_dir/verify_manifest.py" >"$manifest_output" 2>&1
cat "$manifest_output"
grep -Fx "EXACT_DELTA4_MANIFEST_PASS_6_OF_6_CANONICAL_19_6_1" \
    "$manifest_output" >/dev/null

if EXACT_DELTA4_MANIFEST_FAULT=drop-family \
    "$python_bin" "$certificate_dir/verify_manifest.py" >"$fault_output" 2>&1; then
    cat "$fault_output"
    echo "FAIL: missing-family mutation was accepted" >&2
    exit 1
fi
grep -F "manifest does not contain six families" "$fault_output" >/dev/null

if "$python_bin" -O "$certificate_dir/verify_manifest.py" >"$fault_output" 2>&1; then
    echo "FAIL: optimized manifest verifier was accepted" >&2
    exit 1
fi
grep -F "FAIL: assertions disabled" "$fault_output" >/dev/null

if ! PYTHON_BIN="$python_bin" sh "$reconciliation_dir/verify_strict.sh" \
    >"$reconciliation_output" 2>&1; then
    cat "$reconciliation_output"
    exit 1
fi
cat "$reconciliation_output"
grep -Fx "DELTA_GE3_RECONCILIATION_STRICT_PASS_26" \
    "$reconciliation_output" >/dev/null

run_family() {
    family_dir=$1
    expected_marker=$2
    : >"$family_output"
    if ! (cd "$certificate_dir/$family_dir" && sh verify_strict.sh) \
        >"$family_output" 2>&1; then
        cat "$family_output"
        exit 1
    fi
    cat "$family_output"
    grep -Fx "$expected_marker" "$family_output" >/dev/null
}

"$python_bin" "$certificate_dir/verify_manifest.py" --emit-plan >"$plan_output"
while IFS='|' read -r family_dir expected_marker; do
    test -n "$family_dir"
    test -n "$expected_marker"
    run_family "$family_dir" "$expected_marker"
done <"$plan_output"

printf '%s\n' "EXACT_DELTA4_SIX_FAMILY_EXCLUSION_STRICT_PASS"
