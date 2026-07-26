#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ -n "${PYTHON_BIN:-}" ]; then
  :
elif python3 -c 'import sympy' >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif [ -x /Users/alec/Documents/Math/.venv/bin/python ]; then
  PYTHON_BIN=/Users/alec/Documents/Math/.venv/bin/python
else
  echo "FAIL: no Python interpreter with SymPy is available" >&2
  exit 1
fi

"$PYTHON_BIN" "$HERE/verify_independent_bridge_q2_e0_a2_b2_d2_n1_v1.py"

for mutation in hash pivots e7_rank e7_compat e6_rank lower_output
do
  if "$PYTHON_BIN" \
      "$HERE/verify_independent_bridge_q2_e0_a2_b2_d2_n1_v1.py" \
      --mutation "$mutation" >/dev/null 2>&1
  then
    echo "FAIL: required mutation passed: $mutation" >&2
    exit 1
  fi
done

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" \
    "$HERE/verify_independent_bridge_q2_e0_a2_b2_d2_n1_v1.py" \
    >/dev/null 2>&1
then
  echo "FAIL: optimized Python bypassed assertion guard" >&2
  exit 1
fi

echo "INDEPENDENT_Q2_E0_A2_B2_D2_N1_STRICT_PASS"
