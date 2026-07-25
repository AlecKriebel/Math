#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/aopen-pari-fail.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

check_rejected()
{
  label=$1
  edit=$2
  forged="$scratch_dir/$label.gp"
  sed "$edit" "$script_dir/verify_aopen_pari.gp" >"$forged"
  if "$script_dir/verify_aopen_pari_strict.sh" "$forged" >/dev/null 2>&1; then
    echo "FAIL: forged PARI certificate was accepted: $label" >&2
    exit 1
  fi
  echo "PASS fail-closed rejection: $label"
}

check_rejected wrong_w3_residual \
  's|-5\*ww\^3/12|-7*ww^3/12|'
check_rejected wrong_minus_residual \
  's|10\*ww\^4/81|11*ww^4/81|g'
check_rejected missing_final_marker \
  '/PASS all A!=0 branches excluded exactly in PARI\/GP/d'

echo "PASS all PARI fail-closed injections rejected"
