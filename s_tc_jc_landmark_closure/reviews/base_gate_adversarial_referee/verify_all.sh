#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT=$(CDPATH= cd -- "$HERE/../.." && pwd)
REPO=$(CDPATH= cd -- "$PROJECT/.." && pwd)
TMP_REVIEW=$(mktemp -d "${TMPDIR:-/tmp}/base-gate-referee.XXXXXX")
trap 'rm -rf "$TMP_REVIEW"' EXIT HUP INT TERM

test "$(git -C "$REPO" rev-parse d7fb159e)" = d7fb159e038630b449bd87dc835432c5897788b6
test "$(git -C "$REPO" rev-parse f3cc9493)" = f3cc9493b1e677378e3c0b4f8e965cb9199a436f

env -i PATH="$PATH" PYTHONDONTWRITEBYTECODE=1 \
  python3 "$HERE/referee.py" \
  --certificate "$TMP_REVIEW/certificate.json" \
  --mutations "$TMP_REVIEW/mutation_results.json"

cmp "$TMP_REVIEW/certificate.json" "$HERE/certificate.json"
cmp "$TMP_REVIEW/mutation_results.json" "$HERE/mutation_results.json"
(cd "$HERE" && shasum -a 256 -c MANIFEST.sha256)
printf '%s\n' 'VERIFIED: corrected schema-3 n4 base gate, scoped as reported'
