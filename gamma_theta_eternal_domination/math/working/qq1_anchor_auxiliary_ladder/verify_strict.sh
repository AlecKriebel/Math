#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CAMPAIGN=$(CDPATH= cd -- "$HERE/../../.." && pwd)
LABELG="$CAMPAIGN/tools/nauty2_9_3/labelg"
EXPECTED_RESULT_SHA256="67f0e97b8cdbb3379215b7783125a139223030105010bde64b9e24b79b7c9845"
EXPECTED_LABELG_SHA256="ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/qq1-anchor-audit.XXXXXX")
trap 'rm -rf "$WORK"' EXIT HUP INT TERM

export PYTHONDONTWRITEBYTECODE=1

actual_labelg=$(shasum -a 256 "$LABELG" | awk '{print $1}')
test "$actual_labelg" = "$EXPECTED_LABELG_SHA256"

python3 "$HERE/verify_control.py" --labelg "$LABELG" > "$WORK/result.json"
python3 -m json.tool "$WORK/result.json" > /dev/null
actual_result=$(shasum -a 256 "$WORK/result.json" | awk '{print $1}')
test "$actual_result" = "$EXPECTED_RESULT_SHA256"

python3 "$HERE/audit_manifest.py"
python3 -m json.tool "$HERE/ABLATION_RESULTS.json" > /dev/null

echo "QQ1 anchor-auxiliary fixed-control audit: PASS"
