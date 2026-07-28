#!/bin/sh
set -eu

campaign=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
review="$campaign/reviews/rank_one_qqaq0_hostile"
temporary=$(mktemp -d "${TMPDIR:-/tmp}/rank-one-qqaq0-hostile.XXXXXX")
trap 'find "$temporary" -type f -delete; rmdir "$temporary"' EXIT HUP INT TERM

python3 -I -B -W error "$review/independent_check.py" \
  > "$temporary/result.json"
cmp "$review/independent_result.json" "$temporary/result.json"
printf '%s\n' 'rank-one QQ0/AQ0 hostile clean-room audit: PASS'
