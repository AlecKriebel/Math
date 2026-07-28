#!/bin/sh
set -eu

campaign_dir=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
candidate_dir="$campaign_dir/math/working/full_list_positive_rank_terminal"
review_dir="$campaign_dir/reviews/full_list_positive_rank_terminal_hostile"
result_file=$(mktemp "${TMPDIR:-/tmp}/positive-rank-hostile.XXXXXX")
trap 'rm -f "$result_file"' EXIT HUP INT TERM

check_hash() {
    expected=$1
    path=$2
    actual=$(shasum -a 256 "$path" | awk '{print $1}')
    test "$actual" = "$expected"
}

check_hash \
    e25845bbf5e23886284f2046ac8c5c661b48176f4bef9fda5651f733d4a0edb0 \
    "$candidate_dir/CANDIDATE.md"
check_hash \
    6368b2d1d4735d5846f32653eff299587d265487a3bf5a2bafb9ed37b3627884 \
    "$candidate_dir/RESEARCH_LOG.md"
check_hash \
    11b7f63545ad020ed58292e394fc8f0131948dfb1f01bbc8c707ae6da7e14424 \
    "$candidate_dir/probe_positive_rank.py"
check_hash \
    a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d \
    "$campaign_dir/math/working/full_list_safe_color_proof/NOTE.md"
check_hash \
    0d6eb44fa2807cd34e441c31364149577cccf39f28b426a5d81b7cc78c9d1253 \
    "$campaign_dir/math/working/full_list_terminal_gate/NOTE.md"
check_hash \
    0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c \
    "$campaign_dir/math/working/full_list_nonsingleton_terminal/CANDIDATE.md"
check_hash \
    25d80b1167ada960339ae00ad1e1a3ea9919593c1995be54543dc3946755cd56 \
    "$review_dir/independent_replay.py"

sh "$candidate_dir/verify_strict.sh"

python3 -I -B -W error \
    "$review_dir/independent_replay.py" >"$result_file"

test "$(shasum -a 256 "$result_file" | awk '{print $1}')" = \
    26c5ef99ab8a6719135615c9fa0c9d5061628671add43fd2e2565c2dd8a58a00

python3 -I -B -W error - "$result_file" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    result = json.load(stream)

assert result["schema"] == "full-list-positive-rank-hostile-replay-v1"
controls = result["controls"]
assert controls["equality_anchor_rank_drop"]["parameters"] == {
    "gamma": 3,
    "alpha": 3,
    "gamma_infinity": 3,
    "theta": 3,
}
for name in (
    "gamma2_nonretained_corridor_alternate",
    "gamma2_missing_palette_not_missing_edge",
):
    assert controls[name]["parameters"] == {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 4,
    }
assert controls["equality_anchor_rank_drop"]["named_entry"]["rank"] == 1
assert controls["equality_anchor_rank_drop"]["alternate_rank"] == 0
assert controls["gamma2_nonretained_corridor_alternate"][
    "alternate_retained"
] is False
assert controls["gamma2_missing_palette_not_missing_edge"][
    "alternate_retained"
] is True
print("PASS full-list-positive-rank-terminal hostile review")
PY
