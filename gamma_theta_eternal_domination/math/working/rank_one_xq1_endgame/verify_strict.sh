#!/bin/sh
set -eu

campaign=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
package="$campaign/math/working/rank_one_xq1_endgame"
temporary=$(mktemp -d "${TMPDIR:-/tmp}/rank-one-XQ1-verify.XXXXXX")
trap 'find "$temporary" -type f -delete; rmdir "$temporary"' EXIT HUP INT TERM

python3 -I -B -W error "$package/verify_implication.py" \
  > "$temporary/result.json"
cmp "$package/expected_result.json" "$temporary/result.json"
printf '%s\n' 'rank-one XQ1 implication audit: PASS'
