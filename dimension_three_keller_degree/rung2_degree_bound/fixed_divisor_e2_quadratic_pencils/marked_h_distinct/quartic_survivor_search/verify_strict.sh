#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
task_python=${TASK_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
repo_root=$(git -C "$script_dir" rev-parse --show-toplevel)

if [ ! -x "$task_python" ]; then
  echo "FAIL: SymPy interpreter not executable: $task_python" >&2
  exit 2
fi
if ! command -v gp >/dev/null 2>&1; then
  echo "FAIL: gp is required" >&2
  exit 2
fi

sympy_out=$(mktemp)
pari_out=$(mktemp)
modular_out=$(mktemp)
endpoints_sympy_out=$(mktemp)
endpoints_pari_out=$(mktemp)
manifest_out=$(mktemp)
trap 'rm -f "$sympy_out" "$pari_out" "$modular_out" "$endpoints_sympy_out" "$endpoints_pari_out" "$manifest_out"' EXIT HUP INT TERM

(
  cd "$repo_root"
  shasum -a 256 -c "$script_dir/INPUT_MANIFEST.sha256"
) >"$manifest_out" 2>&1
if grep -Eq 'FAILED|No such file|cannot open' "$manifest_out"; then
  cat "$manifest_out"
  exit 1
fi
grep -Fq 'FROZEN_Q2_E2_MARKED_COMPANION_v1.md: OK' "$manifest_out"
grep -Fq 'verify_tau_family_sympy.py: OK' "$manifest_out"

"$task_python" "$script_dir/derive_ctau_e5_obstruction_sympy.py" >"$sympy_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)|Traceback|AssertionError' "$sympy_out"; then
  cat "$sympy_out"
  exit 1
fi
grep -Fxq 'CTAU_E5_SYMPY_PASS_6C1D4A' "$sympy_out"

gp -q "$script_dir/verify_ctau_e5_obstruction_pari.gp" >"$pari_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)' "$pari_out" || grep -Fq '***' "$pari_out"; then
  cat "$pari_out"
  exit 1
fi
grep -Fxq 'CTAU_E5_PARI_PASS_91B027' "$pari_out"

"$task_python" -S "$script_dir/scan_ctau_modular.py" >"$modular_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)|Traceback|AssertionError' "$modular_out"; then
  cat "$modular_out"
  exit 1
fi
grep -Fq 'CTAU_MODULAR_SCAN_PASS_44DA09' "$modular_out"

"$task_python" "$script_dir/derive_six_endpoints_e5_e4_sympy.py" >"$endpoints_sympy_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)|Traceback|AssertionError' "$endpoints_sympy_out"; then
  cat "$endpoints_sympy_out"
  exit 1
fi
grep -Fxq 'SIX_ENDPOINTS_E5_E4_SYMPY_PASS_0A77C2' "$endpoints_sympy_out"

gp -q "$script_dir/verify_six_endpoints_e5_e4_pari.gp" >"$endpoints_pari_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)' "$endpoints_pari_out" || grep -Fq '***' "$endpoints_pari_out"; then
  cat "$endpoints_pari_out"
  exit 1
fi
grep -Fxq 'SIX_ENDPOINTS_E5_E4_PARI_PASS_682F1B' "$endpoints_pari_out"

cat "$sympy_out"
cat "$pari_out"
cat "$modular_out"
cat "$endpoints_sympy_out"
cat "$endpoints_pari_out"
echo "CTAU_INPUT_MANIFEST_PASS_D8C64E"
echo "CTAU_E5_ALL_STRICT_PASS_C593F0"
