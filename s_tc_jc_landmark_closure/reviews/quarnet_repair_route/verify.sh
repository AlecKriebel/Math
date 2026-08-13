#!/usr/bin/env bash
set -euo pipefail

here="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

python3 "$here/check_minimal_repairs.py" > "$tmp"
diff -u "$here/EXPECTED_OUTPUT.txt" "$tmp"
echo "VERIFIED: aligned minimal weak-Theta repairs"
