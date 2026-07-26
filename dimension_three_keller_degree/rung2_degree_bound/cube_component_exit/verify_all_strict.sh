#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CHECK_TMP=$(mktemp -d "${TMPDIR:-/tmp}/cube-component-all-strict.XXXXXX")
trap 'rm -rf -- "$CHECK_TMP"' EXIT HUP INT TERM

if ! "$HERE/verify_strict.sh" >"$CHECK_TMP/primary.out" 2>&1
then
  cat "$CHECK_TMP/primary.out" >&2
  echo "primary strict verification failed" >&2
  exit 1
fi
grep -Fx "CUBE_COMPONENT_EXIT_STRICT_PASS" "$CHECK_TMP/primary.out" >/dev/null
cat "$CHECK_TMP/primary.out"

if ! "$HERE/audit_hostile/verify_strict.sh" >"$CHECK_TMP/hostile.out" 2>&1
then
  cat "$CHECK_TMP/hostile.out" >&2
  echo "hostile strict verification failed" >&2
  exit 1
fi
grep -Fx "CUBE_COMPONENT_HOSTILE_AUDIT_PASS" "$CHECK_TMP/hostile.out" >/dev/null
cat "$CHECK_TMP/hostile.out"

echo "CUBE_COMPONENT_ALL_STRICT_PASS"
