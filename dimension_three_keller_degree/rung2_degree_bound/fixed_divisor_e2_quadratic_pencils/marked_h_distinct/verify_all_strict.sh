#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
task_python=${TASK_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}

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
moduli_sympy_out=$(mktemp)
moduli_pari_out=$(mktemp)
tau_sympy_out=$(mktemp)
tau_pari_out=$(mktemp)
trap 'rm -f "$sympy_out" "$pari_out" "$moduli_sympy_out" "$moduli_pari_out" "$tau_sympy_out" "$tau_pari_out"' EXIT HUP INT TERM

"$task_python" "$script_dir/verify_e7_e6_sympy.py" >"$sympy_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)|Traceback|AssertionError' "$sympy_out"; then
  cat "$sympy_out"
  exit 1
fi
grep -Fxq 'PASS all six marked-h-distinct E7/E6 branches' "$sympy_out"

gp -q "$script_dir/verify_e7_e6_pari.gp" >"$pari_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)' "$pari_out" || grep -Fq '***' "$pari_out"; then
  cat "$pari_out"
  exit 1
fi
grep -Fxq 'PASS PARI: all six marked-h-distinct E7/E6 branches' "$pari_out"

"$task_python" "$script_dir/verify_companion_moduli_sympy.py" >"$moduli_sympy_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)|Traceback|AssertionError' "$moduli_sympy_out"; then
  cat "$moduli_sympy_out"
  exit 1
fi
grep -Fxq 'PASS companion moduli: endpoint exhaustion is false' "$moduli_sympy_out"

gp -q "$script_dir/verify_companion_moduli_pari.gp" >"$moduli_pari_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)' "$moduli_pari_out" || grep -Fq '***' "$moduli_pari_out"; then
  cat "$moduli_pari_out"
  exit 1
fi
grep -Fxq 'PASS PARI companion moduli: endpoint exhaustion is false' "$moduli_pari_out"

"$task_python" "$script_dir/verify_tau_family_sympy.py" >"$tau_sympy_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)|Traceback|AssertionError' "$tau_sympy_out"; then
  cat "$tau_sympy_out"
  exit 1
fi
grep -Fxq 'PASS tau family: k!=0 has E7 rank 18, three legal normal parameters, E6 rank 10 with no compatibility, and k survives' "$tau_sympy_out"

gp -q "$script_dir/verify_tau_family_pari.gp" >"$tau_pari_out" 2>&1
if grep -Eq '(^|[^A-Z])FAIL([^A-Z]|$)' "$tau_pari_out" || grep -Fq '***' "$tau_pari_out"; then
  cat "$tau_pari_out"
  exit 1
fi
grep -Fxq 'PASS PARI tau family: k survives E7/E6 with no compatibility' "$tau_pari_out"

cat "$sympy_out"
cat "$pari_out"
cat "$moduli_sympy_out"
cat "$moduli_pari_out"
cat "$tau_sympy_out"
cat "$tau_pari_out"
echo "PASS strict aggregate: independent SymPy and PARI reconstructions"
