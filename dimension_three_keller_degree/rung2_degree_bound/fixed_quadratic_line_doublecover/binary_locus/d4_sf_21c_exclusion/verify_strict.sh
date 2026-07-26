#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
keller_python=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
keller_gp=${KELLER_GP:-gp}
sympy_output=$(mktemp)
pari_output=$(mktemp)
optimized_output=$(mktemp)
pari_fault_script=$(mktemp)
pari_fault_output=$(mktemp)
trap 'rm -f "$sympy_output" "$pari_output" "$optimized_output" "$pari_fault_script" "$pari_fault_output"' EXIT HUP INT TERM

cd "$certificate_dir"

"$keller_python" -u verify_exclusion_sympy.py | tee "$sympy_output"
grep -Fx "D4_SF_21C_SYMPY_STRICT_PASS" "$sympy_output" >/dev/null

if "$keller_python" -O verify_exclusion_sympy.py >"$optimized_output" 2>&1; then
  echo "FAIL: optimized Python was accepted" >&2
  exit 1
fi
grep -F "FAIL: assertions disabled" "$optimized_output" >/dev/null

"$keller_gp" -q -s 512M verify_exclusion_pari.gp 2>&1 | tee "$pari_output"
grep -Fx "D4_SF_21C_PARI_STRICT_PASS" "$pari_output" >/dev/null
if grep -E '^[[:space:]]*\*\*\*' "$pari_output" >/dev/null; then
  echo "FAIL: PARI/GP reported an error" >&2
  exit 1
fi

sed 's/+ 108\/5,/+ 107\/5,/' verify_exclusion_pari.gp >"$pari_fault_script"
"$keller_gp" -q -s 512M "$pari_fault_script" >"$pari_fault_output" 2>&1 || true
if grep -Fx "D4_SF_21C_PARI_STRICT_PASS" "$pari_fault_output" >/dev/null; then
  echo "FAIL: mutated PARI/GP certificate was accepted" >&2
  exit 1
fi
grep -E '^[[:space:]]*\*\*\*' "$pari_fault_output" >/dev/null

echo "D4_SF_21C_FULL_STRICT_PASS"
