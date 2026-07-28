#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../.." && pwd)
PYTHON=${PYTHON:-python3}

"$PYTHON" -I -B -W error "$HERE/verify_dichotomy.py" > "$HERE/.audit-result.tmp"
cmp "$HERE/.audit-result.tmp" "$HERE/AUDIT_RESULT.json"
rm "$HERE/.audit-result.tmp"

"$PYTHON" -I -B -W error "$HERE/audit_manifest.py"

echo "Adjacent-pair repair dichotomy: PASS"
