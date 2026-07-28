#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
campaign=$(CDPATH= cd -- "$here/../../.." && pwd)
temporary=$(mktemp -d "${TMPDIR:-/tmp}/rank-one-ur1-verify.XXXXXX")
trap 'rm -rf "$temporary"' EXIT HUP INT TERM

python3 -I "$here/verify_implication.py" > "$temporary/implication.json"
cmp "$here/expected_result.json" "$temporary/implication.json"

PYTHONPATH="$campaign/src" python3 -m verifier_a.cli Hslaghb \
  > "$temporary/verifier_a.json"
PYTHONPATH="$campaign/src" python3 -m verifier_b.cli Hslaghb \
  > "$temporary/verifier_b.json"
python3 -I "$here/verify_control.py" \
  --verifier-a "$temporary/verifier_a.json" \
  --verifier-b "$temporary/verifier_b.json" \
  > "$temporary/control.json"
cmp "$here/expected_control_result.json" "$temporary/control.json"

printf '%s\n' 'rank-one ur=1 normalization audit: PASS'
