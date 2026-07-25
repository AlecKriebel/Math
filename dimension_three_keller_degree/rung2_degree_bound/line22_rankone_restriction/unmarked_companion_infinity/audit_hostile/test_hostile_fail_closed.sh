#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_file="$script_dir/verify_unmarked_infinity_pure.py"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/unmarked-infinity-hostile-fail.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

check_rejected()
{
  label=$1
  edit=$2
  forged="$scratch/$label.py"
  sed "$edit" "$source_file" >"$forged"
  if "$script_dir/verify_hostile_strict.sh" "$forged" >/dev/null 2>&1; then
    echo "FAIL: hostile verifier accepted mutation: $label" >&2
    exit 1
  fi
  echo "PASS hostile fail-closed rejection: $label"
}

check_rejected raw_minor \
  's/1709960483517235200,/1709960483517235201,/'
check_rejected e6_minor \
  's/4831838208, "E6 forcing minor"/4831838209, "E6 forcing minor"/'
check_rejected e5_literal \
  's/scale(variable("l1"), -4), scale(variable("l4"), 4)/scale(variable("l1"), -5), scale(variable("l4"), 4)/'
check_rejected final_marker \
  '/ALL HOSTILE PURE-PYTHON UNMARKED-INFINITY CHECKS PASSED/d'

optimized="$scratch/optimized.log"
if ! /usr/bin/python3 -O -u "$source_file" >"$optimized" 2>&1; then
  cat "$optimized"
  echo "FAIL: dependency-free verifier failed under optimized Python" >&2
  exit 1
fi
if ! grep -Fqx \
  "ALL HOSTILE PURE-PYTHON UNMARKED-INFINITY CHECKS PASSED" \
  "$optimized"; then
  cat "$optimized"
  echo "FAIL: optimized dependency-free verifier omitted completion marker" >&2
  exit 1
fi
echo "PASS hostile verifier is not assertion-dependent"
echo "ALL HOSTILE FAIL-CLOSED MUTATIONS REJECTED"
