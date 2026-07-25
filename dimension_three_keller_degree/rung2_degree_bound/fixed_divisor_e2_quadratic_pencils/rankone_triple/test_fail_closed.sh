#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/rankone-fail.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

check_rejected()
{
  label=$1
  edit=$2
  forged="$scratch_dir/$label.py"
  sed "$edit" "$script_dir/verify_rankone_triple_sympy.py" >"$forged"
  if "$script_dir/verify_rankone_triple_sympy_strict.sh" "$forged" \
      >/dev/null 2>&1; then
    echo "FAIL: forged SymPy certificate was accepted: $label" >&2
    exit 1
  fi
  echo "PASS fail-closed rejection: $label"
}

check_rejected wrong_raw_minor 's/1889568/1889569/'
check_rejected wrong_plus_square \
  's/sp.Rational(3, 2) \* H\*\*2/sp.Rational(5, 2) * H**2/'
check_rejected wrong_a3_zero_minor 's/2048, 81/2049, 81/'
check_rejected missing_final_marker \
  '/all rank-one e=2 triple-companion certificates passed/d'

if /usr/bin/python3 -O "$script_dir/verify_rankone_triple_sympy.py" \
    >/dev/null 2>&1; then
  echo "FAIL: optimized Python run bypassed assertions" >&2
  exit 1
fi
echo "PASS optimized Python run rejected"
echo "PASS all SymPy fail-closed injections rejected"
