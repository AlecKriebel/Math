#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
keller_python=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
keller_gp=${KELLER_GP:-gp}
sympy_output=$(mktemp "${TMPDIR:-/tmp}/d4-sf20cc-sympy.XXXXXX")
optimized_output=$(mktemp "${TMPDIR:-/tmp}/d4-sf20cc-opt.XXXXXX")
pari_output=$(mktemp "${TMPDIR:-/tmp}/d4-sf20cc-pari.XXXXXX")
pari_fault_script=$(mktemp "${TMPDIR:-/tmp}/d4-sf20cc-fault.XXXXXX")
pari_fault_output=$(mktemp "${TMPDIR:-/tmp}/d4-sf20cc-fault-out.XXXXXX")
trap 'rm -f "$sympy_output" "$optimized_output" "$pari_output" "$pari_fault_script" "$pari_fault_output"' EXIT HUP INT TERM

cd "$certificate_dir"

"$keller_python" -u verify_exclusion_sympy.py | tee "$sympy_output"
grep -Fx 'D4_SF_20CC_SYMPY_STRICT_PASS' "$sympy_output" >/dev/null

if "$keller_python" -O verify_exclusion_sympy.py >"$optimized_output" 2>&1; then
    echo 'FAIL: optimized Python was accepted' >&2
    exit 1
fi
grep -F 'FAIL: assertions disabled' "$optimized_output" >/dev/null

if ! "$keller_gp" -s 128000000 -q verify_exclusion_pari.gp >"$pari_output" 2>&1; then
    cat "$pari_output"
    exit 1
fi
cat "$pari_output"
if grep -q '\*\*\*' "$pari_output"; then
    exit 1
fi
grep -Fx 'D4_SF_20CC_PARI_HOSTILE_EXCLUSION_PASS' "$pari_output" >/dev/null

sed 's/c3(E5done,2,1,2)-9\*kk\^3/c3(E5done,2,1,2)-8*kk^3/' \
    verify_exclusion_pari.gp >"$pari_fault_script"
"$keller_gp" -s 128000000 -q "$pari_fault_script" >"$pari_fault_output" 2>&1 || true
if ! grep -q '\*\*\*' "$pari_fault_output"; then
    echo 'FAIL: mutated PARI/GP obstruction produced no diagnostic' >&2
    exit 1
fi

printf '%s\n' 'D4_SF_20CC_FULL_STRICT_PASS'
