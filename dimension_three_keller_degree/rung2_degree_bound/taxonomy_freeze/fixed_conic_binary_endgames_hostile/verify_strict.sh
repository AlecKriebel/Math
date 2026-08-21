#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
out_main=$(mktemp)
out_zero=$(mktemp)
trap 'rm -f "$out_main" "$out_zero"' EXIT HUP INT TERM

gp -q "$here/explore_endgames.gp" >"$out_main" 2>&1
gp -q "$here/verify_zero_tangent.gp" >"$out_zero" 2>&1

if grep -E '\*\*\*|user error|syntax error|type error' "$out_main" "$out_zero" |
    grep -v 'Warning:' >/dev/null; then
  sed -n '1,240p' "$out_main"
  sed -n '1,240p' "$out_zero"
  exit 1
fi

require_main() {
  grep -F "$1" "$out_main" >/dev/null || {
    echo "missing main certificate: $1" >&2
    exit 1
  }
}

require_zero() {
  grep -F "$1" "$out_zero" >/dev/null || {
    echo "missing zero-tangent certificate: $1" >&2
    exit 1
  }
}

require_main 'opposite E6 ell rank = 3'
require_main 'opposite E5 compat 1 = 64'
require_main 'semisimple E4 remaining-ell rank = 2/2, minor = -8'
require_main 'semisimple solved det(L) = 0'
require_main 'nilpotent K!=0 minors E6/E5/E4 = -128/128/-16*w11^3'
require_main 'nilpotent K!=0 final solved det(L) = 0'
require_main 'nilpotent K=0 column relation PASS'
require_main 'nilpotent K=0 solved det(L) = 0'
require_main 'split-scalar final E4 coefficient = 0'
require_main 'split-scalar E2 square and det(L) ideal identity PASS'
require_main 'double-scalar final E4 coefficient = 0'
require_main 'double-scalar E2 square and det(L) ideal identity PASS'
require_main 'PASS hostile complete binary fixed-conic endgames'

require_zero 'split-one E5 constant compatibilities = [8]'
require_zero 'split-two E5 constant compatibilities = [8, -16, 8]'
require_zero 'double-Ap E5 constant compatibilities = [8]'
require_zero 'double-Aq E5 constant compatibilities = [8]'
require_zero 'PASS zero-tangent orbit audit'

echo 'PASS strict hostile complete binary fixed-conic endgames'
