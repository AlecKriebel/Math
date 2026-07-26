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

tmp_dir=$(mktemp -d)
cleanup()
{
  case "$tmp_dir" in
    /var/folders/*/T/tmp.*|/tmp/tmp.*) rm -rf -- "$tmp_dir" ;;
    *) echo "FAIL: refusing to remove unexpected temporary path" >&2; exit 2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM

sh "$script_dir/verify_all_strict.sh"
sh "$script_dir/test_fail_closed.sh"
sh "$script_dir/quartic_survivor_search/verify_strict.sh"
sh "$script_dir/../audit_marked_orbit_hostile_2/verify_strict.sh"
"$task_python" \
  "$script_dir/../audit_marked_orbit_reconstruction/verify_marked_orbits_exact.py"

endpoint_out=$(
  "$task_python" \
    "$script_dir/endpoint_closure/verify_endpoint_closure_sympy.py"
)
printf '%s\n' "$endpoint_out"
printf '%s\n' "$endpoint_out" |
  grep -Fxq 'MARKED_DISTINCT_ENDPOINTS_SYMPY_PASS_0E5C42'

co_out=$(
  "$task_python" \
    "$script_dir/co_closure/verify_co_closure_sympy.py"
)
printf '%s\n' "$co_out"
printf '%s\n' "$co_out" |
  grep -Fxq 'MARKED_DISTINCT_CO_SYMPY_PASS_B74219'

if "$task_python" -O \
  "$script_dir/endpoint_closure/verify_endpoint_closure_sympy.py" \
  >"$tmp_dir/endpoint_optimized.out" 2>&1; then
  echo "FAIL: endpoint verifier passed with assertions disabled" >&2
  exit 1
fi
grep -Fq 'assertions are required' "$tmp_dir/endpoint_optimized.out"

if "$task_python" -O \
  "$script_dir/co_closure/verify_co_closure_sympy.py" \
  >"$tmp_dir/co_optimized.out" 2>&1; then
  echo "FAIL: CO verifier passed with assertions disabled" >&2
  exit 1
fi
grep -Fq 'assertions are required' "$tmp_dir/co_optimized.out"

sed 's/== -8 \\* ell\\[8\\] \\*\\* 2/== -7 * ell[8] ** 2/' \
  "$script_dir/endpoint_closure/verify_endpoint_closure_sympy.py" \
  >"$tmp_dir/endpoint_mutated.py"
if "$task_python" "$tmp_dir/endpoint_mutated.py" \
  >"$tmp_dir/endpoint_mutated.out" 2>&1; then
  echo "FAIL: mutated endpoint E4 coefficient passed" >&2
  exit 1
fi
grep -Eq 'AssertionError|Traceback' "$tmp_dir/endpoint_mutated.out"

sed 's/-45137758519296/-45137758519295/' \
  "$script_dir/co_closure/verify_co_closure_sympy.py" \
  >"$tmp_dir/co_mutated.py"
if "$task_python" "$tmp_dir/co_mutated.py" \
  >"$tmp_dir/co_mutated.out" 2>&1; then
  echo "FAIL: mutated CO E7 minor passed" >&2
  exit 1
fi
grep -Eq 'AssertionError|Traceback' "$tmp_dir/co_mutated.out"

echo "MARKED_DISTINCT_CLOSURE_STRICT_PASS_E2D013"
