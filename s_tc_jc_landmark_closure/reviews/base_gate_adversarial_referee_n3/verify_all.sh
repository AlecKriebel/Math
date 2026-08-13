#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT=$(CDPATH= cd -- "$HERE/../.." && pwd)
REPO=$(CDPATH= cd -- "$PROJECT/.." && pwd)
TMP_REVIEW=$(mktemp -d "${TMPDIR:-/tmp}/base-gate-referee-n3.XXXXXX")
trap 'rm -rf "$TMP_REVIEW"' EXIT HUP INT TERM

test "$(git -C "$REPO" rev-parse be8a3087)" = be8a30870550efba2115cf2eb87e1d3611dd8c3b
test "$(git -C "$REPO" rev-parse f3cc9493)" = f3cc9493b1e677378e3c0b4f8e965cb9199a436f
test "$(git -C "$REPO" rev-parse 1018701d)" = 1018701d04d8656fe9ac92bb201413e043b802a1
test "$(git -C "$REPO" rev-parse 663336f8)" = 663336f839c29d91024220ed3777d0c124e975f5

env -i PATH="$PATH" PYTHONDONTWRITEBYTECODE=1 \
  python3 "$HERE/referee_n3.py" \
  --certificate "$TMP_REVIEW/certificate.json" \
  --mutations "$TMP_REVIEW/mutation_results.json"

cmp "$TMP_REVIEW/certificate.json" "$HERE/certificate.json"
cmp "$TMP_REVIEW/mutation_results.json" "$HERE/mutation_results.json"
(cd "$HERE" && shasum -a 256 -c MANIFEST.sha256)
printf '%s\n' 'VERIFIED: schema-3 n3 fixed-root base gate, scoped as reported'
