#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
task_python=${TASK_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
tmp_dir=$(mktemp -d)

cleanup()
{
  case "$tmp_dir" in
    /var/folders/*/T/tmp.*|/tmp/tmp.*) rm -rf -- "$tmp_dir" ;;
    *) echo "FAIL: refusing to remove unexpected temporary path" >&2; exit 2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM

sed 's/"e6_det": 256/"e6_det": 257/g' \
  "$script_dir/verify_e7_e6_sympy.py" >"$tmp_dir/mutated_sympy.py"
if "$task_python" "$tmp_dir/mutated_sympy.py" >"$tmp_dir/sympy.out" 2>&1; then
  echo "FAIL: mutated SymPy certificate passed" >&2
  exit 1
fi
grep -Eq 'AssertionError|Traceback' "$tmp_dir/sympy.out"

sed 's/,256,/,257,/g' \
  "$script_dir/verify_e7_e6_pari.gp" >"$tmp_dir/mutated_pari.gp"
if gp -q "$tmp_dir/mutated_pari.gp" >"$tmp_dir/pari.out" 2>&1; then
  echo "FAIL: mutated PARI certificate passed" >&2
  exit 1
fi
grep -Fq 'FAIL:' "$tmp_dir/pari.out"

echo "PASS fail-closed: both independent certificates reject a pivot mutation"
