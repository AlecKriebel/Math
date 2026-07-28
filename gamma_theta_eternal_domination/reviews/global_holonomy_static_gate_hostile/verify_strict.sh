#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CAMPAIGN=$(CDPATH= cd -- "$HERE/../.." && pwd)
CANDIDATE="$CAMPAIGN/math/working/global_holonomy_static_gate"
LABELG="$CAMPAIGN/tools/nauty2_9_3/labelg"
GENG="$CAMPAIGN/tools/nauty2_9_3/geng"
CADICAL="$CAMPAIGN/tools/cadical_3_0_1/build/cadical"

test "$(shasum -a 256 "$LABELG" | awk '{print $1}')" = \
  "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
test "$(shasum -a 256 "$GENG" | awk '{print $1}')" = \
  "588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1"
test "$(shasum -a 256 "$CADICAL" | awk '{print $1}')" = \
  "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"

TEMPORARY=$(mktemp -d "${TMPDIR:-/tmp}/global-holonomy-hostile.XXXXXX")
trap 'rm -rf "$TEMPORARY"' EXIT HUP INT TERM

python3 "$HERE/verify_independent.py" \
  --candidate "$CANDIDATE" \
  --labelg "$LABELG" \
  --geng "$GENG" \
  > "$TEMPORARY/result.json"

test "$(shasum -a 256 "$TEMPORARY/result.json" | awk '{print $1}')" = \
  "$(tr -d '\n' < "$HERE/expected_result.sha256")"

"$CANDIDATE/verify_strict.sh" > "$TEMPORARY/candidate-replay.log"
grep -qx "global-holonomy static-gate strict replay: PASS" \
  "$TEMPORARY/candidate-replay.log"

echo "global-holonomy static-gate hostile replay: PASS"
