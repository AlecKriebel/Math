#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMPDIR_REPAIR=$(mktemp -d "${TMPDIR:-/tmp}/fixed-conic-pari.XXXXXX")
trap 'rm -rf "$TMPDIR_REPAIR"' EXIT HUP INT TERM
OUT="$TMPDIR_REPAIR/gp.out"

if ! gp -q "$HERE/verify_universal_e7_e6.gp" >"$OUT" 2>&1; then
  cat "$OUT"
  echo "FAIL gp returned nonzero" >&2
  exit 1
fi
cat "$OUT"

# GP can recover from a script-level error and still exit zero. Reject every
# diagnostic form observed for parse, type, and explicit certificate errors.
if grep -E '^[[:space:]]*\*\*\*' "$OUT" | grep -Fvq 'Warning:'; then
  echo "FAIL GP emitted a recovered error diagnostic" >&2
  exit 1
fi

require_marker() {
  if ! grep -Fqx "$1" "$OUT"; then
    echo "FAIL missing exact marker: $1" >&2
    exit 1
  fi
}

require_marker "CERT input dimensions V=12 H2=18 L=9"
require_marker "split E8 rank = 12, kernel dimension = 18"
require_marker "double E8 rank = 12, kernel dimension = 18"
require_marker "split E7 H2 rank = 7"
require_marker "double E7 H2 rank = 7"
require_marker "split fibre free H2 indices = Vecsmall([1, 2, 3, 7, 8, 9, 11, 13, 14, 15, 17])"
require_marker "double fibre free H2 indices = Vecsmall([1, 2, 3, 7, 8, 9, 11, 13, 14, 15, 17])"
require_marker "split E7 constant pivot determinant = -524288"
require_marker "double E7 constant pivot determinant = -524288"
require_marker "CERT split E6 R2=12*p^2*q^2*(a-d)^2*(a+d)"
require_marker "CERT double E6 R2=24*d*p^2*(c*p+(d-a)*q)^2"
require_marker "PASS universal E7 affine fibres and E6 r^2 identities"

echo "PASS strict fixed-conic binary PARI replay"
