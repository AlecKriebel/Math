#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_file="$script_dir/verify_resonance_pari.gp"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/companion-resonance-fail.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

check_rejected()
{
  label=$1
  edit=$2
  forged="$scratch/$label.gp"
  sed "$edit" "$source_file" >"$forged"
  if "$script_dir/verify_resonance_pari_strict.sh" "$forged" \
      >/dev/null 2>&1; then
    echo "FAIL: hostile resonance verifier accepted mutation: $label" >&2
    exit 1
  fi
  echo "PASS hostile resonance rejection: $label"
}

check_rejected raw_minor \
  's/-990677827584,/-990677827583,/'
check_rejected kernel_minor \
  's/)),82944,/)),82945,/'
check_rejected square_chain \
  's/targets6=\[rw3\^2,/targets6=[rw3^2+1,/'
check_rejected e6_minor \
  's/)),5308416,/)),5308417,/'
check_rejected e5_residual \
  's|wantres=36\*Ktop|wantres=37*Ktop|'
check_rejected final_marker \
  '/ALL HOSTILE PARI COMPANION-INFINITY RESONANCE CHECKS PASSED/d'

echo "ALL HOSTILE RESONANCE FAIL-CLOSED MUTATIONS REJECTED"
