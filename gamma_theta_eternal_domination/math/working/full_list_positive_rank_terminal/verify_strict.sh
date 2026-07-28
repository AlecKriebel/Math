#!/bin/sh
set -eu

campaign_dir=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
artifact_dir="$campaign_dir/math/working/full_list_positive_rank_terminal"
result_file=$(mktemp "${TMPDIR:-/tmp}/full-list-positive-rank.XXXXXX")
trap 'rm -f "$result_file"' EXIT HUP INT TERM

check_hash() {
    expected=$1
    path=$2
    actual=$(shasum -a 256 "$path" | awk '{print $1}')
    test "$actual" = "$expected"
}

check_hash \
    e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0 \
    "$artifact_dir/CANDIDATE.md"
check_hash \
    6368b2d1d4735d5846f32653eff299587d265487a3bf5a2bafb9ed37b3627884 \
    "$artifact_dir/RESEARCH_LOG.md"
check_hash \
    11b7f63545ad020ed58292e394fc8f0131948dfb1f01bbc8c707ae6da7e14424 \
    "$artifact_dir/probe_positive_rank.py"

python3 -I -B -W error \
    "$artifact_dir/probe_positive_rank.py" \
    --verify-controls >"$result_file"

python3 -I -B -W error - "$result_file" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    result = json.load(stream)

assert result["schema"] == "full-list-positive-rank-controls-v1"
assert result["equality_anchor_rank_drop"]["parameters"] == {
    "gamma": 3,
    "alpha": 3,
    "gamma_infinity": 3,
    "theta": 3,
}
for key in (
    "gamma2_nonretained_corridor_alternate",
    "gamma2_missing_palette_not_missing_edge",
):
    assert result[key]["parameters"] == {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 4,
    }
print("PASS full-list-positive-rank-terminal strict replay")
PY
