#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
GP_BIN=${GP_BIN:-/opt/homebrew/bin/gp}
RELEASE="$HERE/../d3_construction_search"
CHECK_TMP=$(mktemp -d "${TMPDIR:-/tmp}/d3-bb21-hostile.XXXXXX")
trap 'rm -rf -- "$CHECK_TMP"' EXIT HUP INT TERM

[ -x "$PYTHON_BIN" ] || {
  echo "missing Python interpreter: $PYTHON_BIN" >&2
  exit 1
}

"$PYTHON_BIN" "$HERE/audit_bb21_dependency_free.py" >"$CHECK_TMP/audit.out"
grep -Fx "D3_BB21_DEPENDENCY_FREE_HOSTILE_PASS" "$CHECK_TMP/audit.out" >/dev/null

"$PYTHON_BIN" "$HERE/verify_release_binding.py" >"$CHECK_TMP/binding.out"
grep -Fx "D3_BB21_RELEASE_BINDING_PASS" "$CHECK_TMP/binding.out" >/dev/null

"$PYTHON_BIN" "$HERE/verify_candidate_bb_only.py" >"$CHECK_TMP/primary-bb.out"
grep -Fx "D3_BB21_CANDIDATE_PRIMARY_ONLY_PASS" \
    "$CHECK_TMP/primary-bb.out" >/dev/null

[ -x "$GP_BIN" ] || {
  echo "missing PARI/GP interpreter: $GP_BIN" >&2
  exit 1
}
"$GP_BIN" -q "$RELEASE/verify_independent_pari.gp" \
    >"$CHECK_TMP/pari.out" 2>&1
if grep -E '\*\*\*|syntax error|skipping file' "$CHECK_TMP/pari.out" >/dev/null
then
  echo "independent PARI emitted an interpreter error" >&2
  exit 1
fi
grep -Fx "D3_CONSTRUCTION_INDEPENDENT_PARI_PASS" "$CHECK_TMP/pari.out" >/dev/null
for marker in \
  "PASS BB zero r2-kernel first pivot" \
  "PASS BB zero r2-kernel second pivot" \
  "PASS BB full arbitrary-binary E9" \
  "PASS BB full arbitrary-binary E8" \
  "PASS BB full arbitrary-binary E7" \
  "PASS BB complete E6 pivot replay" \
  "PASS BB full decisive E5 coefficient" \
  "PASS BB origin structural E6 identity"
do
  grep -Fx "$marker" "$CHECK_TMP/pari.out" >/dev/null
done

for mutation in degree0 e5 resultant origin denominator
do
  if "$PYTHON_BIN" "$HERE/audit_bb21_dependency_free.py" \
      --mutation "$mutation" >"$CHECK_TMP/$mutation.out" 2>&1
  then
    echo "required-failure hostile mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -F "AssertionError" "$CHECK_TMP/$mutation.out" >/dev/null
  if grep -Fx "D3_BB21_DEPENDENCY_FREE_HOSTILE_PASS" \
      "$CHECK_TMP/$mutation.out" >/dev/null
  then
    echo "hostile mutation reached terminal marker: $mutation" >&2
    exit 1
  fi
done

if "$PYTHON_BIN" "$HERE/verify_release_binding.py" --mutation contract \
    >"$CHECK_TMP/contract.out" 2>&1
then
  echo "required-failure release-contract mutation unexpectedly passed" >&2
  exit 1
fi
grep -F "AssertionError" "$CHECK_TMP/contract.out" >/dev/null

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" "$HERE/audit_bb21_dependency_free.py" \
    >"$CHECK_TMP/optimized.out" 2>&1
then
  echo "optimized Python bypassed hostile assertion guard" >&2
  exit 1
fi
grep -F "assertions disabled" "$CHECK_TMP/optimized.out" >/dev/null

echo "D3_BB21_HOSTILE_RELEASE_AUDIT_PASS"
