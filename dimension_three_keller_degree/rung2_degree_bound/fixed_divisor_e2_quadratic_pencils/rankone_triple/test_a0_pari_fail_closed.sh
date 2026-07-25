#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/rankone-a0-pari-fail.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

check_rejected()
{
  label=$1
  edit=$2
  forged="$scratch_dir/$label.gp"
  sed "$edit" "$script_dir/verify_a0_pari.gp" >"$forged"
  if "$script_dir/verify_a0_pari_strict.sh" "$forged" \
      >/dev/null 2>&1; then
    echo "FAIL: forged PARI certificate was accepted: $label" >&2
    exit 1
  fi
  echo "PASS fail-closed rejection: $label"
}

check_rejected wrong_xz_augmented_minor \
  's/s^6[*]C6)/s^7*C6)/'
check_rejected wrong_xz_e4_residual \
  's|-8/27[*]s^4|-7/27*s^4|'
check_rejected wrong_a3_zero_minor \
  's/associate(w3RzeroPivot,s^8)/associate(w3RzeroPivot,s^7)/'
check_rejected wrong_gzero_remainder \
  's|-2[*]s[*](s-6[*]hh)|-3*s*(s-6*hh)|'
check_rejected missing_final_marker \
  '/all independent PARI A=0 certificates passed/d'

echo "PASS all A=0 PARI fail-closed injections rejected"
