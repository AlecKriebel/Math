#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
FREEZE=$(dirname "$HERE")
RUNG=$(dirname "$FREEZE")
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
GP_BIN=${GP_BIN:-/opt/homebrew/bin/gp}
TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/q2-e1-cubic-bridge.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

if [ ! -x "$PYTHON_BIN" ]; then
  echo "FAIL: missing Python interpreter: $PYTHON_BIN" >&2
  exit 1
fi
if [ ! -x "$GP_BIN" ]; then
  echo "FAIL: missing PARI/GP interpreter: $GP_BIN" >&2
  exit 1
fi
if [ -n "${PYTHONOPTIMIZE:-}" ]; then
  echo "FAIL: caller supplied PYTHONOPTIMIZE" >&2
  exit 1
fi

(
  cd "$HERE"
  shasum -a 256 -c SOURCE_SHA256.txt >"$TMP_AUDIT/source-hashes.out"
)

run_python_check() {
  script=$1
  marker=$2
  output=$3
  "$PYTHON_BIN" "$script" >"$output"
  grep -Fqx "$marker" "$output" >/dev/null || {
    echo "FAIL: missing marker from $script" >&2
    exit 1
  }
}

run_gp_check() {
  script=$1
  marker=$2
  output=$3
  "$GP_BIN" -q "$script" >"$output"
  grep -Fqx "$marker" "$output" >/dev/null || {
    echo "FAIL: missing marker from $script" >&2
    exit 1
  }
}

BRIDGE_CHECK="$HERE/verify_bridge_q2_e1_a1_b3_d3_n1_v1.py"
run_python_check \
  "$BRIDGE_CHECK" \
  "Q2_E1_A1_B3_D3_N1_BRIDGE_PASS_V1" \
  "$TMP_AUDIT/bridge.out"
run_python_check \
  "$HERE/verify_prelegacy_normal_form_and_routing.py" \
  "PASS: intrinsic cusp/node forms and exact C00--C44 routing" \
  "$TMP_AUDIT/prelegacy-routing.out"

run_python_check \
  "$RUNG/verify_nodal_cubic_exit_sympy.py" \
  "nodal cubic-stratum exit SymPy checks passed" \
  "$TMP_AUDIT/nodal-sympy.out"
run_python_check \
  "$RUNG/verify_scalar_aligned_nodal_sympy.py" \
  "scalar-aligned nodal symbolic SymPy checks passed" \
  "$TMP_AUDIT/aligned-nodal-sympy.out"
run_python_check \
  "$RUNG/verify_cuspidal_cubic_exit_sympy.py" \
  "cuspidal cubic-stratum exit SymPy checks passed" \
  "$TMP_AUDIT/cusp-sympy.out"
run_python_check \
  "$RUNG/verify_scalar_aligned_cusp_sympy.py" \
  "scalar-aligned cuspidal-cubic SymPy checks passed" \
  "$TMP_AUDIT/aligned-cusp-sympy.out"

run_gp_check \
  "$RUNG/verify_nodal_cubic_exit_pari.gp" \
  "nodal cubic-stratum exit PARI/GP checks passed" \
  "$TMP_AUDIT/nodal-pari.out"
run_gp_check \
  "$RUNG/verify_scalar_aligned_nodal_pari.gp" \
  "scalar-aligned nodal PARI/GP checks passed" \
  "$TMP_AUDIT/aligned-nodal-pari.out"
run_gp_check \
  "$RUNG/verify_cuspidal_cubic_exit_pari.gp" \
  "cuspidal cubic-stratum exit PARI/GP checks passed" \
  "$TMP_AUDIT/cusp-pari.out"
run_gp_check \
  "$RUNG/verify_scalar_aligned_cusp_pari.gp" \
  "scalar-aligned cuspidal-cubic PARI/GP checks passed" \
  "$TMP_AUDIT/aligned-cusp-pari.out"

for mutation in row_tuple pivot_tail nodal_rank; do
  mutation_output="$TMP_AUDIT/mutation-$mutation.out"
  if Q2_E1_CUBIC_BRIDGE_MUTATION=$mutation \
    "$PYTHON_BIN" "$BRIDGE_CHECK" >"$mutation_output" 2>&1
  then
    echo "FAIL: mutation survived: $mutation" >&2
    exit 1
  fi
  grep -Fq "FAIL:" "$mutation_output" >/dev/null || {
    echo "FAIL: mutation did not fail closed: $mutation" >&2
    exit 1
  }
done

PYTHONOPTIMIZE=1 "$PYTHON_BIN" "$BRIDGE_CHECK" \
  >"$TMP_AUDIT/optimized-bridge.out"
grep -Fqx "Q2_E1_A1_B3_D3_N1_BRIDGE_PASS_V1" \
  "$TMP_AUDIT/optimized-bridge.out" >/dev/null || {
  echo "FAIL: explicit bridge checks disappeared under optimization" >&2
  exit 1
}

echo "Q2_E1_A1_B3_D3_N1_STRICT_PASS_V1"
