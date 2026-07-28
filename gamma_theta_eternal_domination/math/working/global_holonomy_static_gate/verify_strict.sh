#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CAMPAIGN=$(CDPATH= cd -- "$HERE/../../.." && pwd)
CADICAL="$CAMPAIGN/tools/cadical_3_0_1/build/cadical"
LABELG="$CAMPAIGN/tools/nauty2_9_3/labelg"

test "$(shasum -a 256 "$CADICAL" | awk '{print $1}')" = \
  "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
test "$(shasum -a 256 "$LABELG" | awk '{print $1}')" = \
  "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"

TEMPORARY=$(mktemp -d "${TMPDIR:-/tmp}/global-holonomy-static.XXXXXX")
trap 'rm -rf "$TEMPORARY"' EXIT HUP INT TERM

python3 "$HERE/verify_witness.py" \
  --witness "$HERE/WITNESS.json" \
  --labelg "$LABELG" \
  > "$TEMPORARY/result.json"

test "$(shasum -a 256 "$TEMPORARY/result.json" | awk '{print $1}')" = \
  "$(tr -d '\n' < "$HERE/expected_result.sha256")"

(
  cd "$HERE"
  python3 audit_cegar.py --cadical "$CADICAL"
) > "$TEMPORARY/cegar.json"

cmp "$TEMPORARY/cegar.json" "$HERE/expected_cegar_audit.json"

echo "global-holonomy static-gate strict replay: PASS"
