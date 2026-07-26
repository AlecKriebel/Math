#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CHECK_TMP=$(mktemp -d "${TMPDIR:-/tmp}/cube-component-exit.XXXXXX")
trap 'rm -rf -- "$CHECK_TMP"' EXIT HUP INT TERM

python3 "$HERE/verify_theorem.py" >"$CHECK_TMP/theorem.out"
grep -Fx "CUBE_COMPONENT_THEOREM_EXACT_PASS" "$CHECK_TMP/theorem.out" >/dev/null

python3 "$HERE/verify_denominator_bridge.py" >"$CHECK_TMP/bridge.out"
grep -Fx "CUBE_COMPONENT_DENOMINATOR_BRIDGE_PASS" "$CHECK_TMP/bridge.out" >/dev/null

for mutation in rank2_lead coordinate_sign degree_boundary
do
  if python3 "$HERE/verify_theorem.py" --mutation "$mutation" >"$CHECK_TMP/$mutation.out" 2>&1
  then
    echo "required-failure mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -F "AssertionError" "$CHECK_TMP/$mutation.out" >/dev/null
done

if python3 "$HERE/verify_denominator_bridge.py" --mutation scope >"$CHECK_TMP/scope.out" 2>&1
then
  echo "required-failure mutation unexpectedly passed: scope" >&2
  exit 1
fi
grep -F "AssertionError" "$CHECK_TMP/scope.out" >/dev/null

echo "CUBE_COMPONENT_EXIT_STRICT_PASS"
