#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
AUDIT_TMP=$(mktemp -d "${TMPDIR:-/tmp}/power-fibre-cleanroom.XXXXXX")
trap 'rm -rf -- "$AUDIT_TMP"' EXIT HUP INT TERM

python3 "$HERE/verify_certificate.py" >"$AUDIT_TMP/python.out"
grep -Fx "POWER_FIBRE_CLEANROOM_STRICT_PASS" "$AUDIT_TMP/python.out" >/dev/null

gp -q "$HERE/verify_top_and_exits.gp" >"$AUDIT_TMP/pari.out"
grep -Fx "POWER_FIBRE_PARI_PASS" "$AUDIT_TMP/pari.out" >/dev/null

python3 "$HERE/verify_frozen_corollaries.py" >"$AUDIT_TMP/corollaries.out"
grep -Fx "POWER_FIBRE_FROZEN_COROLLARIES_PASS" "$AUDIT_TMP/corollaries.out" >/dev/null

for mutation in e7_contact e6_sign coordinate degree_ceiling
do
  if python3 "$HERE/verify_certificate.py" --mutation "$mutation" >"$AUDIT_TMP/$mutation.out" 2>&1
  then
    echo "required-failure mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -F "AssertionError:" "$AUDIT_TMP/$mutation.out" >/dev/null
done

if grep -R -n -E '(^|[^A-Za-z])(sympy|sage)([^A-Za-z]|$)' \
  "$HERE/verify_certificate.py" "$HERE/verify_top_and_exits.gp" \
  "$HERE/verify_frozen_corollaries.py" >/dev/null
then
  echo "forbidden symbolic dependency named in verifier" >&2
  exit 1
fi

echo "POWER_FIBRE_CLEANROOM_VERIFY_STRICT_PASS"
